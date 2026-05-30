---
name: meeting-prep
description: Prepares Nick for a specific upcoming call by connecting dots across the contact's enrichment, JARVIS captures, live news, and BALBOA1 proof points into a structured pre-call brief with talking points and anticipated objections. Activate when Nick types "meeting-prep [NAME]". No fluff — only what's actually useful to have in your head before a call.
---

# Meeting Prep Skill

## Trigger

`meeting-prep [NAME]`

Produces a focused pre-call brief, delivered directly in the terminal. Save or copy-paste as needed.

---

## Step 1: Find the contact

Search all silo tabs for NAME. Read their full row: Status, Enrichment (col P), Notes (col Q), LinkedIn URL, Company, Title, Silo.

Also check the Drafts Log for the conversation history: what was sent, what they replied, what stage the relationship is at.

## Step 2: Read the JARVIS bridge

If `~/JARVIS-vault/03-BRIEFS/_balboa-bridge.md` exists and was updated in the last 14 days, read it. Look for any of Nick's recent thinking that connects to this person's world. A live question from JARVIS ("I've been thinking about [X]...") can be a great opener or conversation anchor.

## Step 3: Run one targeted web search

Search: `"[Company]" [relevant angle] news OR funding OR announcement [current month year]`

This is one search maximum. Use it to find the most recent publicly relevant development at their firm or company. No more than 1 search — this prep should be fast.

## Step 4: Build the pre-call brief

```markdown
# Pre-Call Brief: [Name] · [Title] · [Company]
**Date:** [today]  
**Silo:** [silo]  
**Call type:** [inferred from stage — e.g., "First intro call", "Pitch meeting", "Follow-up after interest shown"]

---

## 30-Second Context
[2-3 sentences max. Who they are, why this call matters, what success looks like.]

---

## Their World Right Now
[2-3 bullets on what's happening at their firm/company based on enrichment + news search]
- [specific recent thing]
- [their stated focus or thesis]
- [any relevant market context]

---

## The Call Angle
**What Nick is there to do:**
[One sentence. Is this a pitch? A conversation to test fit? A relationship-building call? A follow-up to a specific question they asked?]

**The BALBOA1 proof point most relevant to them:**
[Pull from project_facts.md — the ONE fact that lands best for this specific person]

**What they care about that BALBOA1 connects to:**
[The bridge between their world and your project — from Notes column or Enrichment]

---

## 5 Talking Points

1. **[Opening hook]** — [What to say first. Reference something specific to them.]
2. **[The ask/angle]** — [The core thing you're there to communicate or get.]
3. **[Proof point]** — [The concrete proof that supports the angle.]
4. **[Their objection, answered]** — [See below — lead with the most likely objection and your answer.]
5. **[The close]** — [What you're asking for at the end of the call: investment conversation, intro, pilot, follow-up meeting, feedback.]

---

## Anticipated Objections + Responses

[Pull from project_facts.md's objections section + infer from their silo type]

| Objection | Response |
|-----------|----------|
| [Likely objection 1] | [Concise, proof-based answer] |
| [Likely objection 2] | [Concise, proof-based answer] |
| [Likely objection 3] | [Concise answer — be honest if the answer is "we're still early on that"] |

---

## JARVIS Connection

[If JARVIS bridge found a relevant capture or question:]
**Current thinking that's relevant:** "[Nick's live question or idea from JARVIS that ties to this call]"
Use this as a conversation thread if the opportunity arises. It makes the conversation feel genuine.

[If no JARVIS content relevant: skip this section]

---

## Don't Forget
- Ask for: [one specific next step Nick should request before hanging up]
- Send after the call: [any follow-up they asked for, or a post-meeting note referencing the specific thing discussed]
- Calendar: calendly.com/nick-balboacorp/30min [if scheduling a follow-up]
```

---

## Quality bar

A good pre-call brief makes Nick feel prepared in 5 minutes. It should NOT:
- Repeat information Nick already knows
- Fill talking points with generic fintech claims
- Use vague language like "discuss potential synergies"

It SHOULD:
- Give at least one specific recent fact about their world
- Identify the one most important thing to communicate
- Surface at least one objection they're likely to raise

If the contact has no Enrichment or Notes data, run the enrichment workflow first (`enrich-contact [NAME]`) and return to meeting prep after. Don't write a generic brief — that's worse than no brief.
