# Command: `reply-to [NAME]`

When Nick gets a reply and types `reply-to NAME`, draft his response.

## Step 1: Find the contact + their reply

Search silo tabs for NAME. Read:
- Their Status (col B)
- Their Reply Snippet (col O) — what they said
- Their Enrichment (col P)
- The most recent draft Nick sent (look in Drafts Log, filter by Contact Name, sort by Date desc)

If Reply Snippet is empty, ask Nick: "What did [Name] say? Paste their reply here."

## Step 2: Classify the reply

Read the snippet and classify into one of:

### A. Interested — wants to schedule
**Signal:** "Let's chat" / "What times work" / "Send me a calendar link" / "Happy to talk"
**Response strategy:** Send Calendly link. Reaffirm the value they signaled interest in. Suggest specific times. Under 60 words.

### B. Interested — asks a question first
**Signal:** "Tell me more about [X]" / "What's your model" / "How does this differ from USDC" / "Who's on your team"
**Response strategy:** Answer their specific question with concrete proof points from `context/balboa1_facts.md`. End by re-asking for the call. Under 120 words.

### C. Interested — wants materials first
**Signal:** "Send me the deck" / "Got a one-pager" / "Where can I read more"
**Response strategy:** Send the materials. Set up the call as the next step. Under 50 words.

### D. Not now — leave door open
**Signal:** "Not focused on [sector] right now" / "Check back in [timeframe]" / "Let me sit with this"
**Response strategy:** Acknowledge gracefully. Offer to send a brief update in [their timeframe]. Don't push. Under 50 words.

### E. Hard no
**Signal:** "Not a fit" / "Don't invest in [sector]" / "Pass"
**Response strategy:** Thank them sincerely, no fight. Ask if they know anyone else for whom it might be a fit (low-cost referral ask). Under 40 words.

### F. Needs clarification on a misunderstanding
**Signal:** They've misread something (e.g., think it's retail, think it's a Bitcoin thing, think you're another stablecoin)
**Response strategy:** Correct the misunderstanding directly without being defensive. Re-frame in one clean sentence. End with the ask. Under 80 words.

### G. Ambiguous or unclear
Ask Nick to clarify what category they're in. Don't draft yet.

## Step 3: Draft using the right tone

Read `context/founder_voice.md` and match the formality level the contact used. If they wrote a short casual line, match short casual. If they wrote formal, match formal.

The reply gets its own Variant ID: `VR-[response category letter]-[short slug]`. Examples: `VR-A-calendly`, `VR-B-genius-act`, `VR-F-not-retail`.

## Step 4: Output

Show Nick:
```
Reply category: [A-G]

Draft response (`[Variant ID]`):
> [draft]

Suggested next-step status change:
[Their next state in the pipeline — e.g., "Set to 5. Meeting Requested if they accept the time"]
```

## Step 5: Log

Append the draft to the Drafts Log:
- Touch Type: `Reply Response`
- Variant ID: `VR-...`
- Outcome: leave blank until Nick reports back

## Edge case: Reply requires info you don't have

If the reply asks something specific that's NOT in `context/balboa1_facts.md` (e.g., "What's your team's background?" and you don't have team bios), don't fabricate. Tell Nick:
```
⚠️ Reply asks about [specific thing]. I don't have that in my context. 

Can you tell me [specific question] so I draft accurately?
```
