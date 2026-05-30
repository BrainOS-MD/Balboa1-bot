# Command: `briefing`

The complete daily brief. Covers outreach, follow-ups, networking, content, grants, and pipeline.
**Total run time: ~15–20 minutes. Output: one markdown file to copy-paste from.**

---

## Step 1: Load all context

Read these in order:
1. `CLAUDE.md` — standing rules (already loaded)
2. `context/balboa1_facts.md` — proof points (update this regularly!)
3. `context/founder_voice.md` — Nick's voice
4. `skills/investor-outreach/SKILL.md`
5. `skills/grant-application/SKILL.md`
6. `skills/contact-enrichment/SKILL.md`
7. `skills/content-generation/SKILL.md`
8. `skills/networking/SKILL.md`

**Also check for Jarvis bridge:**
Look for `~/JARVIS-vault/03-BRIEFS/_balboa-bridge.md`. If it exists and was updated in the last 7 days, read it. This seeds both the content and networking sections with Nick's current thinking.

---

## Step 2: Read the Google Sheet state

Connect via gspread. Read:
- All 5 silo tabs (Venture, OTC, Partnerships, Freight, General Contacts)
- `🎯 Grants Pipeline` tab
- `📨 Drafts Log` (last 30 days — to avoid duplicate drafts)

---

## Step 3: Run the daily research (for content + networking)

Before drafting anything, run 4 web searches to capture today's signal:
1. `stablecoin news [month year]` OR `GENIUS Act update [year]`
2. `maritime trade settlement payments [year]` OR `Panama Canal news [month year]`
3. `LatAm fintech investment [year]` OR `RWA stablecoin funding [year]`
4. One wildcard: `[topic from Jarvis bridge "Nick's Current Thinking" if available]`

Save the top 2–3 findings as a mental note — they'll seed the content and networking sections.

---

## Step 4: Identify all actions

Following the logic in each skill:

**A. Replies needing response** — Status "7. Replied — Positive" + Reply Snippet filled
**B. New outreach** — Status "1. To Connect", Tier 0/1, no recent draft in Drafts Log
**C. Follow-ups due** — FU1 at day 4, FU2 at day 10 (per `skills/investor-outreach/SKILL.md`)
**D. Grants needing action** — deadlines within 14 days or status "Drafting"
**E. Networking contacts** — 15 warm contacts (5+5+5 per `skills/networking/SKILL.md`)
**F. Content** — today's angle from research + Jarvis bridge

---

## Step 5: Draft everything

Run each section in order. Don't summarize or skip.

---

## Step 6: Build the pipeline snapshot

Calculate from live sheet data:

```
PIPELINE SNAPSHOT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total contacts in CRM:        [N]
Active pipeline (sent→sched): [N]    ████████░░ [bar]
Positive replies:             [N]    ████░░░░░░ [bar]
Meetings scheduled:           [N]    ██░░░░░░░░ [bar]
Reply rate:                   [X%]
Conversion to meeting:        [X%]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTREACH FUNNEL
  🟦 To Connect: [N]
  🟨 Request Sent: [N]
  🟩 Accepted: [N]
  📧 Intro Sent: [N]
  📅 Meeting Req'd: [N]
  ✅ Scheduled: [N]
  💬 Replied Positive: [N]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GRANTS
  T1 🔥 Not Started: [N]
  T1 🔥 In Progress: [N]
  Submitted: [N]
  Awarded: [N]
  Deadlines this week: [N]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
JARVIS BRIDGE
  Briefs ready to write: [N or "not synced"]
  Last synced: [date or "not synced"]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

For the ASCII progress bars: █ = 10% of pipeline total. Cap at 10 blocks. Approximate is fine.

---

## Step 7: Write the output file

Save to `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/JARVIS-vault/00-INBOX/_YYYY-MM-DD-daily-brief.md`. Leading underscore required — ensures file sorts to top of 00-INBOX. Use this exact structure:

```markdown
# Daily Brief — [Day, Date]

[PIPELINE SNAPSHOT block from Step 6]

---

## 🔥 Replies — Respond First

[Drafted responses for each "7. Replied — Positive" contact with a Reply Snippet.
Follow rules in skills/investor-outreach/SKILL.md for reply classification.]

---

## 🚀 New Outreach

[Connection requests + intro messages for Tier 0/1 contacts at status "1. To Connect".
Max 12 new drafts. Flag any without Enrichment data.]

---

## 🔁 Follow-Ups Due

[FU1 and FU2 drafts for contacts past their follow-up window.
Each draft includes: last touch date, original variant ID, new draft + new variant ID.]

---

## 🎯 Grants — This Week

[Actions needed for grants with deadlines ≤14 days or status "Drafting".
For each: deadline, status, suggested action, and a one-paragraph pitch angle if applying.]

---

## 📡 Networking

[5 LinkedIn messages, 5 X DMs, 5 Email drafts.
See skills/networking/SKILL.md for format and quality rules.]

---

## 📝 Content

[5 platform drafts: X thread, LinkedIn personal, LinkedIn company, Substack, Company Blog.
See skills/content-generation/SKILL.md for format and compliance rules.
Each draft: copy-paste ready.]

---

## 📊 This Week's Priorities

[3-5 bullets on what to focus on this week based on what the pipeline shows.
Not generic advice — specific to Nick's current pipeline state.]
```

---

## Step 8: Append to Drafts Log

Append every outreach draft (sections: Replies, New Outreach, Follow-Ups) to the `📨 Drafts Log` tab.
Do NOT log networking messages or content drafts in the Drafts Log (they have their own tracking).

---

## Step 9: Check for backfill updates

Scan all silo rows where Status advanced since the last briefing. For any that moved to a "sent" state, write today's date into the Last Touch Date column (col M).

---

## Step 10: Summary message to Nick

```
✅ Daily brief ready: 00-INBOX/_[date]-daily-brief.md

  🔥 [N] replies needing response
  🚀 [N] new outreach drafts (Tier 0/1)
  🔁 [N] follow-ups due
  🎯 [N] grant actions this week
  📡 15 networking messages (5+5+5)
  📝 5 content drafts (X · LinkedIn personal · Company · Substack · Blog)

Pipeline: [N] active contacts · [X%] reply rate · [N] meetings this week
[If Jarvis bridge found]: 🧠 Jarvis: [N] briefs seeding today's content
```

---

## Edge cases

**Nothing in the outreach pipeline:** Tell Nick, then ask if he wants to run enrichment on new contacts to build the pipeline back up.

**Jarvis bridge not found:** Proceed normally. Note in the summary: "🧠 Jarvis: not synced — run `jarvis-to-balboa` to enable smart content seeding."

**Sheet unreachable:** Retry once. If still failing, provide instructions for checking credentials.

**Too many drafts (>40 total):** Prioritize in this order: Replies → Follow-Ups → Tier 0 Outreach → Tier 1 Outreach → Grants → Networking → Content. Cap at top 35 drafts and tell Nick what was deferred.
