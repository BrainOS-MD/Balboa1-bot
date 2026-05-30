---
name: networking
description: Generates 5 LinkedIn messages, 5 X DMs, and 5 email drafts daily to warm 1st-degree contacts for relationship maintenance — not outreach, not pitching. Messages share genuinely relevant finds, reference mutual context, and keep Nick top-of-mind with his network. Source pool: General Contacts + anyone at stage 3+ across all silos. Uses Jarvis bridge for smart connections. Platform tones: X = super casual, LinkedIn = sharp and high-signal, Email = personal.
---

# Networking Skill — Smart Warm Relationship Maintenance

## What this is NOT

This is not investor outreach. That's handled by `skills/investor-outreach/SKILL.md`.

This is relationship maintenance — the practice of staying genuinely connected to the people in Nick's network. The goal is to be someone people are glad to hear from, not someone who only appears when they want something.

## What a good networking message looks like

It does ONE of these things:
1. Shares something specific that the recipient would find genuinely useful or interesting (not generic fintech news)
2. References something they said/posted recently and adds to it
3. Asks a specific question Nick is actually working through (using Jarvis live questions)
4. Reconnects with a personal reference ("reminded me of our conversation about X")
5. Makes a connection between two people in Nick's network who should meet

What it does NOT do:
- Pitch BALBOA1 (unless they specifically asked last time — check the CRM)
- Send the same message to multiple people
- Say "just checking in" with no reason
- Be longer than it needs to be

## Step 1: Select 15 contacts

Source pool (in priority order):
1. Anyone across all silo tabs with Status ≥ "3. Request Accepted" AND Last Touch Date > 21 days ago (meaning they've gone quiet but there's an existing connection)
2. General Contacts tab — contacts with known X/LinkedIn handles
3. Anyone where the Reply Snippet column has an unaddressed response

For each platform (LinkedIn, X, Email), pick 5 contacts who:
- Have an active presence on that platform
- Have something concrete Nick can reference (post, article, project, mutual topic)
- Haven't received a networking message from Nick in the last 30 days (check Drafts Log)

Cap at 15 total unique contacts per day across all 3 platforms. Don't message the same person on two platforms the same day.

## Step 2: Find the hook for each contact

For each of the 15 selected contacts, find ONE of these:

**A. Live news relevant to their world**
Web search: `"[their industry/role]" news [current month year]`. Pull the most interesting development. Is there a GENIUS Act update that hits their space? A maritime shipping development? A LatAm fintech raise?

**B. Something they posted recently**
If they have an X or LinkedIn handle, search for their recent activity. What have they been saying? Can Nick add to it, react to it, or take an interesting position?

**C. A live question from Jarvis bridge**
If `~/JARVIS-vault/03-BRIEFS/_balboa-bridge.md` exists and has live questions, use them: "I've been thinking about [question] — given your background at [company], curious your take."

**D. A connection to make**
Does Nick know two people who should meet? Introduce them. The message goes to the person being introduced, not the one doing the introducing.

**E. A personal recall**
Something from the Enrichment column or Notes that connects to something happening now. "Remember when you mentioned X — looks like [related thing] just happened."

If none of these five apply, skip this contact today and pick someone else.

## Step 3: Write the messages

### LinkedIn (5 messages)

Voice: sharp, high-signal, peer-to-peer. Sounds like a smart operator tapping a colleague on the shoulder. NOT a newsletter, NOT a pitch, NOT a press release.

Format: 3–6 sentences max. No fluff opener. Direct reference in the first sentence.

Skeleton:
```
[Reference their recent work / a shared context / a news item relevant to them] — [Nick's specific take or connection in 1-2 sentences]. [An honest question or a natural next step — "curious what you think" or "made me think of our conversation about X"].

— Nick
```

Examples of good openers:
- "Saw your post on [specific topic] — the [specific point] is something I've been seeing from the Panama side too."
- "This GENIUS Act implementation guidance that dropped [yesterday/this week] seems directly relevant to what you're building at [company] — wanted to flag it."
- "[Mutual person] mentioned you're working on [thing] — completely unrelated but I've been thinking about [Jarvis question] and your background at [firm] is exactly the vantage point I'd want."

---

### X DMs (5 messages)

Voice: super casual, crypto-native. Think: a DM from someone you follow who has a take worth hearing.

Format: 2–4 sentences. No formal structure. Direct.

Skeleton:
```
hey [name] — nick from @stupoorcycle. [the one real thing Nick wants to share or ask]. [optional: a question or a link they'd actually want]
```

Examples:
- "hey [name] — nick from @stupoorcycle. that thread you did on [topic] was sharp, especially [specific point]. been thinking about how that applies to [thing Nick is working through] — got a hot take on [specific aspect]?"
- "hey [name] — saw [news item] just dropped. given what you posted about [their topic] a few weeks back, thought you'd have thoughts. curious."
- "hey [name] — nick. genuinely been thinking about [Jarvis question]. you've been building in [their space] longer than most — how do you [specific question]?"

---

### Email (5 messages)

Voice: personal. Reads like a thoughtful note from someone Nick genuinely wants to stay connected with.

Format: 4–8 sentences. Has a subject line. Warmer than LinkedIn/X but still respects their time.

Subject: specific, not "checking in"
- "[Shared context] — quick note from Nick"
- "[Relevant news] — thought you'd want to see this"
- "[Their name], quick question"

Body skeleton:
```
[Name],

[Reference — one sentence on shared context, recent news, or mutual topic.]

[The thing Nick is sharing or asking — 2-3 sentences. Be specific. Include a link if relevant.]

[One honest question or natural invitation to respond — not "let me know if you want to catch up sometime."]

Nick
```

---

## Step 4: Personalization quality gate

Before including a message in the brief, it must pass:
- [ ] Opens with something specific to this person (not generic)
- [ ] Contains real information or a real question (not fluff)
- [ ] Under the word count cap for its platform
- [ ] Not already sent to this person in the last 30 days (check Drafts Log)
- [ ] Not accidentally pitching BALBOA1 (unless they're in the CRM as an active investor prospect AND previously showed interest)

If any message fails, rewrite it or swap the contact.

## Step 5: Output in the daily brief

```markdown
## 📡 Networking — [Date]

*15 warm contacts. Relationship maintenance only.*

### LinkedIn (5)

**[Name] — [Company] — [Hook type: A/B/C/D/E]**
> [draft — copy-paste ready]

**[Name] — [Company] — [Hook type]**
> [draft]

[× 5 total]

---

### X DMs (5)

**[@handle] — [Hook type]**
> [draft]

[× 5 total]

---

### Email (5)

**[Name] — [Subject]**
> [draft — includes subject line]

[× 5 total]
```

## Standing rules

Never fabricate context. If there's nothing genuine to say to someone today, skip them and pick another contact who has real connective tissue to something in Nick's world right now.

The networking messages should make the recipient think: "Good to hear from him." Not: "He wants something."

Rotate across the full General Contacts tab over time — don't message the same 15 people every week.
