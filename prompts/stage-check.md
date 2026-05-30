# Prompt: `stage-check`

**Triggers:** `stage-check` command OR automatic during `briefing` when Stage 2/3 contacts detected.

---

## Part A: Stage 2 — Connection Request Status Checks

When Nick types `stage-check`, or when the briefing detects Stage 2 contacts with Next Action Date ≤ today:

### Step 1: Find Stage 2 contacts due for a check

Scan all silo tabs. Find contacts where:
- Status = `2. Request Sent`
- Next Action Date ≤ today (or Next Action Date is empty, which means the 7-day auto-set hasn't run yet)

### Step 2: For newly-Stage-2 contacts (no Next Action Date set)

If any Stage 2 contact has an empty Next Action Date column, write `=TODAY()+7` to their Next Action Date cell. This happens silently — no need to notify Nick unless there are many of them.

### Step 3: Present the check list

For each Stage 2 contact where Next Action Date ≤ today, output:

```
─────────────────────────────────────────────
📎 [Name] · [Title] · [Company]
   Sent: [Last Touch Date or "date unknown"]
   Days since sent: [N]
   LinkedIn: [URL or "not on file"]
   Action: Open their profile. Check if the Connect/Pending button changed to Message.
─────────────────────────────────────────────
```

At the bottom:
```
For each contact above, reply:
  y [name]   → mark as connected (Status → 3. Request Accepted)
  n [name]   → still pending (push Next Action Date +7 days)
  skip [name] → leave unchanged

Or: "all connected" / "none connected"
```

### Step 4: Process Nick's responses

When Nick replies with y/n/skip for each name:

**If "y" (accepted):**
- Update Status to `3. Request Accepted`
- Clear the Next Action Date (it will be reset by Stage 3 logic)
- Queue this contact for enrichment (see Part B)
- Confirm: "✓ [Name] marked as accepted — will enrich and draft intro DM in this session"

**If "n" (still pending):**
- Keep Status at `2. Request Sent`
- Push Next Action Date to today + 7
- Confirm: "↻ [Name] — checking again in 7 days"

**If "skip":**
- Leave everything unchanged
- Confirm: "⏭ [Name] — skipped"

---

## Part B: Stage 3 — Auto-Enrichment + Intro DM

Runs automatically for any contact at Status `3. Request Accepted` with an empty Enrichment column. This triggers during the daily briefing OR after Part A marks someone as accepted.

### Step 1: Gather enrichment material

For each Stage 3 contact needing enrichment:

**Token-optimized firm-first approach:**
1. Check if another contact at the same firm was already enriched this session. If yes, reuse the firm-level context.
2. If not: web search `"[Company]" [relevant angle: stablecoin OR maritime OR payments OR VC thesis]`
3. Then: web search `"[Name]" "[Company]" background` for individual-level context

Limit to 2 searches per contact maximum.

### Step 2: Write the Enrichment blob (col P)

Format:
```
About: [1-2 sentence summary of the person]. Recent activity: [topic 1] · [topic 2]. Focus: [their firm's investment thesis or operational area]. Hook: [the single best angle for Nick to lead with].
[enriched YYYY-MM-DD]
```

Write this to col P of their row.

### Step 3: Write the Notes & Research blob (col Q)

This is more detailed than the enrichment blob. It's the full research summary for this contact.

Format:
```
BACKGROUND
[3-5 sentences on the person's background and current role]

FIRM CONTEXT
[2-3 sentences on their firm's thesis, recent investments, or operational focus]

SYNERGIES WITH BALBOA1
[Specific, concrete connections between their work and BALBOA1's story — not generic]

RECOMMENDED ANGLE
[One clear pitch/partnership/intro angle based on what you found]
[What proof point from project_facts.md is most relevant for this person]

RESEARCH GAPS
[What would make this stronger — what couldn't be found via free web search]
```

Write this to col Q of their row.

### Step 4: Draft the intro DM

Now write the first real message Nick will send after connecting. Follow all rules from `skills/investor-outreach/SKILL.md`.

This is NOT a connection request. The connection is already accepted. This is the intro.

Key requirements:
- Opens with the Hook from the enrichment blob
- References one specific thing from their recent activity
- Includes one concrete BALBOA1 proof point (from project_facts.md)
- Ends with a specific ask (15-min call with specific days, or a specific question)
- Under 120 words
- Assign Variant ID: `VL4-[slug]` (VL = LinkedIn, 4 = Stage 4 intro)

### Step 5: Mark stale connection-request drafts as superseded

In the Drafts Log tab, find any rows where:
- Contact Name matches this person
- Touch Type = "Connection Request"
- Outcome is blank

Update their Outcome to `Superseded — contact accepted`.

This prevents the bot from re-drafting connection request messages for people who are already connected.

### Step 6: Output in the briefing

The intro DM draft appears in the `🔥 Priority Actions` section:

```
### [Name] · [Company] · Stage 3 Enriched
**Enrichment:** [one-line summary]
**Notes written to Sheet:** ✓
**Intro DM (VL4-[slug]):**
> [draft]
```

---

## Auto-Set Logic (runs silently in every briefing)

Every time `briefing` runs, before generating any drafts:

1. For every contact newly moved to Stage 2 (Next Action Date empty): write `today + 7` to Next Action Date
2. For every contact at Stage 3 with empty Enrichment: queue for enrichment (Part B above)
3. Write all updates back to the Sheet in one batch call (not one cell at a time)

This keeps the Sheet in sync without Nick having to trigger anything manually.
