# Command: `enrich-contact [NAME]`

When Nick types `enrich-contact NAME`, execute this workflow.

## Step 1: Find the contact

Search across all 5 silo tabs for a row where Name (col D) matches NAME (fuzzy match — be lenient on casing and middle names).

If multiple matches, ask Nick which one.
If no match, ask Nick which silo to add them to and capture: Name, Title, Company, LinkedIn URL, X handle.

## Step 2: Determine the enrichment path

Read `skills/contact-enrichment/SKILL.md` for the full method. Quick routing:

- **Tier 0 or Tier 1 contact:** Suggest Nick use Claude in Chrome (paste the prompt template below to him). Pause and wait for him to paste the result back.
- **Tier 2 with public X/podcast presence:** Do a web search yourself.
- **Tier 3-4 warm contact:** Ask Nick what he remembers about them.
- **Tier 3-4 cold:** Do a quick web search; if nothing strong comes back, flag as "minimal public footprint" and continue.

## Step 3: For Claude-in-Chrome path

Tell Nick:
```
I'll write the enrichment for you. To do this, open [LinkedIn URL] in Chrome 
(logged in as you), open Claude in Chrome, and paste this prompt:

---
Summarize this LinkedIn profile for cold outreach personalization. I need:
- About section (1-2 sentence summary)
- 3 most recent posts (topic + 1-line summary each)
- Patterns in what they engage with (likes, comments, reposts) — surface themes
- The single strongest hook for outreach about: regulated Panama stablecoin for 
  maritime trade settlement with a 3,000-vessel LOI

Format as a 4-line blob:
About: ...
Recent activity: ...
Patterns/Focus: ...
Hook: ...
---

Paste the result back here and I'll save it to the Sheet.
```

When Nick pastes the result, save it to the Enrichment column (col P) with today's date.

## Step 4: For web-search path

Execute these queries (cap at 3 to manage tokens):
1. `"[Name]" "[Company]" interview OR podcast OR thread`
2. `[X handle] stablecoin OR RWA OR maritime` (only if X handle is in the Sheet)
3. `"[Company]" recent investment OR portfolio` (only for VC contacts)

Synthesize results into the 4-line enrichment blob format (see `skills/contact-enrichment/SKILL.md`).

Save to Enrichment column with today's date.

## Step 5: For warm contact path

Ask Nick:
```
What do I need to know about [Name] for outreach?
- Where did you meet?
- What do they care about?
- Anything they've shared recently that's relevant?
- Any other mutual context?
```

Convert Nick's verbal answer into the 4-line enrichment blob format. Save to Sheet.

## Step 6: Confirm

Reply to Nick:
```
✅ Enriched [Name] in [Silo] tab.

Saved enrichment blob:
[the blob]

Want me to draft outreach to them now?
```

If Nick says yes, draft the connection request and intro message immediately using `skills/investor-outreach/SKILL.md`.
