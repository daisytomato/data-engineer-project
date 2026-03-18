# 🗂 Bay Area Data Jobs Pipeline

Automatically scrapes **Analytics Engineer, BI Engineer, Data Analyst, and Data Engineer** full-time jobs posted in the last 24 hours in the Bay Area — writes them to Google Sheets and emails you a digest every morning at **9:00 AM PT**.

---

## 📁 Project Structure

```
job-pipeline/
├── run_pipeline.py              # Orchestrator
├── requirements.txt
├── scripts/
│   ├── scrape_jobs.py           # Fetches jobs via JSearch API (RapidAPI)
│   ├── write_to_sheets.py       # Writes results to Google Sheets
│   └── send_email.py            # Sends HTML email digest via Gmail
└── .github/
    └── workflows/
        └── daily_jobs.yml       # GitHub Actions schedule (9 AM PT daily)
```

---

## 🚀 Setup Guide

### Step 1 — Get a RapidAPI Key (JSearch)

JSearch aggregates LinkedIn, Indeed, Glassdoor and more.

1. Sign up at [rapidapi.com](https://rapidapi.com)
2. Subscribe to **JSearch** (free tier: 200 requests/month — enough for daily runs)
3. Copy your **X-RapidAPI-Key**

---

### Step 2 — Set Up Google Sheets

#### 2a. Create a Google Sheet
1. Go to [sheets.google.com](https://sheets.google.com) → create a new sheet
2. Copy the Sheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/THIS_IS_YOUR_SHEET_ID/edit
   ```

#### 2b. Create a Service Account
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (or use existing)
3. Enable **Google Sheets API** and **Google Drive API**
4. Go to **IAM & Admin → Service Accounts → Create Service Account**
5. Name it (e.g. `job-pipeline-bot`), click **Create**
6. Click the service account → **Keys** tab → **Add Key → JSON**
7. Download the JSON file — this is your `GOOGLE_SERVICE_ACCOUNT_JSON`

#### 2c. Share the Sheet with the Service Account
1. Open your Google Sheet
2. Click **Share**
3. Add the service account email (looks like `job-pipeline-bot@your-project.iam.gserviceaccount.com`) with **Editor** access

---

### Step 3 — Set Up Gmail App Password

1. Enable **2-Step Verification** on your Google account
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Create a new App Password (select "Mail" + "Other")
4. Copy the 16-character password — this is your `GMAIL_APP_PASS`

---

### Step 4 — Add GitHub Secrets

In your GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**:

| Secret Name                  | Value |
|------------------------------|-------|
| `RAPIDAPI_KEY`               | Your RapidAPI key |
| `GOOGLE_SERVICE_ACCOUNT_JSON`| Full contents of the service account JSON file |
| `GOOGLE_SHEET_ID`            | The Sheet ID from the URL |
| `GMAIL_USER`                 | Your Gmail address (e.g. `yourbot@gmail.com`) |
| `GMAIL_APP_PASS`             | 16-char Gmail App Password |
| `NOTIFY_EMAIL`               | Email address to receive the daily digest |

---

### Step 5 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial job pipeline"
git remote add origin https://github.com/YOUR_USERNAME/job-pipeline.git
git push -u origin main
```

GitHub Actions will now run automatically every day at **9:00 AM PT**.

---

## 🔧 Manual Run

**Trigger from GitHub UI:**
Go to your repo → **Actions** tab → **Daily Job Digest** → **Run workflow**

**Run locally:**
```bash
pip install -r requirements.txt

export RAPIDAPI_KEY="your_key"
export GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'
export GOOGLE_SHEET_ID="your_sheet_id"
export GMAIL_USER="yourbot@gmail.com"
export GMAIL_APP_PASS="your_app_password"
export NOTIFY_EMAIL="you@example.com"

python run_pipeline.py
```

---

## 📧 What the Email Looks Like

- Summary table (count per role)
- Top 15 job cards with title, company, location, salary, and direct apply link
- "Open Full Spreadsheet" button linking to Google Sheets

---

## 📊 Google Sheet Format

Each day gets its own tab (e.g. `2025-03-17`) with columns:

| Job Title | Company | Location | Employment Type | Salary | Date Posted | Source | Searched Role | Apply Link | Job Description |
|-----------|---------|----------|-----------------|--------|-------------|--------|---------------|------------|-----------------|

---

## ⏰ Schedule

The pipeline runs at `0 17 * * *` UTC = **9:00 AM PST / 10:00 AM PDT**.

To change the time, edit `.github/workflows/daily_jobs.yml`:
```yaml
- cron: "0 17 * * *"   # adjust UTC hour here
```

---

## 🛠 Troubleshooting

| Issue | Fix |
|-------|-----|
| No jobs found | Check RapidAPI quota; try manual trigger |
| Sheet not updating | Verify service account has Editor access to the sheet |
| Email not received | Check spam folder; confirm App Password is correct |
| GitHub Action fails | Check Actions tab → logs for error details |
