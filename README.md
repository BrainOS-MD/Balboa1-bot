# BizBot — AI Outreach & Briefing System

BizBot is Nick Marton's outreach copilot for BALBOA1. It runs inside Claude Code, reads a Google Sheets CRM, generates personalized networking messages, delivers a daily HTML briefing email, and connects with JARVIS (the second-brain vault) to bridge content intelligence into every outreach decision.

---

## What It Does

| Command | Description |
|---|---|
| `briefing` | Full daily BizBot Brief — pipeline snapshot, top 20 copy-ready messages, content ready to post, follow-ups overdue |
| `stage-check` | Stage 2 connection reviews + Stage 3 enrichment |
| `crm-analysis` | Pipeline health report |
| `meeting-prep [NAME]` | Pre-call brief for a specific contact |
| `network-expand` | News → names → CRM connection queue |
| `enrich-contact [NAME]` | Deep-research one contact |
| `reply-to [NAME]` | Draft response to a received reply |
| `grant-draft [NAME]` | Draft a full grant application |

All output saves to the JARVIS vault `00-INBOX/` with `_YYYY-MM-DD-[command].md` naming.

---

## System Architecture

```
Claude Code (interactive session)
│
├── BizBot (this repo)
│   ├── CLAUDE.md               ← standing instructions + CRM schema
│   ├── scripts/
│   │   ├── send_briefing.py    ← daily BizBot Brief email + browser HTML
│   │   └── send_jarvis_email.py← JARVIS skill output email notifier
│   ├── skills/                 ← per-command prompt files
│   ├── context/                ← balboa1_facts.md, founder_voice.md
│   └── credentials/            ← OAuth tokens (gitignored)
│
├── JARVIS Vault (Obsidian)
│   ├── 00-INBOX/               ← all bot output lands here
│   ├── 03-BRIEFS/              ← content briefs + written drafts
│   ├── 04-PUBLISHED/           ← published posts with analytics
│   └── 05-CLAUDE/              ← JARVIS skills + vault index
│
└── Google Sheets CRM
    └── BALBOA1 CRM             ← OTC, VC, Grants pipeline tabs
```

---

## Daily BizBot Brief

Sent automatically at 9am via launchd (`/Library/LaunchAgents/com.bizbot.dailybrief.plist`), or manually with:

```bash
cd ~/balboa1-bot && .venv/bin/python scripts/send_briefing.py --force
```

The brief includes:
- **Pipeline dashboard** — OTC + VC stage counts with ASCII bar charts
- **Priority actions** — accepted connections with no intro sent yet
- **Follow-ups overdue** — past next action date
- **Top 20 messages** — copy-paste ready, ranked by stage + tier, with 💬 DM Now → buttons
- **Content ready to post** — 03-BRIEFS files marked `ready_to_publish: true`, with per-platform copy buttons
- **Dark mode browser version** — opens automatically with JS copy buttons
- **Gmail version** — sent to nick.grosz@gmail.com with mobile-friendly DM and Obsidian buttons

---

## JARVIS Email Notifier

After each JARVIS skill run (process-inbox, auto-research, think-deep, weekly-digest), an email is sent with:

- **Vault activity** — all files created/modified in the last 24 hours
- **Ready to publish** — briefs marked `ready_to_publish: true` with platform compose buttons
- **New briefs** — recently generated briefs with copy + Generate Content command buttons
- **Time-sensitive captures** — vault-index entries tagged `time-sensitive`, linked to Obsidian
- **Published analytics** — 04-PUBLISHED table with impressions/reads/replies/engagements

---

## Setup

See [SETUP.md](SETUP.md) for full first-run instructions.

---

## Versions

See [docs/CHANGELOG.md](docs/CHANGELOG.md) for the full version history of BizBot and JARVIS.

---

## Security

- `credentials/` is gitignored — never commit OAuth tokens
- No API keys are used — all Google auth uses OAuth with your personal account
- BizBot is draft-only — it never sends messages or modifies live data without Claude in Chrome
