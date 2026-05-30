# Command: `grant-draft [GRANT NAME]`

When Nick types `grant-draft GRANT_NAME`, execute the full application drafting workflow from `skills/grant-application/SKILL.md` Task A.

## Step 1: Find the grant

Search the `🎯 Grants Pipeline` tab for a row where Grant Name (col E) matches. Be lenient on casing and partial matches.

If multiple matches, ask Nick which one.
If no match, ask Nick to provide: grant name, application URL, est. size, category.

## Step 2: Read the application page

If Application URL (col I) exists, fetch and read it. Extract:
- The exact application questions
- Word/character limits per question (if specified)
- Deadline
- Any submission requirements (e.g., GitHub repo, deck, demo video)

If URL is missing or fetch fails, tell Nick:
```
Can you paste the application questions for [Grant Name]? Or share the URL?
```

## Step 3: Draft answers

Follow `skills/grant-application/SKILL.md` exactly. For each question:
- Match the grantor's stated thesis (use their language)
- Source every claim from `context/balboa1_facts.md`
- Stay under stated word limits
- Use concrete proof points, not adjectives
- For "milestones" or "use of funds" questions: be specific with dates and dollar amounts

## Step 4: Output

Save the draft as: `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/JARVIS-vault/00-INBOX/_YYYY-MM-DD-grant-[slugified-name].md`

Format:
```markdown
# Grant Application Draft: [Grant Name]

**Deadline:** [date]  
**Amount requested:** $[X]  
**Application URL:** [url]  
**Status before this draft:** [from sheet]  

---

## [Question 1 — exact text from application]
[Answer, calibrated to word limit]

## [Question 2 — ...]
[...]

---

## Submission checklist
- [ ] Nick reviews & edits draft
- [ ] [Any specific assets required, e.g. "Upload deck"]
- [ ] [Any specific links required, e.g. "Provide GitHub repo URL"]
- [ ] Submit at: [URL]
- [ ] Update Grants Pipeline tab:
      - Status → "Submitted"
      - Date Applied → [today]
      - Amount Requested → $[X]
      - Next Action → "Follow up if no response in 30 days"
```

## Step 5: Update the Sheet

Change the grant's row:
- Status: "Drafting" (was probably "Not Started")
- Next Action: "Nick to review draft at 00-INBOX/[filename]"

## Step 6: Tell Nick

Reply concisely:
```
✅ Drafted [Grant Name] application at 00-INBOX/[filename]

[X] questions answered, [N] words total.
Word count details: [if helpful]

Open it, edit, and submit. After submission, change Status to "Submitted" in the Grants Pipeline tab and I'll auto-follow up in 30 days if no response.
```

## Edge case: Need to know specific info

If a question requires info not in your context (e.g., "What's your GitHub link?" "What audit firm are you using?" "What's your treasury composition?"), don't fabricate. Instead, include the question in the draft with:
```
[NICK TO FILL: specific info needed — e.g., "audit firm name once selected"]
```
And surface a list of these "to-fills" at the end of the draft so Nick can complete them in one pass.
