# BizBot + JARVIS — Product Wiki

---

## Table of Contents

1. [System Overview](#system-overview)
2. [BizBot](#bizbot)
   - [Daily BizBot Brief](#daily-bizbot-brief)
   - [CRM Commands](#crm-commands)
   - [CRM Stage Logic](#crm-stage-logic)
   - [Outreach Rules](#outreach-rules)
3. [JARVIS](#jarvis)
   - [Vault Structure](#vault-structure)
   - [Skills](#skills)
   - [Email Notifier](#email-notifier)
   - [Frontmatter System](#frontmatter-system)
4. [Content Pipeline](#content-pipeline)
5. [Automation](#automation)
6. [Security & Credentials](#security--credentials)

---

## System Overview

BizBot and JARVIS are two AI systems that run inside Claude Code and operate on the same person's life and business:

| System | What It Does | Where It Runs |
|---|---|---|
| **BizBot** | Outreach copilot — CRM, DMs, briefings | `~/balboa1-bot/` |
| **JARVIS** | Second brain — captures, research, content | Obsidian vault |

They share one communication channel: the JARVIS vault `00-INBOX/`. BizBot writes all its output there. JARVIS reads the bridge file (`03-BRIEFS/_bizbot-bridge.md`) to inject current thinking into BizBot's outreach.

---

## BizBot

### Daily BizBot Brief

The BizBot Brief is delivered in two formats every morning:

**Email (Gmail)** — sent to nick.grosz@gmail.com
- Light theme, mobile-optimised
- 💬 DM Now → buttons link to LinkedIn profiles
- Platform-specific draft labels (no JS copy in email clients)

**Browser HTML** — opens automatically in default browser
- Dark mode always on
- JS-powered 📋 Copy buttons — one per platform section for DRAFTS files
- 🎧 NotebookLM → button next to every copy button

**Trigger:**
```bash
# Manual
cd ~/balboa1-bot && .venv/bin/python scripts/send_briefing.py --force

# Automatic — 9am via launchd
/Library/LaunchAgents/com.bizbot.dailybrief.plist
```

**Brief sections in order:**

| Section | Description |
|---|---|
| Pipeline Snapshot | OTC + VC contacts per stage, ASCII bar chart |
| Priority Actions | Accepted connections with no intro DM yet |
| Follow-ups Overdue | Contacts past their Next Action Date |
| Top 20 Messages | Copy-paste DMs ranked by stage priority + tier |
| Content Ready to Post | 03-BRIEFS files with `ready_to_publish: true` |

---

### CRM Commands

| Command | What It Does |
|---|---|
| `briefing` | Full daily BizBot Brief |
| `stage-check` | Reviews Stage 2 + enriches Stage 3 contacts |
| `crm-analysis` | Pipeline health, no external API calls |
| `meeting-prep [NAME]` | Pre-call brief for a specific contact |
| `network-expand` | News → names → CRM queue |
| `enrich-contact [NAME]` | Deep-research one contact |
| `reply-to [NAME]` | Draft response to a received reply |
| `grant-draft [NAME]` | Full grant application draft |

All output: `JARVIS-vault/00-INBOX/_YYYY-MM-DD-[command].md`

---

### CRM Stage Logic

| Stage | Label | Auto-action |
|---|---|---|
| 1 | To Connect | Draft connection request (no note, <280 chars) |
| 2 | Request Sent | Set Next Action Date = today + 7 days |
| 3 | Request Accepted | Trigger enrichment + draft intro DM |
| 4 | Intro Sent | Follow-up queue after 7 days |
| 5 | Meeting Requested | Pre-call brief available |

**Connection requests are always sent without a note.** The first real message is the intro DM after Stage 3.

---

### Outreach Rules

- **One ask per message.** Explicit. Specific time or action.
- **Word count caps:** LinkedIn DM ≤120 words · Email ≤150 words · Follow-up ≤80 words
- **Always lead with proof** from `context/balboa1_facts.md`
- **Variant tagging:** VL1 (LinkedIn touch 1), VL4 (intro DM after Stage 3), VE1 (Email), VX1 (X DM)
- **Every draft logged** to `📨 Drafts Log` tab in Google Sheets

**Banned phrases** (source of truth: `SOUL.md`): delve, tapestry, I'd love to, excited to share, game-changing, revolutionary, utilize, really impressed with your team

---

## JARVIS

### Vault Structure

```
00-INBOX/           ← raw captures + all bot output
01-CAPTURES/
  observations/     ← things noticed, unpolished
  reactions/        ← gut response to something read/heard
  patterns/         ← same principle in two different domains
  questions/        ← genuinely unresolved questions
  numbers/          ← real data with specific figures
02-CONNECTIONS/     ← synthesized insights from 2+ captures
03-BRIEFS/          ← content ready to write; hooks + closers done
04-PUBLISHED/       ← archived posts with performance analytics
05-CLAUDE/
  vault-index.md    ← master catalog (read before scanning files)
  hot-cache.md      ← session memory, max 150 lines
  SOUL.md           ← Nick's identity, audience, voice (single source of truth)
  skills/           ← per-skill instruction files
```

---

### Skills

| Skill | Trigger | Output |
|---|---|---|
| `process-inbox` | Session start (auto) + manual | Files captures, updates vault-index, sends JARVIS email |
| `auto-research` | `auto-research [topic]` | Research file in 00-INBOX |
| `think-deep` | `think-deep [problem]` | Decision brief in 00-INBOX |
| `generate-brief` | `generate brief for [topic]` | Content brief in 03-BRIEFS |
| `write-content` | `write the brief for [title]` | DRAFTS file in 03-BRIEFS |
| `jarvis-to-bizbot` | `jarvis-to-bizbot` | `_bizbot-bridge.md` in 03-BRIEFS |
| `weekly-digest` | `weekly digest` | Performance report in 00-INBOX |
| `lint-vault` | `lint vault` | Health check + auto-fix report |
| `scrape-link` | URL dropped in chat | Cleaned content filed to 01-CAPTURES |
| `kickoff` | `kickoff [project]` | Planning brief |

**Fast Lane:** if a new capture has ≥2 supporting vault-index entries, `generate-brief` runs automatically.

---

### Email Notifier

`send_jarvis_email.py` runs after every skill that produces output. Triggered via bash at the end of each skill's instruction file.

**Email contents:**

| Section | Source |
|---|---|
| Vault Activity | Files modified in last 24h across all vault folders |
| Ready to Publish | 03-BRIEFS with `ready_to_publish: true` |
| New Briefs | 03-BRIEFS files modified in last 24h, not yet ready to publish |
| Time-Sensitive Captures | vault-index rows tagged `time-sensitive`, linked to Obsidian |
| Published Analytics | 04-PUBLISHED frontmatter: impressions, reads, replies, engagements |
| Full Report | The skill's markdown output, rendered as HTML |

**Per-platform copy buttons:** DRAFTS files (`-DRAFTS.md`) are automatically split by `## Platform` H2 headers. Each platform section gets its own colored copy button.

---

### Frontmatter System

**03-BRIEFS** (auto-injected by send_briefing.py):
```yaml
ready_to_publish: false   ← toggle to true to queue for promotion
platforms: [linkedin, x]  ← drives platform buttons + URL fields on promotion
```

**04-PUBLISHED** (injected on promotion from 03-BRIEFS):
```yaml
published: false
published_date:           ← Obsidian calendar picker
published_time:           ← Obsidian datetime picker
LinkedIn URL:             ← per-platform, auto-generated from platforms field
X URL:
platforms_published: []   ← multi-select
impressions:
reads:
replies:
engagements:
```

Platform URL fields are generated dynamically on promotion based on whatever platforms are listed in the source brief. If `platforms: [linkedin, x, substack]`, the promoted file gets `LinkedIn URL:`, `X URL:`, and `Substack URL:` as individual properties. Once filled in Obsidian, these become live hyperlinks in the Published Analytics table.

---

## Content Pipeline

```
Capture (00-INBOX)
  ↓ process-inbox
File (01-CAPTURES)
  ↓ weekly-connections (or fast-lane auto)
Connection (02-CONNECTIONS)
  ↓ generate-brief
Brief (03-BRIEFS)
  ↓ write-content
DRAFTS (03-BRIEFS/-DRAFTS.md)
  ↓ Set ready_to_publish: true in Obsidian
  ↓ next briefing run auto-promotes
Published (04-PUBLISHED)
  ↓ Log engagement metrics in Obsidian
  ↓ weekly-digest analyzes patterns
```

**DRAFTS file format:**
```markdown
# Drafts: [Brief Title]

## X Thread
[tweets]

## LinkedIn Personal
[post]

## Substack
[essay]
```

Each `## Platform` section gets its own copy button in the browser brief.

---

## Automation

| Job | Schedule | File | Notes |
|---|---|---|---|
| BizBot Brief | 9am daily | `com.bizbot.dailybrief.plist` | Skips if already sent; `--force` overrides |
| JARVIS email | After each skill run | Called from skill files | Manual trigger from Claude Code |

**No Claude API is used in cron.** Python scripts run free. Claude steps (inbox processing, research, briefing) are run manually from Claude Code on phone or desktop.

**launchd status:**
```bash
launchctl list | grep bizbot
launchctl load ~/Library/LaunchAgents/com.bizbot.dailybrief.plist
```

---

## Security & Credentials

| File | What It Is | Gitignored |
|---|---|---|
| `credentials/oauth_credentials.json` | Google OAuth client secret | ✅ |
| `credentials/authorized_user.json` | Refresh token (never expires unless revoked) | ✅ |

**Scopes used:**
- `googleapis.com/auth/spreadsheets` — read/write Google Sheets CRM
- `googleapis.com/auth/gmail.send` — send briefing emails
- `googleapis.com/auth/gmail.compose` — compose permissions

**Rules:**
- Never commit credentials
- BizBot is draft-only — never sends messages autonomously
- No API keys; all auth is OAuth with Nick's personal Google account
