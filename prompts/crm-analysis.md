# Prompt: `crm-analysis`

When Nick types `crm-analysis`, load `skills/crm-analysis/SKILL.md` and execute the full pipeline scan.

Steps:
1. Read all 5 silo tabs + Drafts Log + Grants Pipeline from the Sheet
2. Run all 6 analysis sections (pipeline pulse, velocity gaps, cold contacts, variant performance, top 5, grants)
3. Output the full CRM Health Report in the terminal
4. Optionally save to output/crm-health-YYYY-MM-DD.md if Nick asks

No web searches. No external API calls. Pure Sheet analysis only.
