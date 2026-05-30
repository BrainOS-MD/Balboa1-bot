---
name: content-generation
description: Generates copy-paste-ready content for 5 platforms daily: X (personal), LinkedIn (personal), LinkedIn (company), Substack (personal), and Company Blog. Runs live research for relevant news, checks JARVIS bridge for current thinking, and produces a content waterfall from one research session. Activate when Nick types "content" or during the daily briefing. Uses two distinct brand voices — Nick personal (operator, crypto-native) and BALBOA1 institutional (compliance-safe). Inspired by claude-blog's research→brief→write→review pipeline and content-creator's multi-platform adaptation patterns.
---

# BALBOA1 Content Generation Skill

## Architecture: The Waterfall

One daily research session → one content brief → five platform-adapted outputs.

Research once. Publish everywhere. This is the efficiency.

```
RESEARCH (live web search + Jarvis bridge)
    ↓
BRIEF (the One Thing, the proof, the angle)
    ↓
WATERFALL
    ├── X thread (personal @stupoorcycle)
    ├── LinkedIn personal (nicksmarton)
    ├── LinkedIn company (Balboa Corp)
    ├── Substack personal
    └── Company Blog (SEO-optimized)
```

## Step 1: Daily Research Session

Run live web searches. Use 4 search queries maximum (one per topic cluster):

**Query 1 — Stablecoin/Regulatory pulse:**
Search: `stablecoin news [current month year]` OR `GENIUS Act update [year]`

**Query 2 — Maritime/Trade finance pulse:**
Search: `maritime trade settlement payments [year]` OR `Panama Canal trade news [current month]`

**Query 3 — LATAM/Crypto funding:**
Search: `LatAm fintech investment [year]` OR `RWA stablecoin funding [year]`

**Query 4 — Competitor/Market signals:**
Search: `USDC USDT institutional adoption [year]` OR `vertical stablecoin launch [year]`

Also check for JARVIS bridge file at `~/JARVIS-vault/03-BRIEFS/_balboa-bridge.md`. If it exists and is dated within 7 days, read it. Nick's current thinking seeds the content.

### Identify the day's best angle

From research + Jarvis bridge, pick ONE of these:

**A. News reaction** — a development just happened that Nick has a real take on
**B. Contrarian insight** — something most people in this space believe that Nick disagrees with (and can prove)
**C. Behind-the-scenes** — something real from building BALBOA1 right now (if Jarvis bridge has a relevant capture)
**D. Data point** — a number from research that tells a surprising story
**E. Explainer** — a concept that's misunderstood in Nick's space that he can clarify

Pick the type that has the most genuine signal today. Don't force a take.

## Step 2: The Content Brief (internal)

Before writing any platform draft, create the internal brief. Never skip this.

```
ONE THING: [single sentence — the idea the content is built around]
PROOF: [specific number, example, or named fact that proves it]
READER TRANSFORMATION: [what they know/feel at the end that they didn't before]
BEST HOOK (personal): [for Nick's personal voice]
BEST HOOK (company): [for BALBOA1's institutional voice — if applicable]
COMPLIANCE RISK: [any claims that need fact-checking before the company content goes out]
```

## Step 3: Write the Waterfall

### 🐦 X Thread — Personal (@stupoorcycle)

Voice: casual, crypto-native, direct, can be contrarian. Think "thread someone saves."
Format: 5–8 tweets. 280 chars max each.

Structure:
- **Tweet 1**: The hook. Creates tension or surprise. Must make someone stop.
- **Tweets 2–5**: One concrete point per tweet. Each one standalone.
- **Tweet 6** (optional): The nuance / counter-argument
- **Final tweet**: The reframe + "Follow @stupoorcycle for more on [topic]."

Do NOT use: "thread 🧵", "1/", excessive emojis, "WAGMI", outdated slang.
DO use: real numbers, named examples, opinions stated as opinions.

---

### 💼 LinkedIn Personal — nicksmarton

Voice: sharp operator. High signal, low noise. Like a smart person texting a peer, not writing an essay.
Format: 150–300 words. No sub-headers. Prose or minimal bullets if the content is genuinely list-shaped.

Structure:
- **Line 1**: The hook. Never "I've been thinking about" or "I'm excited to share."
- **Body**: 2–3 paragraphs. The One Thing made concrete with proof.
- **Close**: a question, a reframe, or an invitation to debate.

---

### 🏢 LinkedIn Company — Balboa Corp

Voice: institutional thought leadership. Sounds like a well-run company. Data-backed.
Format: 100–200 words max.

COMPLIANCE RULES (non-negotiable):
- Every factual claim sourced from `context/balboa1_facts.md`
- NO price speculation or yield forecasts
- NO unconfirmed traction claimed as live (the LOI is "LOI signed" not "3,000 vessels using BALBOA1")
- NO competitor names used disparagingly
- Use "regulated digital settlement" not "crypto"
- GENIUS Act / Panama IBC framework may be mentioned by name — both are publicly documented

Structure:
- **Line 1**: A market observation or industry fact (not a product pitch)
- **Body**: How this connects to what BALBOA1 is building
- **Close**: A soft CTA ("Following our pilot announcements? DMs open.")

---

### 📧 Substack — Personal (Nick Marton)

Voice: long-form operator essay. Personal + analytical. "What I'm learning building X right now."
Format: 700–1500 words. Think: something worth reading on a Sunday morning.

Structure:
1. **Title**: specific, not clickbait. ("Why Panama's IBC structure is the unlock most stablecoin founders miss")
2. **Intro**: the tension or question this essay addresses — pull the reader in with a specific scenario
3. **What I saw**: Nick's specific observation (from research or Jarvis capture)
4. **The deeper pattern**: what it means in the broader context
5. **The implication**: what to do with this information
6. **Closing line**: the reframe or provocative final thought
7. **CTA**: "Subscribe for more from the trenches." (do not beg for subscribers)

---

### 📝 Company Blog — Balboa Corp

Voice: educational, trust-building, SEO-optimized. Written for: maritime operators, OTC desks, VCs researching the space.
Format: 900–2000 words. Answer-first structure (TL;DR at top, SEO title includes primary keyword).

Structure (from claude-blog's answer-first pattern):
1. **SEO Title**: Primary keyword + specific (not clickbait)
2. **Meta description**: Under 160 chars with keyword
3. **TL;DR** (2–3 sentences): What the reader will learn — answer-first
4. **The Problem**: Make the reader feel the friction (3–4 paragraphs)
5. **The Insight**: The One Thing with proof (3–4 paragraphs)
6. **Maritime Application**: How this applies specifically to their operational reality
7. **What to Do Next**: CTA — pilot program, contact, subscribe to updates
8. **Related reading** (optional): Link to 2–3 internal or credible external sources

COMPLIANCE RULES: same as LinkedIn Company above, plus:
- All statistics need source citation inline
- No unverifiable claims about the state of BALBOA1's launch

---

## Step 4: Quality Check (from claude-blog's review pattern)

Before presenting drafts, self-review:

**Personal content (X, LinkedIn personal, Substack):**
- [ ] Every claim is concrete (no vague claims like "significant" or "many")
- [ ] Nick's voice feels like Nick, not like an AI newsletter
- [ ] No banned phrases present
- [ ] The hook would actually stop a scroll

**Company content (LinkedIn company, blog):**
- [ ] Every factual claim verifiable against `context/balboa1_facts.md`
- [ ] No compliance risk flags left unaddressed
- [ ] No price speculation or forward-looking traction claims
- [ ] Reads like a company with institutional credibility, not a hype project
- [ ] SEO title includes a keyword someone would actually search

## Step 5: Output format in the daily brief

```markdown
## 📝 Content — [Date]

**Today's angle:** [Type A/B/C/D/E + one sentence on what the day's content is about]
**Research source:** [the 1-2 articles/data points this content is built from]
**Jarvis bridge:** [yes/no — if yes, which insight is being used]

---

### 🐦 X Thread
> Tweet 1: [text]
> Tweet 2: [text]
> ...

### 💼 LinkedIn Personal
[draft — copy-paste ready]

### 🏢 LinkedIn Company
[draft — copy-paste ready]
⚠️ COMPLIANCE CHECK: [any flags]

### 📧 Substack
**Title:** [title]
[draft — full text]

### 📝 Company Blog
**Title:** [title]
**Meta:** [description]
[draft — full text]
```

## Standing rules

If there is no strong angle from research today (happens), don't force content. Tell Nick: "No strong signal today — archive day or pick from Jarvis backlog." Better to skip a day than post weak content.

The BALBOA1 company voice is conservative by design. When in doubt, cut rather than add.
