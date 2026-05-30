---
name: grant-application
description: Drafts foundation grant applications, ecosystem program submissions, and follow-ups. Tracks deadlines and stages in the Grants Pipeline tab. Activate whenever Nick is applying for, following up on, or strategizing about grants (Ethereum Foundation, Arbitrum, Base, Optimism, RWA-focused DAOs, LATAM ecosystem programs). Different from investor outreach because grants are application-driven, not relationship-driven.
---

# BALBOA1 Grant Application Skill

## Core difference from investor outreach

Investor outreach = personalized DM, build relationship, ask for meeting.
Grant application = answer specific application questions, surface-level credibility through clean copy, deadline-driven, often anonymous review.

You're optimizing for: clarity, specificity, alignment to the grant's stated thesis, and obvious fit.

## Three primary tasks

### Task A: Draft a full grant application
Triggered by `grant-draft [GRANT NAME]`. 

### Task B: Follow up on a submitted application
Triggered when status = "Submitted" AND >30 days have passed.

### Task C: Identify which grants to apply to next
Triggered in weekly review or `prioritize-grants`.

---

## Task A: Drafting an application

### Step 1: Read the grant's application page
If the grant has an application URL in the Grants Pipeline tab, fetch and read it. Identify:
- The exact application questions they ask
- The stated thesis / what they fund
- The size of grant (helps frame ask)
- Deadlines / cohort timing
- Whether they require code, working product, or just a proposal

### Step 2: Map BALBOA1 to their thesis

Foundations fund what aligns with their narrative. Match your angle to theirs:

| Ecosystem | Lead angle |
|-----------|-----------|
| Ethereum Foundation (ESP) | Open financial standards. RWA primitive. ERC-20 settlement layer for maritime trade. Composability with existing DeFi infra. |
| Base / Optimism / Arbitrum (L2s) | High-volume real-world transactions routing through their execution layer. Captive B2B flow they don't currently capture. |
| Curve, Uniswap, Balancer | Deep, structural liquidity pools backed by real RWA collateral, not mercenary capital. |
| RWA-focused funds (Centrifuge, Goldfinch) | Trade finance asset class. Compliance-cleared issuance. Off-chain assets with verifiable settlement. |
| LATAM-focused funds (Kaszek, Magma, Valor) | Regional trade corridor infrastructure. Panama → US/EU/Asia flow. Underbanked SMB segment. |
| Public goods (Gitcoin, Octant) | Open-source escrow primitives. Compliance tooling reusable by other vertical stablecoins. |

### Step 3: Use the canonical proof stack

Every grant application draws from this list (sourced from `context/balboa1_facts.md`):

1. **Committed volume**: LOI with shipping consultancy for 3,000 vessels across Singapore, Vietnam, Dubai
2. **Active pilots**: Canal Authority and port operator conversations underway
3. **Regulatory structure**: Panama IBC inside the same legal framework as the Canal Authority
4. **Reserves**: Panamanian trust bank custody, monthly Proof-of-Reserves attestations
5. **Smart contract layer**: Escrow tied to bill of lading + customs clearance + delivery verification, with timeout-based return-to-buyer logic
6. **Multi-chain**: ERC-20 (Ethereum) + TRC-20 (TRON) at launch
7. **Market context**: $300B annual Panama trade flow, 13,400+ Canal transits, 8,000+ registered vessels
8. **Macro tailwind**: GENIUS Act passed July 2025, institutional stablecoin regulatory clarity
9. **Differentiated UX**: WhatsApp settlement notifications for crews on limited connectivity
10. **Team credibility**: Operator background ($100M+ revenue systems experience), Panama-based legal counsel, OTC desk partnerships in place

### Step 4: Draft structure for typical grant questions

Most grant applications ask 5–8 questions. Here are the most common with template answers:

#### "What is the project / one-line description?"
> BALBOA1 is a regulated 1:1 USD-backed stablecoin built for institutional maritime trade settlement. Launched from Panama with active pilots, BALBOA1 captures structural B2B payment volume across Canal tolls, bunkering, port disbursements, and trade-finance settlement that currently moves over slow, expensive SWIFT rails.

#### "What problem are you solving?"
> Maritime trade payments — Canal tolls, bunkering, port disbursements, container-level invoicing — move over 3–5 day SWIFT rails with $200–400 wire costs, break on weekends, and force vendors to absorb counterparty risk for work already completed. The Panama Canal alone runs $300B+ in annual trade flow across 13,400+ transits and 8,000+ registered vessels. This is captive, recurring, predictable institutional volume that has no native digital settlement primitive built for it. General-purpose stablecoins (USDT, USDC) don't solve maritime-specific friction: bill-of-lading-tied escrow, multi-party port settlement, jurisdictional clarity for Canal Authority-adjacent flows, or limited-connectivity UX for crews.

#### "Why is your team the right one to build this?"
> Operating Partner Nick Marton previously built revenue infrastructure for $100M+ pipelines, applying systems thinking to traditional B2B sales. The Panama-based team operates inside the same legal framework as the Canal Authority via the country's IBC structure. We have OTC desk partnerships already in place pre-launch, an LOI signed with a shipping consultancy handling payments for 3,000 vessels across Singapore, Vietnam, and Dubai (first committed volume), and active pilot conversations with Canal Authority and major port operators. Smart contract architecture is designed around how maritime payments actually flow — escrow release tied to bill-of-lading upload, customs clearance, and verified delivery, with WhatsApp settlement notifications for crews on limited connectivity.

#### "How will this benefit the [Ethereum/Base/Arbitrum/etc.] ecosystem?"
[Customize per ecosystem. Examples:]
> [For Ethereum]: BALBOA1 launches natively as ERC-20, routing structural B2B volume through Ethereum settlement. Maritime trade payments are non-speculative, recurring, and predictable — exactly the kind of real-world transaction volume Ethereum's RWA narrative needs. Our Curve pool integration deepens stablecoin liquidity with backed real-asset flow.
> [For Arbitrum/Base/Optimism]: We're evaluating L2 deployment for high-frequency, low-value maritime invoice settlement (bunkering line items, port service fees) that are uneconomic on L1. The captive B2B volume from our LOI partner alone represents thousands of monthly settlement transactions — direct execution-layer value for the L2.

#### "What is the milestone you'd use this grant for?"
Be specific. Foundations want to see concrete, dated milestones:
- "Q[X] 202[X]: Complete smart contract security audit ([firm name]) and deploy to [chain] mainnet"
- "Q[X] 202[X]: Onboard pilot partner [Name] processing first $[Y] of live volume"
- "Q[X] 202[X]: Deploy Curve pool and reach $[Z] in TVL"
Match the grant size to the milestone scale.

#### "How much are you requesting?"
Pull from the "Est. Size" column. Default to the middle of their stated range. Justify with the milestone.

### Step 5: Output format

Save the full draft as `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/JARVIS-vault/00-INBOX/_[DATE]-grant-[NAME].md`. Structure:

```markdown
# Grant Application Draft: [Grant Name]
**Deadline:** [date or "rolling"]
**Amount requested:** $[X]
**Status before this draft:** [from sheet]
**Application URL:** [url]

## Question 1: [Their exact question]
[Draft answer, 100-300 words, calibrated to their stated word limit if known]

## Question 2: [...]
[...]

## Suggested next action
- [ ] Nick reviews & edits
- [ ] Submit at [URL]
- [ ] Update Grants Pipeline tab: Status → "Submitted", Date Applied → today, Amount Requested → $X
```

Then update the Grants Pipeline tab in the Sheet: Status → "Drafting", Next Action → "Nick to review draft at 00-INBOX/_[DATE]-grant-[NAME].md"

---

## Task B: Follow up on a submitted application

If status = "Submitted" AND >30 days have passed, draft a brief follow-up:

```
[Greeting if you have a contact name],

I submitted BALBOA1's application to [Grant Name] on [Date Applied] and wanted to check on the status.

Since submission, [one concrete update — new partner / pilot transaction / regulatory milestone / audit completion].

Happy to provide any additional information that would help the review. 

Thanks,
Nick Marton
Operating Partner, Balboa Corp
```

Keep it under 80 words. Single new data point. No begging.

---

## Task C: Prioritize next grants

When asked to prioritize, score each Grants Pipeline row by:

1. **Thesis fit (0–3 points):** How well does BALBOA1's actual story map to their stated thesis?
2. **Effort-to-reward ratio (0–3 points):** Grant size / application complexity. A $50K rolling grant beats a $250K cohort-only grant with low odds.
3. **Strategic value beyond money (0–2 points):** Does winning this grant unlock relationships (e.g., Ethereum Foundation legitimacy), distribution (e.g., L2 ecosystem visibility), or credibility (e.g., Centrifuge RWA validation)?
4. **Realistic timing (0–2 points):** Are we ready to apply *now*, or do we need to wait for [audit completion / first pilot transaction / X]?

Top 10 score → that's the next batch to draft. Surface the list with reasoning.

## Quality gate

Before saving any grant draft:
- [ ] Every claim in the draft is sourced from `context/balboa1_facts.md` — no fabrication
- [ ] The angle matches the grantor's stated thesis (cite their own language if possible)
- [ ] Milestones are concrete and dated
- [ ] Amount requested matches a specific deliverable
- [ ] No marketing fluff — grants are reviewed by technical teams who skim
- [ ] All template variables filled (no `[bracketed]` placeholders left in final draft)
