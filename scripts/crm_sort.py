"""
crm_sort.py — Sort every CRM contact tab by stage priority, then tier.

Sort order within each tab:
  1. "3. Request Accepted"  — needs intro DM, highest urgency
  2. Stage 4+               — active deals / meetings booked
  3. "2. Request Sent"      — waiting on acceptance
  4. "1. To Connect"        — outreach queue
  5. Empty / unknown        — bottom

Secondary sort: Tier 0 → Tier 1 → Tier 2

Run:  python3 scripts/crm_sort.py
"""

import gspread

SHEET_ID = "1GT0JlOm0ehyycaQVkf93WjhYKrAJsN6ZzC_0c7ZGrOQ"

# Tabs that are NOT contact lists — skip them
SKIP_TABS = {
    "📖 README",
    "📊 Dashboard",
    "🎯 Grants Pipeline",
    "✉️ Templates",
    "📨 Drafts Log",
}

TIER_ORDER = {"Tier 0": 0, "Tier 1": 1, "Tier 2": 2}


def stage_priority(status: str) -> int:
    s = status.strip()
    if s.startswith("3."):
        return 0   # Request Accepted — top, needs DM
    if s and s[0].isdigit() and int(s[0]) >= 4:
        return 1   # Meeting booked / further along — still active
    if s.startswith("2."):
        return 2   # Request Sent — waiting
    if s.startswith("1."):
        return 3   # To Connect — queue
    return 99      # empty / unknown — bottom


def sort_key(row):
    tier = row[0].strip() if row else ""
    status = row[1].strip() if len(row) > 1 else ""
    return (stage_priority(status), TIER_ORDER.get(tier, 99))


def is_empty_row(row) -> bool:
    # A row is "empty" if cols A, B, and D (Priority, Status, Name) are all blank
    a = row[0].strip() if len(row) > 0 else ""
    b = row[1].strip() if len(row) > 1 else ""
    d = row[3].strip() if len(row) > 3 else ""
    return not (a or b or d)


def col_letter(n: int) -> str:
    """Convert 1-based column index to letter(s). Handles up to ZZ."""
    result = ""
    while n > 0:
        n, rem = divmod(n - 1, 26)
        result = chr(65 + rem) + result
    return result


def sort_tab(ws) -> dict:
    rows = ws.get_all_values()

    # Expect 3 header rows (title, description, column headers)
    if len(rows) <= 3:
        return {"tab": ws.title, "skipped": True, "reason": "too few rows"}

    header_check_a = rows[2][0].strip() if rows[2] else ""
    header_check_b = rows[2][1].strip() if len(rows[2]) > 1 else ""
    if header_check_a != "Priority" or header_check_b != "Status":
        return {"tab": ws.title, "skipped": True, "reason": "unexpected header structure"}

    data_rows = rows[3:]
    num_cols = len(rows[2])

    non_empty = [r for r in data_rows if not is_empty_row(r)]
    empty = [r for r in data_rows if is_empty_row(r)]

    sorted_data = sorted(non_empty, key=sort_key) + empty

    if not sorted_data:
        return {"tab": ws.title, "skipped": True, "reason": "no data rows"}

    # Pad every row to num_cols so the update range is uniform
    padded = [r + [""] * max(0, num_cols - len(r)) for r in sorted_data]
    padded = [r[:num_cols] for r in padded]  # trim if somehow wider

    end_col = col_letter(num_cols)
    end_row = 3 + len(padded)          # 3 header rows + data rows (1-indexed)
    range_str = f"A4:{end_col}{end_row}"

    ws.update(range_name=range_str, values=padded, value_input_option="RAW")

    # Count contacts at each stage for the report
    stage_counts = {}
    for r in non_empty:
        stage = r[1].strip() if len(r) > 1 else "unknown"
        stage_counts[stage] = stage_counts.get(stage, 0) + 1

    return {
        "tab": ws.title,
        "skipped": False,
        "contacts": len(non_empty),
        "stages": stage_counts,
    }


def main():
    gc = gspread.oauth(
        credentials_filename="./credentials/oauth_credentials.json",
        authorized_user_filename="./credentials/authorized_user.json",
    )
    sh = gc.open_by_key(SHEET_ID)

    worksheets = sh.worksheets()
    print(f"Found {len(worksheets)} tabs. Sorting contact tabs...\n")

    total_sorted = 0
    total_stage3 = 0

    for ws in worksheets:
        if ws.title in SKIP_TABS:
            print(f"  ⏭️  {ws.title} — skipped (non-contact tab)")
            continue

        result = sort_tab(ws)

        if result.get("skipped"):
            print(f"  ⏭️  {result['tab']} — skipped ({result['reason']})")
        else:
            stage3_count = result["stages"].get("3. Request Accepted", 0)
            total_stage3 += stage3_count
            total_sorted += result["contacts"]

            stage_summary = ", ".join(
                f"{v}x {k}" for k, v in sorted(result["stages"].items())
            )
            marker = " ← NEEDS DM" if stage3_count > 0 else ""
            print(
                f"  ✅ {result['tab']:30s} {result['contacts']} contacts  [{stage_summary}]{marker}"
            )

    print(f"\nDone. {total_sorted} contacts sorted across all tabs.")
    if total_stage3 > 0:
        print(f"🔥 {total_stage3} contact(s) at Stage 3 (Request Accepted) — now at top of their tabs.")
    else:
        print("No contacts at Stage 3 yet.")


if __name__ == "__main__":
    main()
