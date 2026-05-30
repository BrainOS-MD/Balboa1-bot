#!/usr/bin/env python3
"""
add-notes-column.py

Adds a 'Notes & Research' column (col Q) to each silo tab in the live Google Sheet.
Safe to run multiple times — checks before adding.

Usage:
    cd ~/balboa-bot
    python3 scripts/add-notes-column.py

Requirements:
    pip3 install --break-system-packages gspread google-auth
"""

import sys
import json

def main():
    # Load config from CLAUDE.md
    try:
        import gspread
    except ImportError:
        print("Error: gspread not installed. Run:")
        print("  pip3 install --break-system-packages gspread google-auth")
        sys.exit(1)

    # Read Sheet ID from CLAUDE.md
    sheet_id = None
    try:
        with open("CLAUDE.md", "r") as f:
            for line in f:
                if 'SHEET_ID' in line and '=' in line:
                    sheet_id = line.split('=')[1].strip().strip('"').strip("'")
                    break
    except FileNotFoundError:
        print("Error: CLAUDE.md not found. Run this script from ~/balboa-bot/")
        sys.exit(1)

    if not sheet_id or sheet_id == "PASTE_YOUR_SHEET_ID_HERE":
        print("Error: SHEET_ID not set in CLAUDE.md")
        print("Open CLAUDE.md and replace PASTE_YOUR_SHEET_ID_HERE with your Sheet ID")
        sys.exit(1)

    print(f"Connecting to Sheet: {sheet_id[:20]}...")

    try:
        gc = gspread.oauth(
            credentials_filename="credentials/oauth_credentials.json",
            authorized_user_filename="credentials/authorized_user.json"
        )
        sh = gc.open_by_key(sheet_id)
    except FileNotFoundError:
        print("Error: credentials/oauth_credentials.json not found")
        print("Follow SETUP.md Section 3 to create OAuth credentials")
        sys.exit(1)
    except Exception as e:
        print(f"Error connecting to Sheet: {e}")
        sys.exit(1)

    SILOS = [
        'Venture & Investment',
        'OTC & Market Makers',
        'Partnerships',
        'Freight Forwarders',
        'General Contacts'
    ]

    NEW_COLUMN_NAME = 'Notes & Research'
    HEADER_ROW = 2  # Headers are in row 2 on silo tabs (row 1 is the title)

    for silo in SILOS:
        try:
            ws = sh.worksheet(silo)
        except gspread.WorksheetNotFound:
            print(f"  ⚠ Sheet tab '{silo}' not found — skipping")
            continue

        # Read current headers
        headers = ws.row_values(HEADER_ROW)

        if NEW_COLUMN_NAME in headers:
            col_idx = headers.index(NEW_COLUMN_NAME) + 1
            print(f"  ✓ '{silo}' — column already exists at col {col_idx}")
            continue

        # Find the next empty column
        next_col = len(headers) + 1

        # Write the header
        ws.update_cell(HEADER_ROW, next_col, NEW_COLUMN_NAME)

        # Apply the same header formatting style as existing headers
        # (Navy background, white bold text) — via Google Sheets API format request
        try:
            col_letter = chr(ord('A') + next_col - 1)  # works for cols up to Z
            ws.format(
                f"{col_letter}{HEADER_ROW}",
                {
                    "backgroundColor": {"red": 0.05, "green": 0.11, "blue": 0.16},
                    "textFormat": {
                        "bold": True,
                        "foregroundColor": {"red": 0.95, "green": 0.94, "blue": 0.92},
                        "fontSize": 11
                    },
                    "horizontalAlignment": "CENTER",
                    "wrapStrategy": "WRAP"
                }
            )
        except Exception:
            pass  # Formatting is cosmetic — don't fail if it errors

        # Set column width to a reasonable size for notes text
        try:
            # Column width via batchUpdate
            body = {
                "requests": [{
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": ws.id,
                            "dimension": "COLUMNS",
                            "startIndex": next_col - 1,
                            "endIndex": next_col
                        },
                        "properties": {"pixelSize": 300},
                        "fields": "pixelSize"
                    }
                }]
            }
            sh.batch_update(body)
        except Exception:
            pass  # Width is cosmetic — don't fail

        print(f"  ✓ '{silo}' — added '{NEW_COLUMN_NAME}' at col {next_col}")

    print("\n✓ Done. Notes & Research column added to all silo tabs.")
    print("\nNext: run the bot and use 'stage-check' to start enriching accepted contacts.")


if __name__ == "__main__":
    main()
