# Changelog — BizBot & JARVIS

---

## BizBot

### v2.0 — June 2026
**Daily BizBot Brief — Full HTML Dashboard**

- Renamed all briefing output from "BALBOA1 Brief" → **BizBot Brief**
- `send_briefing.py` — complete HTML briefing email with Gmail send
- Dark mode browser version auto-opens on every run with JS copy buttons
- **Top 20 messages** — copy-paste ready blocks ranked by CRM stage + tier priority
  - 💬 DM Now → button per contact, links directly to LinkedIn profile
- **Per-platform copy buttons** — DRAFTS files split by `## Platform` headers; separate `📋 Copy X Thread`, `📋 Copy LinkedIn`, `📋 Copy Substack` buttons per section
- **Content ready to post** — 03-BRIEFS files with `ready_to_publish: true` surfaced with platform compose buttons and Obsidian deep links
- **Pipeline dashboard** — OTC + VC stage counts with ASCII bar charts
- **Priority actions** — accepted connections with no intro sent
- **Follow-ups overdue** — contacts past next action date
- **ready_to_publish frontmatter** — auto-injected into all 03-BRIEFS files
- **04-PUBLISHED promotion** — files with `ready_to_publish: true` auto-moved with full analytics frontmatter
- **Per-platform URL fields** — promotion injects `LinkedIn URL:`, `X URL:`, `Substack URL:` etc. based on `platforms` field; platform names become hyperlinks in analytics table once filled
- **launchd cron** — 9am daily via `com.bizbot.dailybrief.plist`; skips if already sent, `--force` overrides

### v1.0 — May 2026
**Initial Release**

- Google Sheets CRM integration via gspread OAuth
- Personalized DM drafts for OTC, VC, Grants, and networking contacts
- Stage-based CRM logic: auto next-action dates, enrichment triggers, intro DM sequencing
- All output routed to JARVIS vault `00-INBOX/`
- Briefing skill: pipeline snapshot, priority actions, follow-ups, top outreach queue
- Founder voice rules, banned phrase list, variant tagging system

---

## JARVIS

### v3.0 — June 2026
**Full Dashboard Email Notifier**

- `send_jarvis_email.py` — rich HTML email + dark-mode browser file after every JARVIS skill run
- **Triggers:** process-inbox, auto-research, think-deep, weekly-digest (generate-brief excluded — surfaces in process-inbox email instead)
- **Vault activity dashboard** — all files created/modified in last 24h, grouped by folder, each linked to Obsidian
- **Ready to publish section** — 03-BRIEFS files with `ready_to_publish: true`, full cards with platform compose buttons, Copy + NotebookLM buttons
- **New briefs section** — recently generated briefs with Copy + Generate Content command copy button
- **Time-sensitive captures** — vault-index `time-sensitive` entries tabulated; summary is a live Obsidian deep link
- **Published analytics table** — 04-PUBLISHED with impressions/reads/replies/engagements; platform names link to live posts when URLs are filled
- **NotebookLM button** — on every content card next to Copy; opens notebooklm.google.com for instant podcast source
- **Per-platform copy buttons** — DRAFTS files detected, platform sections parsed, individual copy buttons per platform
- **Dark mode** — browser version always dark; email version light for inbox readability

### v2.0 — May–June 2026
**Skill Stack Expansion**

- `auto-research` — 3-round iterative research loop (decompose → search → synthesize)
- `think-deep` — structured think → research → synthesize for decisions
- `generate-brief` — auto-research + 7-field brief structure saved to 03-BRIEFS
- `write-content` — per-platform drafts with compliance checklist for LinkedIn Company
- `weekly-digest` — engagement pattern analysis from 04-PUBLISHED
- `jarvis-to-bizbot` — bridge export: top 3 briefs → `_bizbot-bridge.md` for BizBot consumption
- `lint-vault` — vault health check + auto-fix
- `kickoff` — co-founder planning pass before new sub-projects
- **Vault index** — `05-CLAUDE/vault-index.md` master catalog with Sentiment + Depth columns
- **Fast lane** — captures with ≥2 supporting notes auto-trigger `generate-brief`
- **Hot cache** — 150-line limit with auto-archive to `hot-cache-archive-YYYY-MM.md`
- **04-PUBLISHED frontmatter** — date/datetime calendar pickers, multi-select platforms, analytics fields

### v1.0 — May 2026
**Initial Release**

- Obsidian vault structure: 00-INBOX → 01-CAPTURES → 02-CONNECTIONS → 03-BRIEFS → 04-PUBLISHED → 05-CLAUDE
- `process-inbox` — triage, sharpen, file captures; update vault-index; prune hot-cache
- `scrape-link` — URL fetch, clean, file intelligence
- `weekly-connections` — synthesis sessions with index-first filtering
- SOUL.md — single source of truth for Nick's identity, audience, voice, and banned phrases
- Session start/end protocol — auto-process inbox, hot-cache update

---

## Roadmap

- [ ] Chrome MCP analytics scraper — auto-pull post metrics from LinkedIn/X into 04-PUBLISHED
- [ ] NotebookLM iOS deep link — swap in native URL scheme if/when Google publishes one
- [ ] JARVIS → BizBot live signal injection — surface time-sensitive captures directly into top 20 message ranking
- [ ] Substack publication URL — wire in personal Substack URL for compose button
