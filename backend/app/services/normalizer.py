import pandas as pd

COLUMN_MAP = {
    "date": ["date", "month"],
    "revenue": ["revenue", "sales", "income"],
    "expense_category": ["expense_category", "category"],
    "expense_amount": ["expense_amount", "expense", "cost"],
    "accounts_receivable": ["receivable", "accounts_receivable"],
    "accounts_payable": ["payable", "accounts_payable"],
    "inventory_value": ["inventory", "stock"],
    "loan_emi": ["loan_emi", "emi"],
    "gst_paid": ["gst_paid"],
    "gst_due": ["gst_due"]
}

def normalize_data(df):
    warnings = []

    df.columns = df.columns.str.lower()
    normalized = {}

    for standard, variants in COLUMN_MAP.items():
        for v in variants:
            if v in df.columns:
                normalized[standard] = df[v]
                break
        else:
            normalized[standard] = 0
            warnings.append(f"Missing column: {standard}")

    clean_df = pd.DataFrame(normalized)

    clean_df["date"] = pd.to_datetime(clean_df["date"]).dt.to_period("M")

    monthly_df = clean_df.groupby("date").sum(numeric_only=True).reset_index()

    return monthly_df, warnings
