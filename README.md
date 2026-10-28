# Pune IT Job Application Helper

A small, privacy-conscious workflow to track Pune IT support openings and generate tailored application email drafts.

## Target roles
- End User Support / Desktop Support
- IT Helpdesk / Service Desk (L1/L2)
- IT Support Engineer / Technical Support
- Incident, access, hardware and software support

## Quick start
1. Use Python 3.10+.
2. Copy `candidate.example.json` to `candidate.json` and fill in your own details. Do not commit personal data or your resume.
3. Add verified job listings and recruiter contact details to `jobs.csv`.
4. Run:

   ```bash
   python job_apply.py --candidate candidate.json --jobs jobs.csv --out drafts
   ```

5. Review each generated `.eml` draft, verify the recipient and job details, attach your resume yourself, and send only when you choose.

## Privacy and safety
- This tool **does not send emails automatically** and does not scrape websites or harvest recruiter email addresses.
- Use public, verified job postings and recruiter contacts intended for hiring.
- Do not put your resume, phone number, email address, passwords, app passwords, API keys, or other secrets in a public repository.
- Keep `candidate.json`, your resume, and generated drafts local. They are ignored by Git where possible.
- Respect each employer's application instructions and avoid duplicate or unsolicited bulk messages.

## Files
- `job_apply.py`: validates a jobs CSV and generates individual email drafts.
- `jobs.example.csv`: example job tracker format.
- `candidate.example.json`: safe template with placeholder values.

## Job tracker columns
`company,role,location,job_url,recipient_email,contact_name,notes,status`

Use statuses such as `saved`, `ready`, `applied`, `follow-up`, and `closed`. Set a verified `recipient_email` only when the employer/recruiter publishes it for applications; otherwise leave it blank and use the job URL.
