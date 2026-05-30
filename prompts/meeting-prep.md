# Prompt: `meeting-prep [NAME]`

When Nick types `meeting-prep [NAME]`, load `skills/meeting-prep/SKILL.md` and execute the full workflow for NAME.

Steps:
1. Find NAME in all silo tabs
2. Read their Enrichment (col P), Notes (col Q), and Drafts Log history
3. Check JARVIS bridge for relevant current thinking
4. Run ONE targeted web search for recent firm news
5. Build the pre-call brief (see skill for exact format)
6. Deliver directly in the terminal — no output file needed unless Nick asks

If NAME is not in the CRM, ask which silo to look in, or whether Nick wants to create a new entry.
If NAME has no enrichment data, run enrich-contact first and ask Nick to confirm before proceeding.
