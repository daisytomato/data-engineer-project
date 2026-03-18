"""
Sends a daily job digest email with an HTML summary + link to Google Sheet.

Required env vars:
  GMAIL_USER      – sender Gmail address (e.g. yourbot@gmail.com)
  GMAIL_APP_PASS  – Gmail App Password (16-char, not your normal password)
  NOTIFY_EMAIL    – recipient email address
  GOOGLE_SHEET_ID – used to build the sheet URL in the email
"""

import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


def build_html(jobs: list[dict], sheet_url: str) -> str:
    today = datetime.utcnow().strftime("%B %d, %Y")
    role_counts = {}
    for j in jobs:
        r = j.get("Searched Role", "Other")
        role_counts[r] = role_counts.get(r, 0) + 1

    summary_rows = "".join(
        f"<tr><td style='padding:4px 12px'>{role}</td>"
        f"<td style='padding:4px 12px;text-align:center'><b>{count}</b></td></tr>"
        for role, count in sorted(role_counts.items())
    )

    # Top 15 job cards
    cards = ""
    for job in jobs[:15]:
        title = job.get("Job Title", "")
        company = job.get("Company", "")
        location = job.get("Location", "")
        salary = job.get("Salary", "Not Listed")
        link = job.get("Apply Link", "#")
        source = job.get("Source", "")
        posted = job.get("Date Posted", "")

        cards += f"""
        <tr>
          <td style="padding:12px;border-bottom:1px solid #eee">
            <b><a href="{link}" style="color:#1a73e8;text-decoration:none">{title}</a></b><br>
            <span style="color:#555">{company}</span> &nbsp;·&nbsp;
            <span style="color:#777">{location}</span><br>
            <small style="color:#888">💰 {salary} &nbsp;|&nbsp; 📅 {posted} &nbsp;|&nbsp; 🔗 {source}</small>
          </td>
        </tr>"""

    more_note = ""
    if len(jobs) > 15:
        more_note = f"<p style='color:#555'>...and <b>{len(jobs) - 15} more</b> jobs in the full spreadsheet.</p>"

    return f"""
    <html><body style="font-family:Arial,sans-serif;max-width:700px;margin:auto;color:#333">
      <div style="background:#1a73e8;padding:24px;border-radius:8px 8px 0 0">
        <h2 style="color:#fff;margin:0">🗂 Bay Area Data Jobs Digest</h2>
        <p style="color:#cce0ff;margin:4px 0 0">{today} · Last 24 hours · Full-time only</p>
      </div>

      <div style="padding:20px;background:#f8f9fa;border:1px solid #e0e0e0">
        <h3 style="margin-top:0">📊 Summary — {len(jobs)} new jobs found</h3>
        <table style="border-collapse:collapse">
          <tr style="background:#e8f0fe">
            <th style="padding:4px 12px;text-align:left">Role</th>
            <th style="padding:4px 12px">Count</th>
          </tr>
          {summary_rows}
        </table>
        <br>
        <a href="{sheet_url}" style="background:#1a73e8;color:#fff;padding:10px 20px;
           border-radius:4px;text-decoration:none;font-weight:bold">
          📄 Open Full Spreadsheet →
        </a>
      </div>

      <div style="padding:20px;border:1px solid #e0e0e0;border-top:none">
        <h3>🔥 Top Listings</h3>
        <table style="width:100%;border-collapse:collapse">
          {cards}
        </table>
        {more_note}
      </div>

      <div style="padding:12px 20px;background:#f1f3f4;border:1px solid #e0e0e0;
           border-top:none;border-radius:0 0 8px 8px;font-size:12px;color:#888">
        Automated by job-pipeline · GitHub Actions · Runs daily at 9:00 AM PT
      </div>
    </body></html>
    """


def send_email(jobs: list[dict], sheet_url: str):
    sender = os.environ["GMAIL_USER"]
    recipient = os.environ["NOTIFY_EMAIL"]
    app_pass = os.environ["GMAIL_APP_PASS"]

    today = datetime.utcnow().strftime("%b %d, %Y")
    subject = f"🗂 Bay Area Data Jobs – {len(jobs)} new listings ({today})"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Job Pipeline <{sender}>"
    msg["To"] = recipient

    html = build_html(jobs, sheet_url)
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_pass)
        server.sendmail(sender, recipient, msg.as_string())

    print(f"[INFO] Email sent to {recipient}")


if __name__ == "__main__":
    with open("jobs.json") as f:
        jobs = json.load(f)
    sheet_url = f"https://docs.google.com/spreadsheets/d/{os.environ['GOOGLE_SHEET_ID']}"
    send_email(jobs, sheet_url)
