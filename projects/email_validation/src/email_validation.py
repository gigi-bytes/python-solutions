import argparse
import sys
import pandas as pd
from pathlib import Path

def load_table(path: Path) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        sys.exit(f"[ERROR] File not found: {p}")
    if p.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(p)
    if p.suffix.lower() in {".csv", ".txt"}:
        return pd.read_csv(p)
    sys.exit(f"[ERROR] Unsupported file type: {p.suffix}")

def save_table(df: pd.DataFrame, stem: Path, fmt: str):
    if fmt == "xlsx":
        df.to_excel(stem.with_suffix(".xlsx"), index=False)
    elif fmt == "csv":
        df.to_csv(stem.with_suffix(".csv"), index=False)
    else:
        sys.exit(f"[ERROR] Unsupported output format: {fmt}")

def validate_emails(user_df, master_df, user_col, master_col):
    if user_col not in user_df.columns:
        sys.exit(f"[ERROR] Column '{user_col}' not in user file. Available: {list(user_df.columns)}")
    if master_col not in master_df.columns:
        sys.exit(f"[ERROR] Column '{master_col}' not in master file. Available: {list(master_df.columns)}")
    result = user_df.copy()
    result["Valid"] = result[user_col].isin(master_df[master_col])
    result = result.drop_duplicates(subset=[user_col])
    return result

def parse_args():
    p = argparse.ArgumentParser(description="Validate a list of emails against a master list (CSV/XLSX).")
    p.add_argument("--user-file", required=True, help="Path to user list (CSV/XLSX)")
    p.add_argument("--master-file", required=True, help="Path to master list (CSV/XLSX)")
    p.add_argument("--user-col", default="Email", help="Email column in user file")
    p.add_argument("--master-col", default="Email", help="Email column in master file")
    p.add_argument("--out-format", choices=["csv", "xlsx"], default="csv", help="Output format (default: csv)")
    return p.parse_args()

def main():
    args = parse_args()
    user_df = load_table(args.user_file)
    master_df = load_table(args.master_file)
    validated = validate_emails(user_df, master_df, args.user_col, args.master_col)
    invalid = validated[validated["Valid"] == False]
    save_table(validated, Path("validated_emails"), args.out_format)
    save_table(invalid, Path("invalid_emails"), args.out_format)
    print("✅ Done. Created:")
    print(f" - validated_emails.{args.out_format}")
    print(f" - invalid_emails.{args.out_format}")

if __name__ == "__main__":
    main()
