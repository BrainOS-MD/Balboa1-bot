---
name: designer
description: Generates cover art and thumbnail options for content posts using Claude in Chrome to access free image generation tools (no paid API calls). Produces two distinct image prompts based on the content brief, guides Nick through generating them in the browser, and waits for approval before logging the choice. Activate when Nick types "design [content title]" or during content generation when a visual is needed.
---

# Designer Skill

## Free-First Approach

This skill does NOT call an image generation API. Instead:
1. It generates two optimized image prompts based on your content brief
2. It opens the image tool in Claude in Chrome (Ideogram, free tier — no credit card required)
3. You run each prompt in the browser
4. You choose which image to use and paste back the result
5. The skill logs your choice and formats the image for use

**Why this approach:** Free image generation APIs either cost money or have poor quality. Browser-based tools like Ideogram give better results for free with minimal setup.

---

## What This Skill Produces

For each content piece that needs a visual:
- 2 detailed image generation prompts (different styles/angles)
- Step-by-step instructions for generating them in the browser
- A formatted "ready to use" confirmation with the chosen image

---

## Step 1: Find the source brief

If Nick typed `design [content title]`: find the brief in `~/JARVIS-vault/03-BRIEFS/` matching the title.

If called during content generation: read the active content brief from the session.

Read: One Thing, the hook, the platform target (LinkedIn cover vs X thumbnail vs blog header uses different dimensions).

## Step 2: Determine the image type needed

| Platform | Image Type | Optimal Size |
|----------|-----------|-------------|
| LinkedIn personal post | Square or landscape illustration | 1:1 or 1.91:1 |
| LinkedIn company post | Cover/banner style | 1.91:1 (1200×628px) |
| Substack | Header image | 1:1 or 16:9 |
| Company blog | Featured image | 16:9 (1200×675px) |
| X/Twitter | In-tweet image | 16:9 |

## Step 3: Generate two image prompts

For each prompt, think about:
- **Visual metaphor:** what image represents the One Thing from the brief without showing text?
- **Mood:** matches Nick's personal voice (direct, operator) or company voice (institutional, clean)?
- **Style:** photo-realistic vs. illustrated vs. abstract vs. diagram?

Write two prompts that are visually distinct — not two versions of the same idea. One should be conceptual/abstract, one should be more concrete/literal.

**Prompt format for Ideogram:**
```
[Subject + action or composition] + [setting or context] + [style descriptors] + [mood] + [color palette if specific] + [aspect ratio]
```

**Example (for a maritime payments content piece):**

Prompt A (conceptual):
```
A glowing digital bridge connecting two cargo ships on opposite sides of a dark ocean, with luminous data streams flowing between them like fiber optic cables, cinematic aerial view, deep navy and gold color palette, clean and futuristic, 16:9
```

Prompt B (concrete):
```
Close-up of weathered hands holding a smartphone showing an instant payment confirmation, cargo containers visible through a port window in soft focus background, documentary photography style, warm ambient lighting, shallow depth of field, 1:1
```

## Step 4: Guide Nick through generation

Output:
```
🎨 Two image options for: [Content Title]

──────────────────────────────
OPTION A — [Style descriptor, e.g., "Conceptual / Dark Cinematic"]
──────────────────────────────
Prompt (copy this):
[full prompt A]

──────────────────────────────
OPTION B — [Style descriptor, e.g., "Human / Documentary"]
──────────────────────────────
Prompt (copy this):
[full prompt B]

──────────────────────────────

To generate these:
1. Open Claude in Chrome
2. Navigate to: ideogram.ai (free account, no credit card)
3. Click "Generate" and paste each prompt
4. Download the one you prefer

Ideogram tips:
- Click "Edit" after generation to adjust — don't re-generate from scratch
- "Turbo" model is fastest for previews; "Quality" for final use
- If the image has unwanted text, add "no text, no words, no labels" to the prompt

When you have your image, reply:
  "chose A" or "chose B"
  — or — "neither, try again" and I'll generate new prompts
```

## Step 5: Log the choice

When Nick replies with their choice:
- Note the chosen prompt in the Drafts Log with Touch Type = `Image Generated`
- Confirm: "✓ Image for [content title] selected — Option [A/B]"
- Remind Nick where to save it: `output/images/[date]-[slug]-cover.[ext]`

If Nick says "neither, try again":
- Ask: "What felt off about both options — too abstract? Wrong mood? Wrong colors?"
- Generate two new prompts that address the feedback
- Repeat the process

## Standing rules

- Never generate prompts without a content brief to reference — images without a clear brief are just decoration.
- Company content images should look institutional and credible. No AI-art-looking abstracts for the Balboa Corp LinkedIn page.
- Personal content can be more experimental.
- Always offer two distinct options, never two versions of the same concept.
- If Ideogram is down, suggest: leonardo.ai (free tier) or bing.com/images/create (free with Microsoft account).
