"""
Job scraper for Bay Area data/analytics roles using JSearch API (RapidAPI).
Scrapes LinkedIn, Indeed, Glassdoor and more via a single API.
"""

import os
import json
import time
import requests
from datetime import datetime, timezone

# ── Config ────────────────────────────────────────────────────────────────────
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]
TARGET_ROLES = [
    "Analytics Engineer",
    "Business Intelligence Engineer",
    "Data Analyst",
    "Data Engineer",
]
LOCATION = "San Francisco Bay Area, CA"
HOURS_OLD = 24

JSEARCH_URL = "https://jsearch.p.rapidapi.com/search"
HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
}

# ── Scraper ───────────────────────────────────────────────────────────────────

def fetch_jobs_for_role(role: str) -> list[dict]:
    params = {
        "query": f"{role} {LOCATION}",
        "page": "1",
        "num_pages": "3",
        "date_posted": "today",
        "employment_types": "FULLTIME",
        "radius": "50",
    }
    try:
        resp = requests.get(JSEARCH_URL, headers=HEADERS, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("data", [])
    except Exception as e:
        print(f"[WARN] Failed to fetch jobs for '{role}': {e}")
        return []


def normalize_job(job: dict, searched_role: str) -> dict:
    posted_ts = job.get("job_posted_at_timestamp")
    if posted_ts:
        posted_dt = datetime.fromtimestamp(posted_ts, tz=timezone.utc)
        posted_str = posted_dt.strftime("%Y-%m-%d %H:%M UTC")
        # Filter: only last HOURS_OLD hours
        age_hours = (datetime.now(tz=timezone.utc) - posted_dt).total_seconds() / 3600
        if age_hours > HOURS_OLD:
            return None
    else:
        posted_str = "N/A"

    description = job.get("job_description") or ""
    if len(description) > 2000:
        description = description[:2000] + "..."

    return {
        "Job Title": job.get("job_title", ""),
        "Company": job.get("employer_name", ""),
        "Location": job.get("job_city", "") + ", " + job.get("job_state", ""),
        "Employment Type": job.get("job_employment_type", "FULLTIME"),
        "Date Posted": posted_str,
        "Apply Link": job.get("job_apply_link", ""),
        "Job Description": description,
        "Source": job.get("job_publisher", ""),
        "Searched Role": searched_role,
        "Salary": _fmt_salary(job),
    }


def _fmt_salary(job: dict) -> str:
    low = job.get("job_min_salary")
    high = job.get("job_max_salary")
    period = job.get("job_salary_period", "")
    if low and high:
        return f"${low:,.0f} – ${high:,.0f} {period}"
    if low:
        return f"${low:,.0f}+ {period}"
    return "Not Listed"


def scrape_all() -> list[dict]:
    all_jobs = []
    seen_ids = set()

    for role in TARGET_ROLES:
        print(f"[INFO] Fetching: {role}")
        raw_jobs = fetch_jobs_for_role(role)

        for job in raw_jobs:
            job_id = job.get("job_id", "")
            if job_id in seen_ids:
                continue
            seen_ids.add(job_id)

            normalized = normalize_job(job, role)
            if normalized:
                all_jobs.append(normalized)

        time.sleep(1)  # be polite to API

    print(f"[INFO] Total unique jobs found (last {HOURS_OLD}h): {len(all_jobs)}")
    return all_jobs


if __name__ == "__main__":
    jobs = scrape_all()
    with open("jobs.json", "w") as f:
        json.dump(jobs, f, indent=2)
    print(f"[INFO] Saved {len(jobs)} jobs to jobs.json")
