"""
Orchestrator: runs the full pipeline end to end.
  1. Scrape jobs
  2. Write to Google Sheets
  3. Send email digest
"""

import json
import sys
from scripts.scrape_jobs import scrape_all
from scripts.write_to_sheets import write_to_sheet
from scripts.send_email import send_email


def main():
    print("=" * 50)
    print("STEP 1/3 — Scraping jobs...")
    print("=" * 50)
    jobs = scrape_all()

    if not jobs:
        print("[WARN] No jobs found — skipping sheet + email.")
        sys.exit(0)

    # Save for debugging / re-runs
    with open("jobs.json", "w") as f:
        json.dump(jobs, f, indent=2)

    print("\n" + "=" * 50)
    print("STEP 2/3 — Writing to Google Sheets...")
    print("=" * 50)
    sheet_url = write_to_sheet(jobs)

    print("\n" + "=" * 50)
    print("STEP 3/3 — Sending email digest...")
    print("=" * 50)
    send_email(jobs, sheet_url)

    print("\n✅ Pipeline complete!")


if __name__ == "__main__":
    main()
