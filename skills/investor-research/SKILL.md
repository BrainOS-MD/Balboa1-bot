---
name: investor-research
description: Researches an investor's background, fund thesis, portfolio, and recent activity using only free sources — public web pages, news, LinkedIn public profiles, and Crunchbase's publicly visible data. Flags when meaningful data sits behind a paywall. Writes a structured funding summary to the contact's Notes column. Free-first: never calls a paid API. Activate when Nick types "investor-research [NAME]" or when Stage 3 enrichment needs a deeper funding background.
---

# Investor Research Skill

## Free-First Principle

This skill never calls paid APIs. All research comes from:
- Web search (public articles, press releases, blog posts)
- Crunchbase public profile pages (free, visible without login for basic data)
- LinkedIn company pages (publicly visible follower counts, about, recent posts)
- Fund websites and announcement posts
- Twitter/X public timelines

When data is behind a paywall (Crunchbase Pro, PitchBook, Dealroom), this skill flags exactly what's missing so Nick can decide whether to pay for a one-time lookup.

---

## What This Skill Produces

A structured investor research block written to the contact's `Notes & Research` column (col Q):

```
INVESTOR PROFILE — [Name] · [Firm]
Researched: [date]

BACKGROUND
[2-3 sentences on their background and current role at the firm]

FUND THESIS (public)
[What they say they invest in — from website, interviews, public writing]
[Any stage/check-size/geo focus visible from public sources]

RECENT PORTFOLIO ACTIVITY (free sources)
[List 2-4 recent investments or announcements found in public news]
- [Company] ([round], [approx date]) — [why this is relevant to BALBOA1 pitch]
- ...

KNOWN CO-INVESTORS
[Names of firms/people they frequently co-invest with — from news articles]

RELEVANT THESIS CONNECTIONS
[Specific, concrete ways their thesis maps to what Nick is building]
[Not generic — must cite a specific portfolio company or stated focus]

RECOMMENDED PITCH ANGLE
[One paragraph: how to frame BALBOA1 for this specific investor based on what you found]

PAYWALLED DATA (not available in free tier)
[Be specific about what's missing:]
- [ ] Full portfolio list: visible on Crunchbase Pro / PitchBook
- [ ] Fund size: not publicly disclosed
- [ ] Cap table details: require paid access
- [ ] Co-investor breakdown: partial (some from news, full picture needs paid tool)
```

---

## Step 1: Find the contact in the CRM

Look them up in the Venture & Investment or OTC & Market Makers silo. Read their Enrichment column (col P) — use existing context, don't duplicate work.

## Step 2: Run targeted searches (max 3)

**Search 1 — Person + firm background:**
`"[Name]" "[Firm]" portfolio investment thesis`

**Search 2 — Recent activity:**
`"[Firm]" funding announcement OR portfolio news [current year]`

**Search 3 — Crunchbase public page (if VC):**
Navigate to: `crunchbase.com/person/[name-slug]` or `crunchbase.com/organization/[firm-slug]`

Read what's publicly visible without logging in. Basic info (title, firm, sometimes recent investments) is free. Flag anything behind the "Upgrade to see more" wall.

Do NOT run more than 3 searches. If the signal is thin after 3, note it and move on.

## Step 3: Identify thesis connections

This is the most valuable part. Look for specific, non-obvious connections:

- A portfolio company that operates in a similar space (maritime, trade finance, payments rails, LatAm, stablecoins, RWA)
- A thesis statement that directly maps to Nick's pitch
- A co-investor they work with who might know Nick's project
- A recent fund announcement that signals they're actively deploying in this category

Generic connections ("they invest in fintech and Nick is in fintech") don't count. Specific ones do.

## Step 4: Write the research block

Write the full research block (see format above) to col Q of the contact's row.

Use language like "Based on public sources as of [date]" to set expectations on data freshness.

## Step 5: Flag paywalled data clearly

For each item that would provide meaningful signal but is behind a paywall, add it to the PAYWALLED DATA section with:
- What the data is
- Which tool has it (Crunchbase Pro, PitchBook, Dealroom, LinkedIn Sales Navigator)
- Whether it's worth paying for given where this contact is in the pipeline

Rule of thumb: If the contact is Tier 0 and a meeting is already scheduled, a one-time Crunchbase Pro lookup (~$0 if you use the free trial) might be worth it. For Tier 3 contacts still at Stage 1, skip it.

## Standing rules

- Never invent data. If you can't find it in public sources, say so.
- Never claim a firm "recently invested in X" without citing a specific article or announcement.
- Crunchbase free tier shows limited data — describe what you saw, not what might be there.
- If the person has almost no public footprint (common for LP-facing allocators, family offices), note this explicitly and recommend a different enrichment approach (mutual connection, direct conversation).
