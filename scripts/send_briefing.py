#!/usr/bin/env python3
"""
BizBot Daily Briefing — Gmail Send Script
Generates HTML briefing email and sends via Gmail API.
Run manually or via launchd cron at 9am daily.
"""

import os, json, re, base64, gspread
from pathlib import Path
from datetime import date, datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collections import Counter

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ── Paths ──────────────────────────────────────────────────────────────────
BOT_DIR         = Path(__file__).parent.parent
CREDS_PATH      = BOT_DIR / "credentials" / "oauth_credentials.json"
TOKEN_PATH      = BOT_DIR / "credentials" / "authorized_user.json"
VAULT           = Path.home() / "Library/Mobile Documents/iCloud~md~obsidian/Documents/JARVIS-vault"
INBOX           = VAULT / "00-INBOX"
BRIEFS          = VAULT / "03-BRIEFS"
PUBLISHED       = VAULT / "04-PUBLISHED"
BRIDGE_FILE     = BRIEFS / "_bizbot-bridge.md"
SHEET_ID        = "1GT0JlOm0ehyycaQVkf93WjhYKrAJsN6ZzC_0c7ZGrOQ"
TO_EMAIL        = "nick.grosz@gmail.com"
SCOPES          = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose",
]

TODAY           = date.today()
TODAY_STR       = TODAY.strftime("%Y-%m-%d")
DISPLAY_DATE    = TODAY.strftime("%B %-d, %Y")

# ── Auth ───────────────────────────────────────────────────────────────────
def get_credentials():
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return creds


# ── CRM helpers ────────────────────────────────────────────────────────────
STAGE_PRIORITY = {
    "3. Request Accepted": 1,
    "4. Intro Sent":       2,
    "5. Meeting Requested": 3,
    "2. Request Sent":     4,
}
TIER_SCORE = {"Tier 0": 0, "Tier 1": 1, "Tier 2": 2, "High": 1, "Med": 2}
STAGE_LABEL = {
    "1. To Connect":        "To Connect",
    "1. Not Contacted":     "Not Contacted",
    "2. Request Sent":      "Request Sent",
    "3. Request Accepted":  "Accepted ✓",
    "4. Intro Sent":        "Intro Sent",
    "5. Meeting Requested": "Meeting Req'd",
    "13. Closed — Lost":    "Closed",
}


def parse_date(s):
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            pass
    return None


def overdue(nad_str):
    d = parse_date(nad_str)
    return d is not None and d <= TODAY


def read_crm(gc):
    sh = gc.open_by_key(SHEET_ID)

    def tab(name, header_row=3, skip=3):
        ws = sh.worksheet(name)
        rows = ws.get_all_values()
        return rows[header_row - 1], rows[skip:]

    otc_hdr, otc = tab("OTC & Market Makers")
    vc_hdr,  vc  = tab("Venture & Investment")

    try:
        ws_g    = sh.worksheet("🎯 Grants Pipeline")
        g_rows  = ws_g.get_all_values()
        g_hi    = next((i for i, r in enumerate(g_rows) if "Status" in r), 1)
        grants  = g_rows[g_hi + 1:]
        g_hdr   = g_rows[g_hi]
    except Exception:
        grants, g_hdr = [], []

    return otc, vc, grants, g_hdr


def pipeline_counts(rows, status_col=1):
    return Counter(r[status_col] for r in rows if len(r) > status_col and r[status_col])


def clean_linkedin_url(raw):
    """Strip UTM params, return clean profile URL."""
    if not raw:
        return ""
    return raw.split("?")[0].rstrip("/")


# ── Platform section parsing (shared with JARVIS email) ────────────────────
_PLATFORM_HEADERS = [
    "X Thread", "Twitter Thread", "Twitter",
    "LinkedIn Personal", "LinkedIn Company", "LinkedIn",
    "Substack", "Instagram", "Company Blog",
]

PLATFORM_SECTION_STYLE = {
    "x thread":         {"color": "#000000", "label": "X Thread",  "compose": "https://x.com/compose/post"},
    "twitter":          {"color": "#000000", "label": "X Thread",  "compose": "https://x.com/compose/post"},
    "linkedin personal":{"color": "#0A66C2", "label": "LinkedIn",  "compose": "https://www.linkedin.com/feed/"},
    "linkedin company": {"color": "#004182", "label": "LinkedIn Co","compose": "https://www.linkedin.com/"},
    "linkedin":         {"color": "#0A66C2", "label": "LinkedIn",  "compose": "https://www.linkedin.com/feed/"},
    "substack":         {"color": "#FF6719", "label": "Substack",  "compose": "https://substack.com/"},
    "instagram":        {"color": "#E1306C", "label": "Instagram", "compose": "https://www.instagram.com/"},
    "company blog":     {"color": "#6B7280", "label": "Blog",      "compose": "#"},
}


def parse_platform_sections(body):
    """Split DRAFTS body by ## Platform headers. Returns {header: content}."""
    parts = re.split(r"^## (.+)$", body, flags=re.MULTILINE)
    sections = {}
    for i in range(1, len(parts), 2):
        header  = parts[i].strip()
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        if any(ph.lower() in header.lower() for ph in _PLATFORM_HEADERS):
            sections[header] = content
    return sections


def top20_messages(otc_rows):
    scored = []
    for r in otc_rows:
        if len(r) < 10:
            continue
        status = r[1]
        if status not in STAGE_PRIORITY:
            continue
        msg = r[9].strip()
        if not msg:
            continue
        tier     = r[0].strip()
        li_url   = clean_linkedin_url(r[6]) if len(r) > 6 else ""
        score    = STAGE_PRIORITY[status] * 10 + TIER_SCORE.get(tier, 5)
        scored.append((score, r[3], r[5], r[4], status, msg, tier, li_url))
    scored.sort(key=lambda x: x[0])
    return scored[:20]


def followups_due(rows, status_col=1, nad_col=2, name_col=3, co_col=5):
    due = []
    for r in rows:
        if len(r) <= nad_col:
            continue
        nad = r[nad_col].strip()
        if nad and overdue(nad) and r[status_col] in STAGE_PRIORITY:
            due.append((r[name_col], r[co_col] if len(r) > co_col else "", nad, r[status_col]))
    return due


def stage3_no_intro(rows, status_col=1, name_col=3, co_col=5):
    return [(r[name_col], r[co_col] if len(r) > co_col else "")
            for r in rows if len(r) > status_col and r[status_col] == "3. Request Accepted"]


# ── Content helpers ────────────────────────────────────────────────────────
def get_ready_content():
    """Return list of (filename, title, meta, filepath) from 03-BRIEFS,
    excluding anything already in 04-PUBLISHED."""
    published_names = {f.stem.replace("-DRAFTS", "") for f in PUBLISHED.glob("*.md")}
    cutoff = datetime.now() - timedelta(days=5)
    results = []
    for f in sorted(BRIEFS.glob("*.md")):
        if f.name.startswith("_"):
            continue
        if "DRAFTS" in f.name:
            continue
        stem = f.stem
        if any(stem in p or p in stem for p in published_names):
            continue
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        if mtime < cutoff:
            continue
        text = f.read_text(errors="ignore")

        # Strip YAML frontmatter for body parsing
        body = re.sub(r"^---\n.*?\n---\n?", "", text, flags=re.DOTALL).strip()

        # Platform
        platform = ""
        pm = re.search(r"\*\*Platform[:\*]+\s*(.+)", text)
        if not pm:
            pm = re.search(r"^platforms?[:\s]+(.+)", text, re.MULTILINE | re.IGNORECASE)
        if pm:
            platform = pm.group(1).strip()

        # Title from first H1
        tm = re.search(r"^#\s+(.+)", body, re.MULTILINE)
        title = tm.group(1).strip() if tm else stem

        # Hashtags from body
        hashtags = re.findall(r"(?<!\w)#[A-Za-z][A-Za-z0-9_]+", body)
        hashtags = list(dict.fromkeys(hashtags))[:8]  # dedupe, cap at 8

        # Word count (body only)
        word_count = len(body.split())

        # Last modified
        last_mod = mtime.strftime("%-d %b %Y")

        # First real sentence: skip headers, bold labels, blank lines
        first_line = ""
        for line in body.split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.startswith("#") or line.startswith("**") or line.startswith("---"):
                continue
            if re.match(r"^[\*_\-]+$", line):
                continue
            first_line = line[:280]
            break

        meta = {
            "platform": platform,
            "hashtags": hashtags,
            "word_count": word_count,
            "last_mod": last_mod,
            "first_line": first_line,
        }
        results.append((f.name, title, meta, f))
    return results


PLATFORM_URL_FIELD = {
    "linkedin":          "LinkedIn URL",
    "linkedin-personal": "LinkedIn URL",
    "linkedin personal": "LinkedIn URL",
    "x":                 "X URL",
    "twitter":           "X URL",
    "x thread":          "X URL",
    "substack":          "Substack URL",
    "linkedin company":  "LinkedIn Company URL",
    "instagram":         "Instagram URL",
    "company blog":      "Blog URL",
}


def promote_ready_to_publish():
    """Move any 03-BRIEFS files with ready_to_publish: true to 04-PUBLISHED."""
    moved = []
    for f in BRIEFS.glob("*.md"):
        text = f.read_text(errors="ignore")
        if not re.search(r"^ready_to_publish:\s*true", text, re.MULTILINE | re.IGNORECASE):
            continue
        dest = PUBLISHED / f.name

        # Extract platforms from frontmatter to generate per-platform URL fields
        pm = re.search(r"^platforms?:\s*\[?(.+?)\]?$", text, re.MULTILINE | re.IGNORECASE)
        platform_url_fields = ""
        if pm:
            raw = pm.group(1)
            platforms = [p.strip().strip("\"'") for p in re.split(r"[,;]", raw) if p.strip()]
            for p in platforms:
                field_name = PLATFORM_URL_FIELD.get(p.lower(), f"{p.title()} URL")
                platform_url_fields += f"{field_name}: \n"

        frontmatter_addition = (
            "published: false\n"
            "published_date: \n"
            "published_time: \n"
            f"{platform_url_fields}"
            "platforms_published: []\n"
            "impressions: \n"
            "reads: \n"
            "replies: \n"
            "engagements: \n"
        )
        if text.startswith("---"):
            new_text = text.replace("---\n", f"---\n{frontmatter_addition}", 1)
        else:
            new_text = f"---\n{frontmatter_addition}---\n\n" + text
        dest.write_text(new_text)
        f.unlink()
        moved.append(f.name)
    return moved


def inject_briefs_frontmatter():
    """Add ready_to_publish: false to any 03-BRIEFS .md without it."""
    for f in BRIEFS.glob("*.md"):
        if f.name.startswith("_"):
            continue
        text = f.read_text(errors="ignore")
        if "ready_to_publish:" in text:
            continue
        if text.startswith("---"):
            new_text = text.replace("---\n", "---\nready_to_publish: false\n", 1)
        else:
            new_text = f"---\nready_to_publish: false\n---\n\n" + text
        f.write_text(new_text)


# ── HTML builders ──────────────────────────────────────────────────────────
def pct_bar(n, total, width=20):
    if total == 0:
        return "░" * width
    filled = round(n / total * width)
    return "█" * filled + "░" * (width - filled)


def html_pipeline_table(otc_counts, vc_counts):
    stages = [
        ("2. Request Sent",      "Stage 2 · Req Sent"),
        ("3. Request Accepted",  "Stage 3 · Accepted ✓"),
        ("4. Intro Sent",        "Stage 4 · Intro Sent"),
        ("5. Meeting Requested", "Stage 5 · Mtg Req'd"),
    ]
    otc_total = sum(otc_counts.values())
    vc_total  = sum(vc_counts.values())
    rows_html = ""
    for stage_key, label in stages:
        o = otc_counts.get(stage_key, 0)
        v = vc_counts.get(stage_key, 0)
        o_bar = pct_bar(o, otc_total)
        v_bar = pct_bar(v, vc_total)
        rows_html += f"""
        <tr>
          <td style="padding:6px 10px;font-size:13px;color:#555">{label}</td>
          <td style="padding:6px 10px;text-align:center;font-weight:bold;color:#1a1a2e">{o}</td>
          <td style="padding:6px 10px;font-family:monospace;font-size:11px;color:#4CAF50">{o_bar}</td>
          <td style="padding:6px 10px;text-align:center;font-weight:bold;color:#1a1a2e">{v}</td>
          <td style="padding:6px 10px;font-family:monospace;font-size:11px;color:#2196F3">{v_bar}</td>
        </tr>"""
    return f"""
    <table style="width:100%;border-collapse:collapse;background:#f9f9f9;border-radius:8px;overflow:hidden">
      <thead>
        <tr style="background:#1a1a2e;color:#fff">
          <th style="padding:8px 10px;text-align:left;font-size:13px">Stage</th>
          <th style="padding:8px 10px;text-align:center;font-size:13px">OTC #</th>
          <th style="padding:8px 10px;text-align:left;font-size:13px">OTC Bar</th>
          <th style="padding:8px 10px;text-align:center;font-size:13px">VC #</th>
          <th style="padding:8px 10px;text-align:left;font-size:13px">VC Bar</th>
        </tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table>"""


def html_section(title, emoji, content_html, border_color="#1a1a2e"):
    return f"""
    <div style="margin:28px 0;padding:20px 24px;border-left:4px solid {border_color};background:#fff;border-radius:0 8px 8px 0;box-shadow:0 1px 4px rgba(0,0,0,0.06)">
      <h2 style="margin:0 0 14px 0;font-size:16px;color:#1a1a2e">{emoji} {title}</h2>
      {content_html}
    </div>"""


def obsidian_url(filepath):
    """Generate obsidian:// deep link for a vault file path."""
    rel = str(filepath).replace(str(VAULT) + "/", "")
    encoded = rel.replace(" ", "%20").replace("&", "%26")
    return f"obsidian://open?vault=JARVIS-vault&file={encoded}"


def _copy_button(text_id):
    return f"""<button onclick="(function(){{var el=document.getElementById('{text_id}');navigator.clipboard.writeText(el.innerText).then(function(){{var b=document.getElementById('cb-{text_id}');b.textContent='✅ Copied!';setTimeout(function(){{b.textContent='📋 Copy Text'}},1500)}})}})()" id="cb-{text_id}" style="background:#333;color:#fff;border:none;padding:10px 18px;border-radius:6px;font-size:13px;font-weight:bold;cursor:pointer;min-height:44px">📋 Copy Text</button>"""


def html_msg_block(rank, name, company, title, status, tier, msg, li_url="", browser=False):
    stage_color = {
        "3. Request Accepted":  "#4CAF50",
        "4. Intro Sent":        "#FF9800",
        "5. Meeting Requested": "#9C27B0",
        "2. Request Sent":      "#2196F3",
    }.get(status, "#888")
    stage_display = STAGE_LABEL.get(status, status)
    safe_msg = msg.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text_id = f"msg-{rank}"

    dm_button = ""
    if li_url:
        dm_button = f"""
        <a href="{li_url}" style="display:inline-block;background:#0A66C2;color:#fff;text-decoration:none;padding:10px 18px;border-radius:6px;font-size:13px;font-weight:bold;min-height:44px;line-height:24px">
          💬 DM Now →
        </a>"""

    copy_btn = _copy_button(text_id) if browser else ""

    return f"""
    <div style="margin:16px 0;padding:16px;background:#f8f8f8;border-radius:8px;border:1px solid #e0e0e0">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;flex-wrap:wrap;gap:8px">
        <div>
          <span style="font-weight:bold;font-size:15px;color:#1a1a2e">#{rank} — {name}</span>
          <span style="font-size:13px;color:#666"> · {company}</span>
          <div style="margin-top:3px;font-size:12px;color:#999">{title}</div>
        </div>
        <div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap">
          <span style="background:{stage_color};color:#fff;padding:4px 10px;border-radius:4px;font-size:11px;font-weight:bold">{stage_display}</span>
          <span style="background:#eee;color:#555;padding:4px 10px;border-radius:4px;font-size:11px">{tier}</span>
        </div>
      </div>
      <pre id="{text_id}" style="white-space:pre-wrap;word-wrap:break-word;font-family:inherit;font-size:13px;line-height:1.7;margin:0 0 12px 0;color:#222;background:#fff;padding:14px;border-radius:6px;border:1px solid #ddd">{safe_msg}</pre>
      <div style="display:flex;gap:10px;flex-wrap:wrap">
        {copy_btn}
        {dm_button}
      </div>
    </div>"""


def html_content_block(rank, filename, title, meta, obs_url="", browser=False, full_text=""):
    copy_src_id = f"content-full-{rank}"
    platform    = meta.get("platform", "")
    hashtags    = meta.get("hashtags", [])
    word_count  = meta.get("word_count", 0)
    last_mod    = meta.get("last_mod", "")
    first_line  = meta.get("first_line", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    hashtag_html = " ".join(
        f'<span style="background:#e8f4f8;color:#0A66C2;padding:2px 7px;border-radius:3px;font-size:11px">{h}</span>'
        for h in hashtags
    ) if hashtags else '<span style="color:#bbb;font-size:11px">no hashtags found</span>'

    obs_button = ""
    if obs_url:
        obs_button = f'<a href="{obs_url}" style="display:inline-block;background:#7C3AED;color:#fff;text-decoration:none;padding:10px 16px;border-radius:6px;font-size:12px;font-weight:bold;margin:2px">📓 Obsidian →</a>'

    # Per-platform or single copy buttons
    hidden_html  = ""
    copy_buttons = ""
    sections     = parse_platform_sections(full_text) if full_text else {}

    if sections and browser:
        for sec_label, sec_text in sections.items():
            sec_id   = re.sub(r"[^a-z0-9]", "-", f"b-{rank}-{sec_label}".lower())
            safe_sec = sec_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            style    = next(
                (v for k, v in PLATFORM_SECTION_STYLE.items() if k in sec_label.lower()),
                {"color": "#333", "label": sec_label},
            )
            hidden_html  += f'<pre id="{sec_id}" style="display:none">{safe_sec}</pre>'
            copy_buttons += (
                f'<button onclick="(function(){{var el=document.getElementById(\'{sec_id}\');'
                f'navigator.clipboard.writeText(el.innerText).then(function(){{'
                f'var b=document.getElementById(\'cb-{sec_id}\');b.textContent=\'✅ Copied!\';'
                f'setTimeout(function(){{b.textContent=\'📋 {style["label"]}\'}},1500)}})}})()" '
                f'id="cb-{sec_id}" style="background:{style["color"]};color:#fff;border:none;'
                f'padding:10px 16px;border-radius:6px;font-size:12px;font-weight:bold;'
                f'cursor:pointer;margin:2px">📋 Copy {style["label"]}</button>'
            )
    elif sections and not browser:
        for sec_label in sections:
            style = next(
                (v for k, v in PLATFORM_SECTION_STYLE.items() if k in sec_label.lower()),
                {"color": "#555", "label": sec_label},
            )
            copy_buttons += (
                f'<span style="display:inline-block;background:{style["color"]};color:#fff;'
                f'padding:8px 12px;border-radius:6px;font-size:11px;font-weight:bold;margin:2px">'
                f'📋 {style["label"]} Draft</span>'
            )
    else:
        if browser and full_text:
            safe_full    = full_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            hidden_html  = f'<pre id="{copy_src_id}" style="display:none">{safe_full}</pre>'
        copy_buttons = _copy_button(copy_src_id) if browser else ""

    platform_label = platform or ("Multi-platform" if sections else "—")

    return f"""
    <div style="margin:14px 0;padding:16px;background:#fffdf5;border-radius:8px;border:1px solid #ffe082">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;flex-wrap:wrap;gap:6px">
        <span style="font-weight:bold;font-size:14px;color:#1a1a2e">#{rank} — {title}</span>
        <span style="background:#FF9800;color:#fff;padding:4px 10px;border-radius:4px;font-size:11px;font-weight:bold">{platform_label}</span>
      </div>
      <div style="display:flex;gap:16px;align-items:center;margin-bottom:10px;flex-wrap:wrap">
        <span style="font-size:11px;color:#aaa">📁 03-BRIEFS/{filename}</span>
        <span style="font-size:11px;color:#888">🕐 {last_mod}</span>
        <span style="font-size:11px;color:#888">📝 {word_count} words</span>
      </div>
      <div style="margin-bottom:10px;display:flex;flex-wrap:wrap;gap:4px">{hashtag_html}</div>
      <p style="margin:0 0 12px 0;font-size:13px;color:#444;font-style:italic;line-height:1.6">{first_line}</p>
      {hidden_html}
      <div style="display:flex;flex-wrap:wrap;gap:4px;align-items:center">
        {copy_buttons}
        {obs_button}
      </div>
    </div>"""


# ── Main briefing builder ──────────────────────────────────────────────────
def build_briefing_html(otc_rows, vc_rows, grants, g_hdr, browser=False):
    otc_counts = pipeline_counts(otc_rows)
    vc_counts  = pipeline_counts(vc_rows)

    otc_stage3 = stage3_no_intro(otc_rows)
    vc_stage3  = stage3_no_intro(vc_rows)
    otc_fup    = followups_due(otc_rows)
    vc_fup     = followups_due(vc_rows)
    top20      = top20_messages(otc_rows)
    content    = get_ready_content()

    otc_total  = sum(otc_counts.values())
    vc_total   = sum(vc_counts.values())

    # ── Section: Pipeline snapshot ─────────────────────────────────────────
    pipeline_html = f"""
    <div style="display:flex;gap:16px;margin-bottom:16px;flex-wrap:wrap">
      <div style="flex:1;min-width:140px;padding:14px;background:#1a1a2e;border-radius:8px;text-align:center;color:#fff">
        <div style="font-size:28px;font-weight:bold">{otc_total}</div>
        <div style="font-size:12px;opacity:0.7;margin-top:4px">OTC Contacts</div>
        <div style="font-size:11px;opacity:0.5">{otc_counts.get("3. Request Accepted",0)} warm · {otc_counts.get("4. Intro Sent",0)} intros out</div>
      </div>
      <div style="flex:1;min-width:140px;padding:14px;background:#1a1a2e;border-radius:8px;text-align:center;color:#fff">
        <div style="font-size:28px;font-weight:bold">{vc_total}</div>
        <div style="font-size:12px;opacity:0.7;margin-top:4px">VC Contacts</div>
        <div style="font-size:11px;opacity:0.5">{vc_counts.get("3. Request Accepted",0)} warm · {vc_counts.get("5. Meeting Requested",0)} meetings req'd</div>
      </div>
      <div style="flex:1;min-width:140px;padding:14px;background:#4CAF50;border-radius:8px;text-align:center;color:#fff">
        <div style="font-size:28px;font-weight:bold">{len(otc_stage3) + len(vc_stage3)}</div>
        <div style="font-size:12px;opacity:0.9;margin-top:4px">Warm, No Intro Yet</div>
        <div style="font-size:11px;opacity:0.7">Send today</div>
      </div>
      <div style="flex:1;min-width:140px;padding:14px;background:#FF5722;border-radius:8px;text-align:center;color:#fff">
        <div style="font-size:28px;font-weight:bold">{len(otc_fup) + len(vc_fup)}</div>
        <div style="font-size:12px;opacity:0.9;margin-top:4px">Follow-ups Overdue</div>
        <div style="font-size:11px;opacity:0.7">Past next action date</div>
      </div>
    </div>
    """ + html_pipeline_table(otc_counts, vc_counts)

    # ── Section: Priority actions ──────────────────────────────────────────
    priority_html = ""
    if otc_stage3:
        rows_h = "".join(
            f"<tr><td style='padding:5px 8px;font-size:13px'>{n}</td><td style='padding:5px 8px;font-size:13px;color:#555'>{c}</td><td style='padding:5px 8px'><span style='background:#4CAF50;color:#fff;padding:2px 6px;border-radius:3px;font-size:11px'>Accepted ✓ — Send intro DM</span></td></tr>"
            for n, c in otc_stage3[:15]
        )
        priority_html += f"""
        <p style="font-weight:bold;margin:0 0 8px 0;color:#4CAF50">OTC — {len(otc_stage3)} accepted connections, no intro sent</p>
        <table style="width:100%;border-collapse:collapse;margin-bottom:16px">
          <tr style="background:#f0f0f0"><th style="padding:5px 8px;text-align:left;font-size:12px">Name</th><th style="padding:5px 8px;text-align:left;font-size:12px">Company</th><th style="padding:5px 8px;text-align:left;font-size:12px">Action</th></tr>
          {rows_h}
        </table>"""
    if vc_stage3:
        rows_h = "".join(
            f"<tr><td style='padding:5px 8px;font-size:13px'>{n}</td><td style='padding:5px 8px;font-size:13px;color:#555'>{c}</td></tr>"
            for n, c in vc_stage3
        )
        priority_html += f"""
        <p style="font-weight:bold;margin:0 0 8px 0;color:#2196F3">VC — {len(vc_stage3)} accepted, no intro sent</p>
        <table style="width:100%;border-collapse:collapse">
          <tr style="background:#f0f0f0"><th style="padding:5px 8px;text-align:left;font-size:12px">Name</th><th style="padding:5px 8px;text-align:left;font-size:12px">Firm</th></tr>
          {rows_h}
        </table>"""

    # ── Section: Follow-ups ────────────────────────────────────────────────
    fup_html = ""
    if otc_fup:
        rows_h = "".join(
            f"<tr><td style='padding:5px 8px;font-size:13px'>{n}</td><td style='padding:5px 8px;font-size:13px;color:#555'>{c}</td><td style='padding:5px 8px;font-size:12px;color:#FF5722'>{d}</td><td style='padding:5px 8px;font-size:12px'>{STAGE_LABEL.get(s,s)}</td></tr>"
            for n, c, d, s in otc_fup[:15]
        )
        fup_html += f"""
        <p style="font-weight:bold;margin:0 0 8px 0">OTC Follow-ups ({len(otc_fup)} overdue)</p>
        <table style="width:100%;border-collapse:collapse;margin-bottom:14px">
          <tr style="background:#f0f0f0"><th style="padding:5px 8px;text-align:left;font-size:12px">Name</th><th style="padding:5px 8px;text-align:left;font-size:12px">Company</th><th style="padding:5px 8px;text-align:left;font-size:12px">Due</th><th style="padding:5px 8px;text-align:left;font-size:12px">Stage</th></tr>
          {rows_h}
        </table>"""
    if vc_fup:
        rows_h = "".join(
            f"<tr><td style='padding:5px 8px;font-size:13px'>{n}</td><td style='padding:5px 8px;font-size:13px;color:#555'>{c}</td><td style='padding:5px 8px;font-size:12px;color:#FF5722'>{d}</td><td style='padding:5px 8px;font-size:12px'>{STAGE_LABEL.get(s,s)}</td></tr>"
            for n, c, d, s in vc_fup[:10]
        )
        fup_html += f"""
        <p style="font-weight:bold;margin:0 0 8px 0">VC Follow-ups ({len(vc_fup)} overdue)</p>
        <table style="width:100%;border-collapse:collapse">
          <tr style="background:#f0f0f0"><th style="padding:5px 8px;text-align:left;font-size:12px">Name</th><th style="padding:5px 8px;text-align:left;font-size:12px">Firm</th><th style="padding:5px 8px;text-align:left;font-size:12px">Due</th><th style="padding:5px 8px;text-align:left;font-size:12px">Stage</th></tr>
          {rows_h}
        </table>"""
    if not fup_html:
        fup_html = "<p style='color:#4CAF50'>No follow-ups overdue today.</p>"

    # ── Section: Top 20 messages ───────────────────────────────────────────
    msgs_html = ""
    for i, (score, name, company, title, status, msg, tier, li_url) in enumerate(top20, 1):
        msgs_html += html_msg_block(i, name, company, title, status, tier, msg, li_url, browser=browser)

    # ── Section: Content ───────────────────────────────────────────────────
    content_html = ""
    if content:
        for i, (fname, title, meta, fpath) in enumerate(content, 1):
            full_text = Path(fpath).read_text(errors="ignore") if browser else ""
            content_html += html_content_block(i, fname, title, meta, obsidian_url(fpath), browser=browser, full_text=full_text)
    else:
        content_html = "<p style='color:#999'>No new content drafts in 03-BRIEFS from the last 5 days.</p>"

    # ── Assemble full HTML ─────────────────────────────────────────────────
    dark_css = """
  body { background:#0d0d14 !important; color:#e0e0e0 !important; }
  .wrapper { }
  /* section cards */
  div[style*="background:#fff"] { background:#1a1a28 !important; }
  div[style*="background:#f8f8f8"] { background:#1e1e2e !important; }
  div[style*="background:#f9f9f9"] { background:#181824 !important; }
  div[style*="background:#fffdf5"] { background:#1e1c12 !important; }
  div[style*="border:1px solid #e0e0e0"] { border-color:#333 !important; }
  div[style*="border:1px solid #ffe082"] { border-color:#5a4800 !important; }
  /* pre blocks */
  pre { background:#111120 !important; border-color:#333 !important; color:#d0d0d0 !important; }
  /* tables */
  tr[style*="background:#f0f0f0"] { background:#252535 !important; }
  td, th { color:#ccc !important; }
  /* footer */
  p[style*="color:#bbb"] { color:#555 !important; }
  /* hashtag chips */
  span[style*="background:#e8f4f8"] { background:#0d2a3a !important; }
  /* meta text */
  span[style*="color:#aaa"], span[style*="color:#888"], p[style*="color:#aaa"] { color:#666 !important; }
  p[style*="color:#444"] { color:#aaa !important; }
  /* copy button */
  button { background:#2a2a3e !important; border:1px solid #444 !important; }
  button:hover { background:#3a3a55 !important; }
""" if browser else ""

    extra_head = f"<style>{dark_css}</style>" if browser else ""

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background:#f4f4f7; margin:0; padding:0; }}
  .wrapper {{ max-width:720px; margin:0 auto; padding:24px 16px; }}
  .header {{ background:#1a1a2e; color:#fff; padding:24px 28px; border-radius:10px; margin-bottom:24px; }}
  .header h1 {{ margin:0 0 4px 0; font-size:22px; }}
  .header p  {{ margin:0; font-size:13px; opacity:0.6; }}
</style>
{extra_head}
</head>
<body><div class="wrapper">

  <div class="header">
    <h1>BizBot Brief</h1>
    <p>BizBot · {DISPLAY_DATE} · OTC-first mode</p>
  </div>

  {html_section("Pipeline Snapshot", "📊", pipeline_html, "#1a1a2e")}
  {html_section("Priority Actions — Send Today", "🔥", priority_html, "#4CAF50")}
  {html_section("Follow-ups Overdue", "🔁", fup_html, "#FF5722")}
  {html_section("Top 20 Messages — Copy & Paste Ready", "💬", msgs_html, "#9C27B0")}
  {html_section("Content Ready to Post", "📝", content_html, "#FF9800")}

  <p style="text-align:center;font-size:11px;color:#bbb;margin-top:32px">BizBot · {TODAY_STR} · Full brief saved to JARVIS vault 00-INBOX/_{{TODAY_STR}}-daily-brief.md</p>
</div></body></html>"""

    return html


# ── Gmail send ─────────────────────────────────────────────────────────────
def send_email(service, html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"BizBot Brief — {DISPLAY_DATE}"
    msg["From"]    = TO_EMAIL
    msg["To"]      = TO_EMAIL
    msg.attach(MIMEText(html_body, "html"))
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    print(f"✅ Brief sent to {TO_EMAIL}")


# ── Sent-today check ───────────────────────────────────────────────────────
SENT_FLAG = BOT_DIR / "output" / f".brief-sent-{TODAY_STR}"

def already_sent():
    return SENT_FLAG.exists()

def mark_sent():
    SENT_FLAG.parent.mkdir(parents=True, exist_ok=True)
    SENT_FLAG.touch()


# ── Entry point ────────────────────────────────────────────────────────────
def main(force=False):
    print(f"BizBot briefing — {TODAY_STR}")

    if already_sent() and not force:
        print(f"⏭  Brief already sent today ({TODAY_STR}). Skipping cron run.")
        print("   Run with --force to resend.")
        return

    # Auth
    creds   = get_credentials()
    gc      = gspread.authorize(creds)
    gmail   = build("gmail", "v1", credentials=creds)

    # Pre-briefing: inject frontmatter into 03-BRIEFS, promote ready files
    inject_briefs_frontmatter()
    moved = promote_ready_to_publish()
    if moved:
        print(f"  Promoted to 04-PUBLISHED: {moved}")

    # Read CRM
    otc_rows, vc_rows, grants, g_hdr = read_crm(gc)

    # Build both versions
    email_html   = build_briefing_html(otc_rows, vc_rows, grants, g_hdr, browser=False)
    browser_html = build_briefing_html(otc_rows, vc_rows, grants, g_hdr, browser=True)

    # Save interactive browser file and open it
    browser_path = BOT_DIR / "output" / f"brief-{TODAY_STR}.html"
    browser_path.parent.mkdir(parents=True, exist_ok=True)
    browser_path.write_text(browser_html)
    import subprocess
    subprocess.Popen(["open", str(browser_path)])
    print(f"🌐 Browser brief opened: {browser_path}")

    # Save markdown brief to JARVIS inbox
    brief_path = INBOX / f"_{TODAY_STR}-daily-brief.md"
    brief_path.write_text(
        f"# BizBot Brief — {DISPLAY_DATE}\n\n"
        f"*Full HTML brief sent to {TO_EMAIL}*\n\n"
        f"See email for pipeline snapshot, top 20 messages, content drafts, and follow-up actions.\n"
    )

    # Send email + mark sent
    send_email(gmail, email_html)
    mark_sent()


if __name__ == "__main__":
    import sys
    force = "--force" in sys.argv
    main(force=force)
