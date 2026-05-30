---
name: crm-analysis
description: Scans and analyzes the full CRM pipeline using only the data already in your Google Sheet — no external API calls, no web searches, no token overhead. Produces a pipeline health report with specific, actionable findings. Activate when Nick types "crm-analysis" or at the start of the weekly review. Can also be called automatically during the daily briefing to surface the top 3 priority insights.
---

# CRM Analysis Skill

## What this is NOT

This is not a web search skill. It does not call external APIs.

It reads your Google Sheet — which is already connected — and derives insights from the data that's already there. Think of it as the weekly review your CRM should give you automatically but doesn't.

## What it produces

A `CRM Health Report` with six sections:
1. Pipeline pulse (where are contacts clustered?)
2. Velocity gaps (where are contacts getting stuck?)
3. Gone cold (contacts with no touch in 30+ days)
4. Variant performance (which message types get replies?)
5. Top 5 opportunities (specific contacts to prioritize today)
6. Grant pipeline health (deadlines + drafts in progress)

## Step 1: Read the Sheet

Load from Google Sheet (already configured via gspread):
- All 5 silo tabs — full rows, all columns
- Drafts Log tab — all rows with Outcome data
- Grants Pipeline tab — all rows

Calculate today's date for age computations.

## Step 2: Pipeline Pulse

Count contacts at each stage across all silos:

```
Stage               Count    % of total
───────────────────────────────────────
1. To Connect       [N]      [X%]
2. Request Sent     [N]      [X%]
3. Request Accepted [N]      [X%]
4. Intro Sent       [N]      [X%]
5. Meeting Req'd    [N]      [X%]
6. Scheduled        [N]      [X%]
7. Replied — Pos    [N]      [X%]
8. Replied — Not Now[N]      [X%]
9. FU1 Due          [N]      [X%]
10. FU2 Due         [N]      [X%]
11. Not a Fit       [N]      [X%]
12. Closed — Won    [N]      [X%]
13. Closed — Lost   [N]      [X%]
```

**Signal:** If >50% of the pipeline is at Stage 1 (To Connect), outreach velocity is low. If >30% is at Stages 9–10 (follow-ups), follow-through is the bottleneck.

## Step 3: Velocity Gaps

For each stage transition, measure the average days contacts spend in that stage:
- Days at Stage 2 before moving to Stage 3 (connection acceptance rate proxy)
- Days at Stage 4 before moving to Stage 5 (intro response rate proxy)
- Days at Stage 5 before moving to Stage 6 (meeting conversion rate proxy)

Flag any stage where average dwell > 14 days as a **velocity gap**.

Compare velocity by silo: is one silo consistently slower than others?

## Step 4: Gone Cold

Find all contacts where:
- Status is between Stage 3 and Stage 8 (active pipeline)
- Last Touch Date is more than 30 days ago OR is empty

These are contacts that were engaged but fell off the radar.

List each one with: Name, Company, Silo, Last Touch Date (or "never recorded"), Stage.

Flag as **Priority: Review** — these are warm leads going cold.

## Step 5: Variant Performance

Read the Drafts Log tab. For rows where Outcome is filled:

Calculate reply rate by:
- `Touch Type` (Connection Request vs Intro vs Follow-up)
- `Platform` (LinkedIn vs X vs Email)
- `Variant ID` prefix (VL1 vs VL2 vs VE1, etc.)

**Only count variants with ≥ 5 sends** (anything less isn't statistically meaningful).

Rank by reply rate. Produce:
- Top 3 best-performing variants (highest reply rate)
- Bottom 3 worst-performing variants (lowest reply rate)
- One sentence insight: "X opener on LinkedIn is outperforming Y opener by Z%"

If fewer than 20 total logged outcomes: note "Insufficient data for reliable variant analysis. Log outcomes consistently in the Drafts Log for 2 more weeks."

## Step 6: Top 5 Opportunities

Pick the 5 contacts most worth acting on TODAY based on this scoring:

| Factor | Points |
|--------|--------|
| Status = "7. Replied — Positive" with no logged response | +5 |
| Status = "2. Request Sent" AND Next Action Date ≤ today | +4 |
| Status = "3. Request Accepted" AND Enrichment column empty | +4 |
| Tier 0 contact | +3 |
| Tier 1 contact | +2 |
| Gone cold > 30 days (Stage 3–8) | +3 |
| Has Reply Snippet (they replied, needs response) | +3 |
| Last Touch Date = 4–5 days ago (FU1 window) | +2 |
| Last Touch Date = 10–11 days ago (FU2 window) | +2 |

Pick the top 5 by total score. For each, output:
```
[Name] · [Company] · [Silo] — Score: [X]
Status: [stage]  |  Last Touch: [N days ago or never]
Why: [1-line reason this contact is a priority]
Action: [specific thing to do — reply, enrich, follow up, check connection status]
```

## Step 7: Grant Pipeline Health

From Grants Pipeline tab:
- Deadlines within 7 days: **URGENT**
- Deadlines within 14 days: **UPCOMING**
- Status = "Drafting" (in progress, needs completion)
- Status = "Submitted" AND Date Applied > 30 days ago (chase for a response)

Count grants by status tier (T1, T2, T3) that haven't been started.

## Step 8: Output Format

```markdown
# CRM Health Report — [Date]

## 📊 Pipeline Pulse
[stage counts table]

**Bottleneck:** [the stage where the most contacts are stuck]
**Velocity issue:** [any stage with average dwell > 14 days]

## 🚨 Gone Cold ([N] contacts)
[list with name, company, last touch, days inactive]

## 📬 Variant Performance
Best performing: [variant ID] — [X%] reply rate ([N] sends)
Worst performing: [variant ID] — [X%] reply rate ([N] sends)
Insight: [one-sentence finding]

## 🎯 Top 5 Opportunities Today
[5 contacts with score + action]

## 🎯 Grant Pipeline
URGENT (≤7 days): [N] grants
UPCOMING (≤14 days): [N] grants
In progress: [N] drafts
Response-due: [N] submitted > 30 days
```

## Standing rules

- Flag data quality issues when found: "Last Touch Date is empty for [N]% of Stage 4+ contacts — consider running a backfill."
- Never invent data. If a column is empty, say so.
- Never suggest checking LinkedIn or external sources. This skill is purely internal.
- If the Sheet is clean and everything looks healthy, say so directly: "Pipeline looks healthy. No urgent flags."
