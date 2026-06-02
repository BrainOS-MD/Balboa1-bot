#!/usr/bin/env python3
"""
JARVIS Email Notifier — Full Dashboard
Sends a rich HTML email + dark-mode browser file after any JARVIS skill run.
Triggered by: process-inbox, auto-research, think-deep, weekly-digest

Usage:
  python send_jarvis_email.py --file /path/to/_2026-06-01-inbox-processed.md
"""

import os, re, sys, base64, subprocess
from pathlib import Path
from datetime import date, datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ── Paths ──────────────────────────────────────────────────────────────────
BOT_DIR    = Path(__file__).parent.parent
CREDS_PATH = BOT_DIR / "credentials" / "oauth_credentials.json"
TOKEN_PATH = BOT_DIR / "credentials" / "authorized_user.json"
VAULT      = Path.home() / "Library/Mobile Documents/iCloud~md~obsidian/Documents/JARVIS-vault"
INBOX      = VAULT / "00-INBOX"
CAPTURES   = VAULT / "01-CAPTURES"
CONNECTS   = VAULT / "02-CONNECTIONS"
BRIEFS     = VAULT / "03-BRIEFS"
PUBLISHED  = VAULT / "04-PUBLISHED"
INDEX      = VAULT / "05-CLAUDE" / "vault-index.md"
TO_EMAIL   = "nick.grosz@gmail.com"
SCOPES     = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose",
]

TODAY        = date.today()
TODAY_STR    = TODAY.strftime("%Y-%m-%d")
DISPLAY_DATE = TODAY.strftime("%B %-d, %Y")
NOW          = datetime.now()

# ── Platform config ────────────────────────────────────────────────────────
PLATFORM_CONFIG = {
    "linkedin":          {"label": "LinkedIn",    "color": "#0A66C2", "url": "https://www.linkedin.com/feed/"},
    "linkedin-personal": {"label": "LinkedIn",    "color": "#0A66C2", "url": "https://www.linkedin.com/feed/"},
    "linkedin personal": {"label": "LinkedIn",    "color": "#0A66C2", "url": "https://www.linkedin.com/feed/"},
    "x":                 {"label": "X",           "color": "#000000", "url": "https://x.com/compose/post"},
    "twitter":           {"label": "X",           "color": "#000000", "url": "https://x.com/compose/post"},
    "x thread":          {"label": "X Thread",    "color": "#000000", "url": "https://x.com/compose/post"},
    "substack":          {"label": "Substack",    "color": "#FF6719", "url": "https://substack.com/"},
    "linkedin company":  {"label": "LinkedIn Co", "color": "#004182", "url": "https://www.linkedin.com/"},
    "instagram":         {"label": "Instagram",   "color": "#E1306C", "url": "https://www.instagram.com/"},
    "company blog":      {"label": "Blog",        "color": "#6B7280", "url": "#"},
}

# Maps frontmatter platform values to the URL field name injected on promotion
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

NOTEBOOKLM_URL = "https://notebooklm.google.com"


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


# ── Vault helpers ───────────────────────────────────────────────────────────
def obsidian_url(filepath):
    rel = str(filepath).replace(str(VAULT) + "/", "")
    encoded = rel.replace(" ", "%20").replace("&", "%26")
    return f"obsidian://open?vault=JARVIS-vault&file={encoded}"


def read_frontmatter(text):
    """Parse YAML frontmatter. Keys may contain spaces (e.g. 'LinkedIn URL')."""
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).split("\n"):
        kv = re.match(r"^([A-Za-z][A-Za-z0-9 _-]*):\s*(.*)", line)
        if kv:
            fm[kv.group(1).strip()] = kv.group(2).strip()
    return fm


def strip_frontmatter(text):
    return re.sub(r"^---\n.*?\n---\n?", "", text, flags=re.DOTALL).strip()


# Known platform section headers as they appear in DRAFTS files
_PLATFORM_HEADERS = [
    "X Thread", "Twitter Thread", "Twitter",
    "LinkedIn Personal", "LinkedIn Company", "LinkedIn",
    "Substack", "Instagram", "Company Blog",
]

def parse_platform_sections(body):
    """
    Split a DRAFTS file body by ## Platform headers.
    Returns OrderedDict {header_label: content_text} for each platform section found.
    Non-platform H2s (e.g. ## Compliance Checklist) are excluded.
    """
    parts = re.split(r"^## (.+)$", body, flags=re.MULTILINE)
    # parts = [pre, header1, content1, header2, content2, ...]
    sections = {}
    for i in range(1, len(parts), 2):
        header  = parts[i].strip()
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        # Only keep recognised platform sections
        if any(ph.lower() in header.lower() for ph in _PLATFORM_HEADERS):
            sections[header] = content
    return sections


PLATFORM_SECTION_STYLE = {
    "x thread":        {"color": "#000000", "label": "X Thread",       "compose": "https://x.com/compose/post"},
    "twitter":         {"color": "#000000", "label": "X Thread",       "compose": "https://x.com/compose/post"},
    "linkedin personal":{"color":"#0A66C2", "label": "LinkedIn",       "compose": "https://www.linkedin.com/feed/"},
    "linkedin company":{"color": "#004182", "label": "LinkedIn Co",    "compose": "https://www.linkedin.com/"},
    "linkedin":        {"color": "#0A66C2", "label": "LinkedIn",       "compose": "https://www.linkedin.com/feed/"},
    "substack":        {"color": "#FF6719", "label": "Substack",       "compose": "https://substack.com/"},
    "instagram":       {"color": "#E1306C", "label": "Instagram",      "compose": "https://www.instagram.com/"},
    "company blog":    {"color": "#6B7280", "label": "Blog",           "compose": "#"},
}


def files_modified_since(directory, hours=24):
    cutoff = NOW - timedelta(hours=hours)
    results = []
    for f in sorted(Path(directory).rglob("*.md")):
        if f.name.startswith("."):
            continue
        try:
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if mtime >= cutoff:
                results.append((mtime, f))
        except Exception:
            pass
    return sorted(results, key=lambda x: x[0], reverse=True)


def scan_vault_activity():
    folder_map = {
        "00-INBOX":       INBOX,
        "01-CAPTURES":    CAPTURES,
        "02-CONNECTIONS": CONNECTS,
        "03-BRIEFS":      BRIEFS,
        "04-PUBLISHED":   PUBLISHED,
    }
    activity = {}
    for label, path in folder_map.items():
        if path.exists():
            hits = files_modified_since(path, hours=24)
            if hits:
                activity[label] = hits
    return activity


def get_ready_to_publish():
    """03-BRIEFS files with ready_to_publish: true."""
    results = []
    for f in sorted(BRIEFS.glob("*.md")):
        if f.name.startswith("_"):
            continue
        text = f.read_text(errors="ignore")
        fm   = read_frontmatter(text)
        if fm.get("ready_to_publish", "").lower() != "true":
            continue
        body = strip_frontmatter(text)
        tm   = re.search(r"^#\s+(.+)", body, re.MULTILINE)
        title = tm.group(1).strip() if tm else f.stem
        raw_plat = fm.get("platforms", fm.get("platform", ""))
        platforms = [p.strip().strip("[]\"'") for p in re.split(r"[,;]", raw_plat) if p.strip()]
        hm   = re.search(r"(?:Hook\s*1|Hooks?\s*\(ranked\)[^\n]*\n+(?:\d+\.\s*)?)([^\n]+)", body)
        hook = hm.group(1).strip()[:220] if hm else ""
        hashtags = list(dict.fromkeys(re.findall(r"(?<!\w)#[A-Za-z][A-Za-z0-9_]+", body)))[:6]
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        results.append({
            "path":             f,
            "filename":         f.name,
            "title":            title,
            "platforms":        platforms,
            "hook":             hook,
            "word_count":       len(body.split()),
            "hashtags":         hashtags,
            "last_mod":         mtime.strftime("%-d %b %Y"),
            "full_text":        body,
            "obs_url":          obsidian_url(f),
            "platform_sections": parse_platform_sections(body),
        })
    return results


def get_new_briefs():
    """03-BRIEFS files created or modified in the last 24h (not ready_to_publish yet)."""
    cutoff  = NOW - timedelta(hours=24)
    results = []
    for f in sorted(BRIEFS.glob("*.md")):
        if f.name.startswith("_"):
            continue
        try:
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
        except Exception:
            continue
        if mtime < cutoff:
            continue
        text = f.read_text(errors="ignore")
        fm   = read_frontmatter(text)
        if fm.get("ready_to_publish", "").lower() == "true":
            continue  # already in ready-to-publish section
        body  = strip_frontmatter(text)
        tm    = re.search(r"^#\s+(.+)", body, re.MULTILINE)
        title = tm.group(1).strip() if tm else f.stem
        raw_plat = fm.get("platforms", fm.get("platform", ""))
        platforms = [p.strip().strip("[]\"'") for p in re.split(r"[,;]", raw_plat) if p.strip()]
        hm    = re.search(r"(?:Hook\s*1|Hooks?\s*\(ranked\)[^\n]*\n+(?:\d+\.\s*)?)([^\n]+)", body)
        hook  = hm.group(1).strip()[:220] if hm else ""
        hashtags = list(dict.fromkeys(re.findall(r"(?<!\w)#[A-Za-z][A-Za-z0-9_]+", body)))[:6]
        one_thing = ""
        ot = re.search(r"(?:One Thing|ONE THING)[^\n]*\n+([^\n#]+)", body)
        if ot:
            one_thing = ot.group(1).strip()[:200]
        results.append({
            "path":              f,
            "filename":          f.name,
            "title":             title,
            "platforms":         platforms,
            "hook":              hook,
            "one_thing":         one_thing,
            "hashtags":          hashtags,
            "last_mod":          mtime.strftime("%-d %b %Y %-I:%M %p"),
            "full_text":         body,
            "obs_url":           obsidian_url(f),
            "platform_sections": parse_platform_sections(body),
        })
    return results


def get_time_sensitive():
    if not INDEX.exists():
        return []
    lines = INDEX.read_text(errors="ignore").split("\n")
    results = []
    for line in lines:
        if "time-sensitive" not in line.lower():
            continue
        cols = [c.strip() for c in line.split("|") if c.strip()]
        if len(cols) >= 4:
            results.append(cols)
    return results[:10]


def get_published_analytics():
    results = []
    for f in sorted(PUBLISHED.glob("*.md"), reverse=True)[:12]:
        text = f.read_text(errors="ignore")
        fm   = read_frontmatter(text)
        if not fm:
            continue
        body  = strip_frontmatter(text)
        tm    = re.search(r"^#\s+(.+)", body, re.MULTILINE)
        title = tm.group(1).strip() if tm else f.stem
        # Build per-platform links from individual URL fields
        raw_plat = fm.get("platforms_published", fm.get("platforms", fm.get("platform", "")))
        platforms_list = [p.strip().strip("[]\"'") for p in re.split(r"[,;]", raw_plat) if p.strip()]
        platform_links = []
        for p in platforms_list:
            url_field = PLATFORM_URL_FIELD.get(p.lower(), f"{p.title()} URL")
            url = fm.get(url_field, "").strip()
            if url:
                platform_links.append({"label": p.title(), "url": url})
            else:
                platform_links.append({"label": p.title(), "url": ""})
        results.append({
            "filename":       f.name,
            "title":          title,
            "platform_links": platform_links,
            "pub_date":       fm.get("published_date", "—"),
            "impressions":    fm.get("impressions", "—"),
            "reads":          fm.get("reads", "—"),
            "replies":        fm.get("replies", "—"),
            "engagements":    fm.get("engagements", "—"),
            "published":      fm.get("published", "false"),
            "obs_url":        obsidian_url(f),
        })
    return results


# ── Report type ─────────────────────────────────────────────────────────────
TYPE_META = {
    "inbox":   {"label": "Inbox Processed",    "emoji": "📥", "accent": "#4CAF50", "prefix": "JARVIS Inbox"},
    "research":{"label": "Research Complete",  "emoji": "🔍", "accent": "#2196F3", "prefix": "JARVIS Research"},
    "brief":   {"label": "Brief Generated",    "emoji": "📋", "accent": "#9C27B0", "prefix": "JARVIS Brief"},
    "think":   {"label": "Think-Deep Complete","emoji": "🧠", "accent": "#FF9800", "prefix": "JARVIS Think-Deep"},
    "digest":  {"label": "Weekly Digest",      "emoji": "📊", "accent": "#00BCD4", "prefix": "JARVIS Digest"},
    "jarvis":  {"label": "JARVIS Report",      "emoji": "🤖", "accent": "#9C27B0", "prefix": "JARVIS"},
}


def detect_type(filename):
    name = Path(filename).name.lower()
    if "inbox" in name or "processed" in name: return "inbox"
    if "research" in name:                      return "research"
    if "brief" in name:                         return "brief"
    if "think" in name or "deep" in name:       return "think"
    if "digest" in name or "weekly" in name:    return "digest"
    return "jarvis"


# ── Button primitives ────────────────────────────────────────────────────────
def btn_link(label, url, color, text_color="#fff"):
    return (
        f'<a href="{url}" style="display:inline-block;background:{color};color:{text_color};'
        f'text-decoration:none;padding:10px 16px;border-radius:6px;font-size:12px;'
        f'font-weight:bold;margin:3px 4px 3px 0">{label}</a>'
    )


def btn_copy(text_id, label="📋 Copy", browser=False):
    if not browser:
        return ""
    return (
        f'<button onclick="(function(){{var el=document.getElementById(\'{text_id}\');'
        f'navigator.clipboard.writeText(el.innerText).then(function(){{'
        f'var b=document.getElementById(\'cb-{text_id}\');b.textContent=\'✅ Copied!\';'
        f'setTimeout(function(){{b.textContent=\'{label}\'}},1500)}})}})()" '
        f'id="cb-{text_id}" style="background:#2a2a3e;color:#fff;border:1px solid #444;'
        f'padding:10px 16px;border-radius:6px;font-size:12px;font-weight:bold;'
        f'cursor:pointer;margin:3px 4px 3px 0">{label}</button>'
    )


def btn_generate_content(title, idx, browser=False):
    """Copy-to-clipboard button with the Claude Code write command."""
    cmd    = f"write the brief for {title}"
    btn_id = f"gc-{idx}"
    if browser:
        return (
            f'<pre id="{btn_id}" style="display:none">{cmd}</pre>'
            f'<button onclick="(function(){{navigator.clipboard.writeText(document.getElementById(\'{btn_id}\').innerText).then(function(){{'
            f'var b=document.getElementById(\'gcb-{btn_id}\');b.textContent=\'✅ Command Copied!\';'
            f'setTimeout(function(){{b.textContent=\'⚡ Copy: Generate Content\'}},2000)}})}})()" '
            f'id="gcb-{btn_id}" style="background:#0d2a1a;color:#4CAF50;border:1px solid #4CAF50;'
            f'padding:10px 16px;border-radius:6px;font-size:12px;font-weight:bold;cursor:pointer;margin:3px 4px 3px 0">'
            f'⚡ Copy: Generate Content</button>'
        )
    # Email: static code label
    return (
        f'<span style="display:inline-block;background:#0d2a1a;color:#4CAF50;border:1px solid #4CAF50;'
        f'padding:8px 14px;border-radius:6px;font-size:11px;font-weight:bold;margin:3px 4px 3px 0">'
        f'⚡ Claude Code: write the brief for {title}</span>'
    )


def btn_notebooklm():
    return btn_link("🎧 NotebookLM →", NOTEBOOKLM_URL, "#1A73E8")


def btn_obsidian(url):
    return btn_link("📓 Obsidian →", url, "#7C3AED")


def platform_compose_buttons(platforms):
    html = ""
    for p in platforms:
        cfg = PLATFORM_CONFIG.get(p.lower().strip())
        if cfg:
            html += btn_link(f"{cfg['label']} →", cfg["url"], cfg["color"])
    return html


# ── Section wrapper ──────────────────────────────────────────────────────────
def section(title, emoji, content_html, accent="#333", browser=False):
    bg = "#1a1a28" if browser else "#ffffff"
    return f"""
<div style="margin:20px 0;background:{bg};border-radius:10px;overflow:hidden;box-shadow:0 1px 6px rgba(0,0,0,0.15)">
  <div style="background:{accent};padding:11px 20px">
    <span style="font-weight:bold;font-size:14px;color:#fff">{emoji} {title}</span>
  </div>
  <div style="padding:18px 22px">{content_html}</div>
</div>"""


# ── Content card (shared by ready-to-publish and new briefs) ─────────────────
def content_card(item, idx, card_type="rtp", browser=False):
    """
    card_type: 'rtp' (ready-to-publish) or 'brief' (newly generated)
    """
    text_id   = f"{card_type}-{idx}"
    is_rtp    = card_type == "rtp"
    accent    = "#9C27B0" if is_rtp else "#2196F3"
    card_bg   = ("#1e1e2e" if is_rtp else "#0d1a2e") if browser else ("#f9f6ff" if is_rtp else "#f0f6ff")
    title_col = "#e0e0e0" if browser else "#1a1a2e"
    sub_col   = "#888"    if browser else "#666"
    hook_bg   = "#111120" if browser else "#f5f5f5"
    hook_col  = "#ccc"    if browser else "#444"

    # Hashtags
    hashtag_html = " ".join(
        f'<span style="background:{"#0d2a3a" if browser else "#e8f4f8"};'
        f'color:{"#58a6ff" if browser else "#0A66C2"};padding:2px 7px;border-radius:3px;font-size:11px">{h}</span>'
        for h in item.get("hashtags", [])
    )

    # Hook block
    hook_html = ""
    if item.get("hook"):
        safe_hook = item["hook"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        hook_html = f'<p style="font-style:italic;font-size:13px;color:{hook_col};background:{hook_bg};padding:10px 14px;border-radius:6px;margin:10px 0 0 0">&ldquo;{safe_hook}&rdquo;</p>'

    # One Thing block (brief only)
    one_thing_html = ""
    if not is_rtp and item.get("one_thing"):
        safe_ot = item["one_thing"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        ot_col = "#aaa" if browser else "#555"
        one_thing_html = f'<p style="font-size:12px;color:{ot_col};margin:8px 0 0 0"><strong>One Thing:</strong> {safe_ot}</p>'

    # Per-platform sections (DRAFTS files) vs single full-text copy
    platform_sections = item.get("platform_sections", {})
    hidden      = ""
    copy_btns   = ""

    if platform_sections and browser:
        # One hidden <pre> + copy button per platform section
        for sec_label, sec_text in platform_sections.items():
            sec_id   = re.sub(r"[^a-z0-9]", "-", f"{text_id}-{sec_label}".lower())
            safe_sec = sec_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            style    = next(
                (v for k, v in PLATFORM_SECTION_STYLE.items() if k in sec_label.lower()),
                {"color": "#333", "label": sec_label, "compose": "#"},
            )
            hidden    += f'<pre id="{sec_id}" style="display:none">{safe_sec}</pre>'
            copy_btns += (
                f'<button onclick="(function(){{var el=document.getElementById(\'{sec_id}\');'
                f'navigator.clipboard.writeText(el.innerText).then(function(){{'
                f'var b=document.getElementById(\'cb-{sec_id}\');b.textContent=\'✅ Copied!\';'
                f'setTimeout(function(){{b.textContent=\'📋 {style["label"]}\'}},1500)}})}})()" '
                f'id="cb-{sec_id}" style="background:{style["color"]};color:#fff;border:none;'
                f'padding:10px 16px;border-radius:6px;font-size:12px;font-weight:bold;'
                f'cursor:pointer;margin:3px 4px 3px 0">📋 Copy {style["label"]}</button>'
            )
    elif platform_sections and not browser:
        # Email: one static label per platform (no JS)
        for sec_label in platform_sections:
            style = next(
                (v for k, v in PLATFORM_SECTION_STYLE.items() if k in sec_label.lower()),
                {"color": "#333", "label": sec_label},
            )
            copy_btns += (
                f'<span style="display:inline-block;background:{style["color"]};color:#fff;'
                f'padding:8px 14px;border-radius:6px;font-size:11px;font-weight:bold;margin:3px 4px 3px 0">'
                f'📋 {style["label"]} Draft</span>'
            )
    else:
        # Single-platform or brief file — one copy button
        if browser and item.get("full_text"):
            safe_full  = item["full_text"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            hidden     = f'<pre id="{text_id}" style="display:none">{safe_full}</pre>'
        copy_btns = btn_copy(text_id, browser=browser)

    # Compose buttons (one per platform, links to post composer)
    if platform_sections:
        platform_compose = ""
        for sec_label in platform_sections:
            style = next(
                (v for k, v in PLATFORM_SECTION_STYLE.items() if k in sec_label.lower()),
                {"color": "#555", "label": sec_label, "compose": "#"},
            )
            platform_compose += btn_link(f"{style['label']} →", style["compose"], style["color"])
    else:
        platform_compose = platform_compose_buttons(item.get("platforms", []))

    # Button row
    obs_btn = btn_obsidian(item["obs_url"])
    nlm_btn = btn_notebooklm()

    if is_rtp:
        action_btns = f"{copy_btns}{nlm_btn}{platform_compose}{obs_btn}"
    else:
        gen_btn     = btn_generate_content(item["title"], idx, browser)
        action_btns = f"{copy_btns}{nlm_btn}{gen_btn}{platform_compose}{obs_btn}"

    return f"""
<div style="margin:14px 0;padding:18px;background:{card_bg};border-radius:8px;border-left:4px solid {accent}">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:6px;margin-bottom:6px">
    <span style="font-weight:bold;font-size:15px;color:{title_col}">{item['title']}</span>
    <span style="font-size:11px;color:{sub_col}">🕐 {item.get('last_mod','')}{' · 📝 '+str(item.get('word_count',''))+' words' if item.get('word_count') else ''}</span>
  </div>
  {f'<div style="margin-bottom:8px;display:flex;flex-wrap:wrap;gap:4px">{hashtag_html}</div>' if hashtag_html else ''}
  {hook_html}
  {one_thing_html}
  {hidden}
  <div style="display:flex;flex-wrap:wrap;align-items:center;margin-top:12px">
    {action_btns}
  </div>
</div>"""


# ── Section builders ─────────────────────────────────────────────────────────
def build_vault_activity_html(activity, browser=False):
    if not activity:
        col = "#666" if browser else "#999"
        return f'<p style="color:{col};font-size:13px">No vault files modified in the last 24 hours.</p>'

    icons = {"00-INBOX":"📥","01-CAPTURES":"🗂","02-CONNECTIONS":"🔗","03-BRIEFS":"📋","04-PUBLISHED":"✅"}
    html  = ""
    col   = "#e0e0e0" if browser else "#1a1a2e"
    sub   = "#888"    if browser else "#666"

    for folder, files in activity.items():
        icon = icons.get(folder, "📁")
        html += f'<p style="font-weight:bold;font-size:13px;color:{col};margin:14px 0 5px 0">{icon} {folder} — {len(files)} file{"s" if len(files)!=1 else ""}</p>'
        html += '<ul style="margin:0 0 8px 20px;padding:0">'
        for mtime, f in files[:8]:
            ots  = obsidian_url(f)
            time = mtime.strftime("%-I:%M %p")
            html += f'<li style="margin-bottom:5px;font-size:13px"><a href="{ots}" style="color:#7C3AED;text-decoration:none">{f.name}</a> <span style="font-size:11px;color:{sub}">— {time}</span></li>'
        html += "</ul>"
    return html


def build_ready_to_publish_html(items, browser=False):
    if not items:
        col = "#666" if browser else "#999"
        return f'<p style="color:{col};font-size:13px">No content marked ready_to_publish: true in 03-BRIEFS.</p>'
    return "".join(content_card(item, i, "rtp", browser) for i, item in enumerate(items, 1))


def build_new_briefs_html(items, browser=False):
    if not items:
        col = "#666" if browser else "#999"
        return f'<p style="color:{col};font-size:13px">No new briefs generated in the last 24 hours.</p>'
    return "".join(content_card(item, i, "brief", browser) for i, item in enumerate(items, 1))


def _ts_obsidian_url(type_v, slug):
    """Reconstruct Obsidian URL from vault-index type + slug columns."""
    type_map = {
        "observation":  "observations",
        "observations": "observations",
        "reaction":     "reactions",
        "reactions":    "reactions",
        "pattern":      "patterns",
        "patterns":     "patterns",
        "question":     "questions",
        "questions":    "questions",
        "number":       "numbers",
        "numbers":      "numbers",
        "connection":   "",   # 02-CONNECTIONS root
        "connections":  "",
    }
    folder = type_map.get(type_v.lower().strip(), type_v.lower())
    if folder:
        candidate = CAPTURES / folder / f"{slug}.md"
        if not candidate.exists():
            # try without subfolder
            candidate = CAPTURES / f"{slug}.md"
    else:
        candidate = CONNECTS / f"{slug}.md"

    if candidate.exists():
        return obsidian_url(candidate)
    # fallback: search across all captures subfolders
    for f in CAPTURES.rglob(f"{slug}.md"):
        return obsidian_url(f)
    return ""


def build_time_sensitive_html(entries, browser=False):
    if not entries:
        col = "#666" if browser else "#999"
        return f'<p style="color:{col};font-size:13px">No time-sensitive captures in vault index.</p>'

    col = "#e0e0e0" if browser else "#1a1a2e"
    sub = "#888"    if browser else "#666"
    hdr = "#252520" if browser else "#fff8e1"
    lnk = "#7C3AED"
    html  = '<table style="width:100%;border-collapse:collapse;font-size:13px">'
    html += f'<tr style="background:{hdr}"><th style="padding:6px 10px;text-align:left;color:{sub}">Date</th><th style="padding:6px 10px;text-align:left;color:{sub}">Type</th><th style="padding:6px 10px;text-align:left;color:{col}">Summary</th><th style="padding:6px 10px;text-align:left;color:{sub}">Tags</th></tr>'
    for cols in entries:
        date_v = cols[0] if len(cols) > 0 else "—"
        type_v = cols[1] if len(cols) > 1 else "—"
        slug   = cols[2] if len(cols) > 2 else ""
        tags   = cols[3] if len(cols) > 3 else "—"
        summ   = cols[-1] if len(cols) > 4 else (slug or "—")
        bd     = "#333" if browser else "#eee"
        obs    = _ts_obsidian_url(type_v, slug)
        summ_html = (
            f'<a href="{obs}" style="color:{lnk};text-decoration:none;font-weight:500">{summ}</a>'
            if obs else summ
        )
        html += f'<tr style="border-top:1px solid {bd}"><td style="padding:5px 10px;color:{sub};font-size:12px;white-space:nowrap">{date_v}</td><td style="padding:5px 10px;color:{sub};font-size:12px">{type_v}</td><td style="padding:5px 10px;color:{col}">{summ_html}</td><td style="padding:5px 10px;font-size:11px;color:#888">{tags}</td></tr>'
    html += "</table>"
    return html


def build_analytics_html(items, browser=False):
    if not items:
        col = "#666" if browser else "#999"
        return f'<p style="color:{col};font-size:13px">No published notes found in 04-PUBLISHED.</p>'

    sub = "#888"    if browser else "#666"
    col = "#e0e0e0" if browser else "#1a1a2e"
    hdr = "#252535" if browser else "#f0f0f0"
    bd  = "#333"    if browser else "#eee"
    html  = '<table style="width:100%;border-collapse:collapse;font-size:12px">'
    html += f'<tr style="background:{hdr}"><th style="padding:7px 10px;text-align:left;color:{sub}">Title</th><th style="padding:7px 10px;text-align:left;color:{sub}">Platform</th><th style="padding:7px 10px;text-align:center;color:{sub}">Date</th><th style="padding:7px 10px;text-align:center;color:{sub}">Impr.</th><th style="padding:7px 10px;text-align:center;color:{sub}">Reads</th><th style="padding:7px 10px;text-align:center;color:{sub}">Replies</th><th style="padding:7px 10px;text-align:center;color:{sub}">Eng.</th><th style="padding:7px 10px;text-align:left;color:{sub}">Open</th></tr>'

    for item in items:
        # Platform column: linked if URL exists, plain text if not
        platform_html = ""
        for pl in item["platform_links"]:
            if pl["url"]:
                platform_html += f'<a href="{pl["url"]}" style="color:#0A66C2;font-size:12px;display:block">{pl["label"]}</a>'
            else:
                platform_html += f'<span style="color:{sub};font-size:12px;display:block">{pl["label"]}</span>'
        if not platform_html:
            platform_html = f'<span style="color:{sub}">—</span>'

        obs_link = f'<a href="{item["obs_url"]}" style="color:#7C3AED;font-size:11px">Obsidian</a>'
        html += (
            f'<tr style="border-top:1px solid {bd}">'
            f'<td style="padding:6px 10px;color:{col}">{item["title"]}</td>'
            f'<td style="padding:6px 10px">{platform_html}</td>'
            f'<td style="padding:6px 10px;text-align:center;color:{sub}">{item["pub_date"]}</td>'
            f'<td style="padding:6px 10px;text-align:center;font-weight:bold;color:{col}">{item["impressions"]}</td>'
            f'<td style="padding:6px 10px;text-align:center;color:{sub}">{item["reads"]}</td>'
            f'<td style="padding:6px 10px;text-align:center;color:{sub}">{item["replies"]}</td>'
            f'<td style="padding:6px 10px;text-align:center;color:{sub}">{item["engagements"]}</td>'
            f'<td style="padding:6px 10px">{obs_link}</td>'
            f'</tr>'
        )
    html += "</table>"
    return html


# ── Markdown → HTML ──────────────────────────────────────────────────────────
def inline_fmt(text, browser=False):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    code_bg  = "#1e1e2e" if browser else "#f5f5f5"
    code_col = "#79c0ff" if browser else "#d63384"
    text = re.sub(r"`([^`]+)`", f'<code style="background:{code_bg};color:{code_col};padding:1px 5px;border-radius:3px;font-size:12px">\\1</code>', text)
    em_col = "#e0e0e0" if browser else "#1a1a2e"
    text = re.sub(r"\*\*(.+?)\*\*", f'<strong style="color:{em_col}">\\1</strong>', text)
    it_col = "#bbb" if browser else "#555"
    text = re.sub(r"\*(.+?)\*", f'<em style="color:{it_col}">\\1</em>', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" style="color:#58a6ff">\1</a>', text)
    return text


def md_to_html(text, browser=False):
    body     = strip_frontmatter(text)
    lines    = body.split("\n")
    out      = []
    in_pre   = in_ul = in_ol = False
    col      = "#ccc" if browser else "#333"
    bg_pre   = "#111120" if browser else "#f5f5f5"
    bdr_pre  = "#30363d" if browser else "#ddd"
    hr_col   = "#333"   if browser else "#e0e0e0"

    for line in lines:
        if line.strip().startswith("```"):
            if in_pre:
                out.append("</code></pre>"); in_pre = False
            else:
                if in_ul: out.append("</ul>"); in_ul = False
                if in_ol: out.append("</ol>"); in_ol = False
                out.append(f'<pre style="background:{bg_pre};color:#c9d1d9;padding:14px;border-radius:6px;overflow-x:auto;font-size:12px;line-height:1.6;border:1px solid {bdr_pre}"><code>')
                in_pre = True
            continue

        if in_pre:
            out.append(line.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))
            continue

        bullet = re.match(r"^\s*[-*+]\s+(.*)", line)
        num    = re.match(r"^\s*\d+\.\s+(.*)", line)
        if in_ul and not bullet: out.append("</ul>"); in_ul = False
        if in_ol and not num:    out.append("</ol>"); in_ol = False

        if re.match(r"^---+$", line.strip()):
            out.append(f'<hr style="border:none;border-top:1px solid {hr_col};margin:16px 0">'); continue

        h4 = re.match(r"^####\s+(.*)", line)
        h3 = re.match(r"^###\s+(.*)",  line)
        h2 = re.match(r"^##\s+(.*)",   line)
        h1 = re.match(r"^#\s+(.*)",    line)
        c1 = "#e0e0e0" if browser else "#1a1a2e"
        c2 = "#d0d0d0" if browser else "#1a1a2e"
        c3 = "#aaa"    if browser else "#444"
        bd = "#333"    if browser else "#eee"
        if h1: out.append(f'<h1 style="font-size:19px;color:{c1};margin:20px 0 10px;border-bottom:1px solid {bd};padding-bottom:8px">{inline_fmt(h1.group(1),browser)}</h1>'); continue
        if h2: out.append(f'<h2 style="font-size:15px;color:{c2};margin:18px 0 8px">{inline_fmt(h2.group(1),browser)}</h2>'); continue
        if h3: out.append(f'<h3 style="font-size:13px;color:{c3};margin:14px 0 6px">{inline_fmt(h3.group(1),browser)}</h3>'); continue
        if h4: out.append(f'<h4 style="font-size:12px;color:#888;margin:10px 0 4px">{inline_fmt(h4.group(1),browser)}</h4>'); continue

        if bullet:
            if not in_ul: out.append(f'<ul style="margin:6px 0 6px 20px;padding:0;color:{col};font-size:13px;line-height:1.7">'); in_ul = True
            out.append(f'<li style="margin-bottom:4px">{inline_fmt(bullet.group(1),browser)}</li>'); continue
        if num:
            if not in_ol: out.append(f'<ol style="margin:6px 0 6px 24px;padding:0;color:{col};font-size:13px;line-height:1.7">'); in_ol = True
            out.append(f'<li style="margin-bottom:4px">{inline_fmt(num.group(1),browser)}</li>'); continue

        if not line.strip():
            out.append('<div style="height:7px"></div>'); continue

        out.append(f'<p style="margin:3px 0;font-size:13px;line-height:1.8;color:{col}">{inline_fmt(line,browser)}</p>')

    if in_ul: out.append("</ul>")
    if in_ol: out.append("</ol>")
    if in_pre: out.append("</code></pre>")
    return "\n".join(out)


# ── Full page builder ────────────────────────────────────────────────────────
def build_html(md_text, report_type, filepath, browser=False):
    meta   = TYPE_META.get(report_type, TYPE_META["jarvis"])
    accent = meta["accent"]
    emoji  = meta["emoji"]
    label  = meta["label"]
    fname  = Path(filepath).name

    activity    = scan_vault_activity()
    ready       = get_ready_to_publish()
    new_briefs  = get_new_briefs()
    time_sens   = get_time_sensitive()
    analytics   = get_published_analytics()

    def sec(title, em, content, ac):
        return section(title, em, content, ac, browser)

    bg_page = "#0d0d14" if browser else "#f0f0f4"
    bg_hdr  = "#1a1a2e"
    foot_col = "#555"   if browser else "#aaa"

    obs_vault_btn = btn_link("📓 Open JARVIS Vault →", "obsidian://open?vault=JARVIS-vault", "#7C3AED")

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>JARVIS — {label} — {DISPLAY_DATE}</title>
<style>
  *{{box-sizing:border-box}}
  body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:{bg_page};margin:0;padding:0}}
  a{{color:#58a6ff}}
  @media(max-width:600px){{.wrapper{{padding:10px 8px!important}}}}
</style>
</head>
<body><div class="wrapper" style="max-width:760px;margin:0 auto;padding:24px 16px">

  <div style="background:{bg_hdr};border-left:5px solid {accent};color:#fff;padding:22px 26px;border-radius:10px;margin-bottom:18px">
    <div style="font-size:21px;font-weight:bold;margin-bottom:4px">{emoji} JARVIS — {label}</div>
    <div style="font-size:12px;opacity:0.55">{DISPLAY_DATE} · {fname}</div>
    <div style="margin-top:14px">{obs_vault_btn}</div>
  </div>

  {sec("Vault Activity — Last 24 Hours",      "🗂",  build_vault_activity_html(activity, browser),       "#607D8B")}
  {sec("Ready to Publish",                    "🚀",  build_ready_to_publish_html(ready, browser),         "#9C27B0")}
  {sec("New Briefs Generated",                "📋",  build_new_briefs_html(new_briefs, browser),          "#2196F3")}
  {sec("Time-Sensitive Captures",             "⚡",  build_time_sensitive_html(time_sens, browser),       "#FF9800")}
  {sec("Published Content Analytics",         "📈",  build_analytics_html(analytics, browser),            "#00BCD4")}
  {sec(label + " — Full Report",              emoji, md_to_html(md_text, browser),                        accent)}

  <p style="text-align:center;font-size:11px;color:{foot_col};margin-top:28px">
    JARVIS · {TODAY_STR} · <a href="{obsidian_url(filepath)}" style="color:#7C3AED">Open source file in Obsidian</a>
  </p>

</div></body></html>"""


# ── Send email ───────────────────────────────────────────────────────────────
def send_email(service, html_body, subject):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = TO_EMAIL
    msg["To"]      = TO_EMAIL
    msg.attach(MIMEText(html_body, "html"))
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    print(f"✅ Email sent → {TO_EMAIL} | {subject}")


# ── Entry point ──────────────────────────────────────────────────────────────
def main():
    args = sys.argv[1:]
    if "--file" not in args:
        print("Usage: send_jarvis_email.py --file /path/to/output.md")
        sys.exit(1)

    file_path   = Path(args[args.index("--file") + 1])
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    md_text     = file_path.read_text(errors="ignore")
    report_type = detect_type(file_path.name)
    meta        = TYPE_META.get(report_type, TYPE_META["jarvis"])
    subject     = f"{meta['prefix']} — {DISPLAY_DATE}"

    email_html   = build_html(md_text, report_type, file_path, browser=False)
    browser_html = build_html(md_text, report_type, file_path, browser=True)

    out_dir      = BOT_DIR / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    slug         = file_path.stem.lstrip("_")
    browser_path = out_dir / f"{slug}.html"
    browser_path.write_text(browser_html)
    subprocess.Popen(["open", str(browser_path)])
    print(f"🌐 Browser report opened: {browser_path}")

    creds = get_credentials()
    gmail = build("gmail", "v1", credentials=creds)
    send_email(gmail, email_html, subject)


if __name__ == "__main__":
    main()
