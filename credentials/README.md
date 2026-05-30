# Credentials folder

## Files that belong here

**`oauth_credentials.json`** — OAuth 2.0 client secrets downloaded from Google Cloud Console.
Follow SETUP.md Section 3 to create this. Treat it like a password — never commit to git.

**`authorized_user.json`** — Auto-created by gspread after your first browser login.
Do not edit. If authentication breaks, delete this file and re-authorize (the browser prompt will reappear on the next run).

## Neither file is in git

Both are listed in `.gitignore`. If you clone this repo fresh, you need to re-create `oauth_credentials.json` from Google Cloud Console and re-authorize.
