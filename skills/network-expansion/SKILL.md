---
name: network-expansion
description: Expands the CRM pipeline by reading today's relevant news, extracting names of investors, OTC operators, and industry professionals, building a LinkedIn connection queue, and helping Nick add them via Claude Cowork desktop app. Updates the CRM automatically after each addition. Activate when Nick types "network-expand". Requires Claude Cowork installed. Free-first — no paid scraping tools.
---

# Network Expansion Skill

## What This Does

Every day there are people in the news who are directly relevant to what Nick is building: investors who just funded a competitor, OTC desks expanding into new corridors, maritime operators announcing digital transformation initiatives, VC partners tweeting about stablecoins or trade finance. This skill finds them and routes them into the CRM.

Flow:
```
Today's news → extracted names → LinkedIn search queue → Cowork adds them → CRM updated at Stage 1
```

## Requirements

- Claude Cowork desktop app (installed and running)
- LinkedIn logged in (in the browser Cowork uses)
- The CRM connected via gspread

---

## Step 1: Read today's news

Run 3 targeted web searches to find names worth connecting with:

**Search 1 — Stablecoin / payments funding news:**
`stablecoin OR RWA OR payments infrastructure funding announcement [current month year]`

**Search 2 — Maritime / trade finance news:**
`maritime trade settlement OR port payments OR trade finance news [current month year]`

**Search 3 — VC activity in the space:**
`VC investor stablecoin OR maritime fintech announcement [current month year]`

Do not run more than 3 searches.

## Step 2: Extract names and qualify them

From the search results, extract the names of people who meet ALL of these criteria:
- A real person (not a company or fund name)
- Publicly mentioned in a specific context relevant to Nick's thesis
- Has a discoverable LinkedIn presence (they're public enough to be in the news)
- Not already in the CRM (check by firm name + person name against all silo tabs)

**Quality bar — include only if:**
- They're a decision-maker (partner, managing director, VP, founder, CEO, head-of)
- The context is a strong thesis match (stablecoin, payments rails, maritime, trade finance, RWA, LatAm, Panama)
- You have a specific reason to add them (not just "they exist in this space")

**Disqualify if:**
- Already in the CRM
- The only news mention is generic industry commentary
- No LinkedIn-searchable identity
- Clearly not a fit for what Nick is doing

## Step 3: Build the connection queue

For each qualified name, output:
```
─────────────────────────────────────────────
NAME: [Full Name]
COMPANY: [Firm / Company]
TITLE: [Role as mentioned in news]
WHY: [One sentence — the specific reason this is a strong add]
NEWS CONTEXT: [The article/announcement that surfaced them]
LINKEDIN SEARCH: [Suggested search query — "Name Company"]
SILO: [Which CRM tab they belong in: Venture / OTC / Partnerships / Freight / General]
TIER: [Tier 0 / 1 / 2 based on relevance and stage of Nick's raise]
─────────────────────────────────────────────
```

Present the full list before proceeding. Pause here for Nick's review.

Ask: "Review this list. Reply 'add all', 'add [numbers]', or 'skip [numbers]' for any you want to change."

## Step 4: LinkedIn additions via Cowork

For each approved name, walk Nick through the Cowork-assisted add:

```
Adding: [Name] at [Company]

1. In Cowork, navigate to LinkedIn
2. Search: [their LinkedIn search query]
3. Find their profile — verify it's the right person (check title + company match)
4. Click Connect
5. DO NOT add a note in the connection request (per CRM flow — connection request only)
6. Reply "added [name]" when done
```

Wait for confirmation before moving to the next person. Process one at a time.

**Note:** Cowork can automate browser navigation but LinkedIn's connection flow requires manual confirmation. This prevents rate limits and account flags. LinkedIn allows ~25-30 connection requests per day safely — don't exceed this.

## Step 5: Update the CRM

For each confirmed add, write a new row to the appropriate silo tab:

| Column | Value |
|--------|-------|
| Priority | Per tier assigned in Step 3 |
| Status | `2. Request Sent` |
| Next Action Date | `=TODAY()+7` |
| Name | Full name |
| Title / Role | As found |
| Company | As found |
| LinkedIn URL | Filled in if found during the Cowork search |
| Context | News context + date |
| Enrichment | `Enrichment pending — request sent [date]` |

Batch all writes into one Sheets API call per silo.

## Step 6: Report

```
✅ Network Expansion Complete — [Date]

Added to CRM: [N] contacts
  Venture & Investment: [N]
  OTC & Market Makers: [N]
  Partnerships: [N]
  General Contacts: [N]

Skipped: [N] (below quality threshold)
Already in CRM: [N] (deduplicated)

These contacts are now at Stage 2 with Next Action Date set.
The bot will flag them for status check in 7 days.
```

## Standing rules

- Never add someone just because they showed up in a search. Qualify every name.
- Never exceed ~25 LinkedIn connection requests per day across all sources (bot-added + manual).
- Never add a note to a LinkedIn connection request — per the CRM flow, notes go in the DM after acceptance.
- If a name appears but no LinkedIn profile can be found after reasonable effort, skip them and note it.
