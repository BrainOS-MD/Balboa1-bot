# Setup Guide — BALBOA1 Outreach Bot

For Mac. Assumes zero terminal experience. **Plan 45 minutes** for the first run.

---

## What you're setting up

1. Claude Code on your Mac (logs in with your Pro account)
2. Google Sheets connected to the bot via a free Google Cloud project
3. The bot folder living at `~/balboa1-bot`

You'll do each section once. After that, daily use is `cd ~/balboa1-bot && claude`.

---

## Section 1: Install the tools (15 min)

### 1.1 Install Node.js (required for Claude Code)

Open the **Terminal** app (Cmd+Space, type "Terminal").

Paste this and press Enter:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
This installs Homebrew, a package manager. Follow the prompts. May take 5–10 min.

After it finishes, install Node:
```bash
brew install node
```

Verify Node installed:
```bash
node --version
```
Should print something like `v22.x.x`. If it does, you're good.

### 1.2 Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

When done, log in:
```bash
claude
```

Claude Code will ask how you want to authenticate. **Choose "Claude account" (Pro subscription)** — NOT API key. A browser window will open. Log in with **nick.grosz@gmail.com**. Approve the connection.

Once back in Terminal, you should see Claude Code is running. Type `/exit` to leave for now.

### 1.3 Install Python (for one-time Google auth helper)

```bash
brew install python
pip3 install --break-system-packages gspread google-auth google-auth-oauthlib
```

---

## Section 2: Get your Sheet into Google Drive (5 min)

### 2.1 Upload the seed file

1. Download `BALBOA1_CRM_v2.xlsx` (provided to you).
2. Go to [drive.google.com](https://drive.google.com).
3. Drag the xlsx into your Drive.
4. **Right-click the file → "Open with → Google Sheets"**. This converts it to native Google Sheets format.
5. Rename it to **`BALBOA1 CRM`** (no extension).
6. Open the converted file. **Copy the URL.** It looks like:
   `https://docs.google.com/spreadsheets/d/1AbcDeFgHiJkLmNoPqRsTuVwXyZ1234567/edit#gid=0`
7. The long string between `/d/` and `/edit` is your **Sheet ID**. Save it somewhere — you'll paste it into the bot in Section 4.

### 2.2 Verify the tabs

You should see these tabs at the bottom:
- 📖 README
- 📊 Dashboard
- 🎯 Grants Pipeline
- Venture & Investment
- OTC & Market Makers
- Partnerships
- Freight Forwarders
- General Contacts
- ✉️ Templates
- 📨 Drafts Log

Click the Dashboard tab — you should see the funnel chart, priority pie, and silo bar chart. If charts didn't import cleanly during the xlsx→Sheets conversion, see "Section 7: Troubleshooting" below.

---

## Section 3: Connect Google Sheets to the bot (10 min)

You're creating OAuth credentials so the bot can read/write your Sheet using your own Google login — no service account needed.

### 3.1 Create a Google Cloud project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Sign in with **nick.grosz@gmail.com**
3. Top bar: click the project dropdown → "New Project"
4. Name it: `balboa1-bot`. Click Create. Wait 30 seconds.
5. Make sure `balboa1-bot` is selected in the top bar.

### 3.2 Enable the Google Sheets API

1. Left menu: ☰ → APIs & Services → Library
2. Search "Google Sheets API". Click it. Click **Enable**.
3. Go back to Library. Search "Google Drive API". Click it. Click **Enable**.

### 3.3 Create an OAuth 2.0 Client ID

1. Left menu: ☰ → APIs & Services → Credentials
2. Click **+ Create Credentials → OAuth client ID**
3. If prompted to configure the consent screen first:
   - Click "Configure consent screen" → choose **External** → Create
   - App name: `balboa1-bot`. User support email: your email. Developer email: your email.
   - Click Save and Continue through all steps (no scopes needed, no test users needed).
   - Go back to Credentials → + Create Credentials → OAuth client ID.
4. Application type: **Desktop app**. Name: `balboa1-bot`. Click Create.
5. A dialog shows your client ID and secret. Click **Download JSON**.
6. Rename the downloaded file to **`oauth_credentials.json`**.

### 3.4 Drop the credentials file in place

Move `oauth_credentials.json` into `~/balboa1-bot/credentials/`.

```bash
ls ~/balboa1-bot/credentials/
```
Should print `oauth_credentials.json`.

### 3.5 Authorize on first run

The first time the bot connects to the Sheet, it will open a browser window asking you to sign in with Google and grant access. Do that once — it saves a token to `credentials/authorized_user.json` so you never have to do it again.

---

## Section 4: Install the bot folder (5 min)

### 4.1 Move the bot folder into place

Download the `balboa1-bot.zip` file. Unzip it. Move the unzipped `balboa1-bot` folder to your home directory (just `~/`, i.e. `/Users/yourname/`).

Verify in Terminal:
```bash
ls ~/balboa1-bot
```
You should see `README.md`, `SETUP.md`, `briefing.md`, `CLAUDE.md`, `skills/`, etc.

### 4.2 Drop in the credentials

If you haven't already done Section 3.4, move `oauth_credentials.json` into `~/balboa1-bot/credentials/`.

```bash
ls ~/balboa1-bot/credentials/
```
Should print `oauth_credentials.json`.

### 4.3 Set your Sheet ID

Open `~/balboa1-bot/CLAUDE.md` in any text editor (TextEdit is fine — make sure you're editing as plain text: Format → Make Plain Text).

Find the line:
```
SHEET_ID = "PASTE_YOUR_SHEET_ID_HERE"
```
Replace `PASTE_YOUR_SHEET_ID_HERE` with the Sheet ID you copied in Section 2.1. Save.

---

## Section 5: First run (5 min)

```bash
cd ~/balboa1-bot
claude
```

Claude Code launches inside the folder. It automatically loads `CLAUDE.md` (your standing instructions) and discovers the skills in `skills/`.

Test the connection:
```
read my sheet and tell me how many contacts I have in each silo
```

If it returns counts, you're connected. 🎉

Now run the morning briefing:
```
briefing
```

The bot will:
1. Read all 5 silo tabs
2. Identify today's outreach (new sends + follow-ups due)
3. Identify grants nearing deadline
4. Draft personalized messages
5. Save them all to `output/daily_brief_YYYY-MM-DD.md`
6. Append entries to the `📨 Drafts Log` tab in your Sheet

Open `output/daily_brief_YYYY-MM-DD.md` in any text editor (or in Claude Code) and copy-paste the drafts to LinkedIn / X / Gmail.

---

## Section 6: Daily use

Every morning:
```bash
cd ~/balboa1-bot && claude
```
Then type `briefing`.

After sending each message, in the Sheet:
- Change Status dropdown to next stage (e.g., "2. Request Sent")
- The Last Touch Date column auto-fills when you do this (bot also writes back)

When someone replies:
- Set Status to "7. Replied — Positive" (or appropriate stage)
- Paste a snippet of what they said into the `Reply Snippet` column
- Next morning's briefing will include a drafted response

To draft a reply right now without waiting for tomorrow:
```
reply-to Max Boonen
```

To enrich one contact (paste in their About + recent posts):
```
enrich-contact Joe Lonsdale
```

To draft a full grant application:
```
grant-draft Ethereum Foundation
```

---

## Section 7: Troubleshooting

**"Claude Code prompts me about an API key on every launch"**
Run: `unset ANTHROPIC_API_KEY` then `claude` again. Then in Claude Code, run `/login` and choose Claude subscription. To make it stick across terminal sessions, add this line to `~/.zshrc`:
```
unset ANTHROPIC_API_KEY
```

**"Bot can't read the sheet"**
- Verify `oauth_credentials.json` is in `~/balboa1-bot/credentials/`
- If `authorized_user.json` is missing or expired, delete it — the browser auth prompt will reappear on the next run
- Verify the Sheet ID in `CLAUDE.md` matches your actual sheet URL

**"Charts didn't survive xlsx → Sheets conversion"**
This is a known Google Sheets quirk. Easiest fix: in the Dashboard tab, manually recreate the three charts:
- Funnel: select cells A5:B18 → Insert → Chart → Bar chart
- Priority Tier: select E5:F11 → Insert → Chart → Pie chart
- Silo: select H5:I10 → Insert → Chart → Column chart
Takes about 90 seconds total.

**"Hitting Pro plan rate limits during heavy briefings"**
The morning briefing uses one Claude Code session for typically 5-15 minutes. Should stay well within Pro limits at <150 contacts. If you scale to 500+ contacts and hit limits, you have two options: (1) split briefings into "morning" (top tiers) and "afternoon" (general contacts), or (2) add API credits to your Anthropic Console for overflow.

**"I want to schedule briefing to run automatically at 7am"**
That requires moving from Pro subscription to API credits (headless mode). Skip this for now — manual 60-second runs are fine and you save the API spend.
