#!/usr/bin/env python3
"""Generate reviewable email drafts for verified job listings. Never sends mail."""
import argparse
import csv
import json
import re
from email.message import EmailMessage
from pathlib import Path

REQUIRED = {"company", "role", "location", "job_url", "recipient_email", "contact_name", "notes", "status"}

def clean(value):
    return (value or "").strip()

def safe_filename(value):
    value = re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-_").lower()
    return value[:70] or "job"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", default="candidate.json")
    parser.add_argument("--jobs", default="jobs.csv")
    parser.add_argument("--out", default="drafts")
    args = parser.parse_args()

    candidate_path = Path(args.candidate)
    jobs_path = Path(args.jobs)
    if not candidate_path.exists():
        raise SystemExit(f"Candidate file not found: {candidate_path}. Copy candidate.example.json to candidate.json.")
    if not jobs_path.exists():
        raise SystemExit(f"Jobs file not found: {jobs_path}. Copy jobs.example.csv to jobs.csv.")

    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    name = clean(candidate.get("name"))
    skills = clean(candidate.get("skills"))
    experience = clean(candidate.get("experience"))
    resume_filename = clean(candidate.get("resume_filename")) or "your resume"
    if not name or name == "YOUR NAME":
        raise SystemExit("Fill in your real name in candidate.json before generating drafts.")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    count = 0
    with jobs_path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            raise SystemExit("Missing CSV columns: " + ", ".join(sorted(missing)))
        for row in reader:
            status = clean(row.get("status")).lower()
            company, role = clean(row.get("company")), clean(row.get("role"))
            if status not in {"ready", "saved"} or not company or not role:
                continue
            recipient = clean(row.get("recipient_email"))
            job_url = clean(row.get("job_url"))
            contact = clean(row.get("contact_name")) or "Hiring Team"
            location = clean(row.get("location")) or "Pune"
            notes = clean(row.get("notes"))
            subject = f"Application for {role} — {name}"
            body = (
                f"Dear {contact},\n\n"
                f"I am writing to express my interest in the {role} opportunity at {company}"
                f" ({location}).\n\n"
                f"My relevant experience: {experience or '[Add relevant experience]'}\n"
                f"Relevant skills: {skills or '[Add relevant skills]'}\n\n"
                f"I would appreciate the opportunity to discuss how my background fits this role. "
                f"I can share my resume for your review.\n\n"
                f"Job posting: {job_url or '[Add verified job posting URL]'}\n"
                + (f"Notes: {notes}\n" if notes else "")
                + f"\nThank you for your time and consideration.\n\n"
                f"Regards,\n{name}\n"
                f"[Add your phone number] | [Add your email]\n\n"
                f"Attachment reminder: attach {resume_filename} manually before sending.\n"
            )
            msg = EmailMessage()
            msg["Subject"] = subject
            if recipient:
                msg["To"] = recipient
            msg.set_content(body)
            filename = safe_filename(f"{company}-{role}") + ".eml"
            path = out / filename
            if path.exists():
                path = out / safe_filename(f"{company}-{role}-{count+1}") + ".eml"
            path.write_bytes(msg.as_bytes())
            count += 1
            print(f"Created draft: {path}" + (f" (recipient: {recipient})" if recipient else " (recipient not set; use job portal)"))
    print(f"\nCreated {count} draft(s). Nothing was sent. Review each draft, verify details, attach your resume, and send manually.")

if __name__ == "__main__":
    main()
