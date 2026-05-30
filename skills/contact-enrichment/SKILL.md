---
name: contact-enrichment
description: Pulls public information about a contact (LinkedIn About, recent posts, X activity, podcasts, portfolio investments) so outreach drafts can be personalized. Uses free sources only — Claude in Chrome, web search, manual paste-in, Google Alerts. Activate when drafting outreach to a contact whose Enrichment column is empty, or when Nick runs `enrich-contact [NAME]` directly.
---

# Contact Enrichment Skill

## What "enrichment" means here

A 200–600 character text blob, written by you, stored in the contact's `Enrichment` column (col P) on their silo tab. Format:

```
[About summary, 1-2 sentences]. Recent activity: [post/quote/topic 1] · [topic 2]. Portfolio/focus: [if VC, list 2-3 recent investments rhyming with BALBOA1]. Hook: [the single best angle for cold outreach to THIS person].
```

Example for Joe Lonsdale (8VC):
```
Co-founder Palantir & 8VC. Vocal on supply chain reshoring, US industrial base, dollar dominance. Recent activity: argued for US-anchored stablecoins on X · Posted thread on logistics fragility. Portfolio rhymes: Flexport, Anduril, Epirus. Hook: dollar dominance + supply chain hardening — BALBOA1 is regulated USD stablecoin capturing $300B Panama trade flow, infrastructure not speculation.
```

That blob lets the bot draft personalized DMs forever without re-fetching.

## The free enrichment stack

Use these in order of leverage. Stop once you have enough for a strong personalization line.

### 1. Claude in Chrome (highest leverage, best for top tiers)

For Tier 0 / Tier 1 contacts, Nick should run Claude in Chrome (beta in his Claude app):

**Workflow Nick will execute:**
1. Open the contact's LinkedIn profile in Chrome (logged in as Nick)
2. Open Claude in Chrome extension
3. Prompt: `"Summarize this profile for outreach: About section, 3 most recent posts, and any patterns in what they engage with. Output as the enrichment blob format from skills/contact-enrichment/SKILL.md."`
4. Copy the output
5. Paste into the Enrichment column for that contact in the Sheet

**Time per contact:** 90 seconds.
**Use for:** Tier 0 (5 contacts), Tier 1 (20-30 contacts). Total: ~45 minutes one-time investment for top 30.

### 2. Web search via Claude (best for VC partners with public footprint)

For any contact at any tier, when drafting outreach, run a web search if Enrichment is empty.

Search patterns that work:
- `"[Name]" "[Firm]" interview` → podcast appearances, often the richest source
- `"[Name]" thesis stablecoin OR RWA OR fintech` → their writing
- `"[Firm]" recent investment [year]` → portfolio additions
- `[X handle] stablecoin OR maritime OR Panama` → recent X activity if they're public
- `[Name] [Firm] LinkedIn` → fallback to find the profile if Nick hasn't linked it

Cap web search at 2 queries per contact during a briefing — token budget matters.

Synthesize results into the enrichment blob format. Write it back to the Sheet so we don't re-search next time.

### 3. Manual paste-in (best for warm/general contacts)

For warm contacts Nick already knows, ask Nick directly:
```
"What do I need to remember about [Name]? Where did you meet, what do they care about, anything they've shared recently?"
```

Convert Nick's verbal context into the enrichment blob format. Save to Sheet.

### 4. Google Alerts (passive, set-and-forget)

Once per silo, set up Google Alerts for ongoing intelligence:
- Firm name (e.g., "Castle Island Ventures")
- Key contact name (e.g., "Nic Carter")
- Topic keyword overlap with BALBOA1 (e.g., "Panama stablecoin", "maritime trade finance")

Send alerts to a dedicated Gmail folder. Once a week, scan the digest and add fresh activity to the Enrichment column of mentioned contacts. This is how the enrichment data stays current over months.

**Nick's one-time setup (15 min):** [google.com/alerts](https://google.com/alerts) → create alerts for top 10 firms + 5 topic queries.

### 5. X / Twitter (free, manual)

For OTC desks, market makers, and crypto-native traders, X is where the action is. No paid API. Workflow:

- Search the contact on X (or use their handle from the Sheet)
- Read their last ~10 posts
- Note: what they're posting about, what they engage with, any references to stablecoins/RWA/payments
- Convert to enrichment blob

For high-volume DM campaigns to X followers (your @stupoorcycle followers), use the patterns in the `Twitter DM Campaign.md` reference doc — but the bot drafts fresh per contact, never copy-pastes templates.

## What NOT to do (and why)

❌ **Don't use Apify or any paid LinkedIn scraper.** Risk to Nick's 750-connection personal LinkedIn is too high. A flagged or banned account loses years of relationship-building.

❌ **Don't pay for the Twitter/X API.** $200/mo for basic tier returns minimal value for a cold DM workflow. Free manual reading is enough.

❌ **Don't fabricate enrichment.** If a contact has zero public footprint and Nick has no warm context, write `Enrichment: minimal public footprint; cold outreach needs to lead with proof points, not personalization.` and the bot will compensate in the draft.

❌ **Don't enrich the long tail.** 490 general contacts × 90 seconds = 12 hours. Only enrich contacts being actively drafted to. Lazy enrichment.

## Output: writing back to the Sheet

When you complete enrichment for a contact, update the Sheet:
1. Find the contact's row across silo tabs (search by Name in col D)
2. Write the enrichment blob to col P
3. Note the date of enrichment in col P after the blob: `... [enriched YYYY-MM-DD]`

## Refresh cadence

Enrichment goes stale. For Tier 0 / Tier 1 contacts:
- Re-enrich every 60 days (the bot tracks via the date stamp in col P)
- If a Tier 0 contact's enrichment is >60 days old, the bot's briefing flags it: "⚠️ Enrichment for [Name] is [X] days old — consider re-running Claude in Chrome before next outreach."

For Tier 2+ contacts, don't refresh unless they reply.
