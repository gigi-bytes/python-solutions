# Email Validation Project

## 📌 Problem
Users often change email domains (for example, from agency emails to personal emails).  
We need a way to **validate user-submitted emails against a master list** to prevent errors when merging or verifying accounts.

---

## 🛠️ Solution
A Python script (`src/email_validation.py`) that:
- Reads CSV or Excel files (`.csv`, `.xlsx`)
- Compares a user list against a master list by email column
- Flags valid and invalid emails
- Outputs two reports:
  - `validated_emails.csv/xlsx` → all emails with a `Valid` column (True/False)
  - `invalid_emails.csv/xlsx` → only the invalid emails

---

## 🚀 Quickstart

```bash
# Run with sample data
python src/email_validation.py \
  --user-file data/samples/user_list.csv \
  --master-file data/samples/master_list.csv \
  --user-col Email \
  --master-col Email \
  --out-format xlsx
