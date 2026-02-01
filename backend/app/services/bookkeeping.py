import pandas as pd

# Minimal SME Chart of Accounts (India-friendly)
CHART_OF_ACCOUNTS = {
    "Rent & Lease": ["rent", "lease"],
    "Salaries & Wages": ["salary", "wages", "payroll"],
    "Utilities": ["electricity", "water", "internet", "phone"],
    "Marketing & Advertising": ["ads", "advertising", "promotion"],
    "Logistics & Transport": ["transport", "shipping", "delivery"],
    "Office Expenses": ["stationery", "office"],
    "Professional Fees": ["consulting", "legal", "audit"],
    "Interest & Finance Charges": ["interest", "bank charge"],
}

def categorize(description: str):
    if not description or not isinstance(description, str):
        return "Uncategorized", 0.4

    text = description.lower()

    for category, keywords in CHART_OF_ACCOUNTS.items():
        for kw in keywords:
            if kw in text:
                return category, 0.9

    return "Uncategorized", 0.5


def automated_bookkeeping(df: pd.DataFrame):
    """
    Input: normalized monthly dataframe
    Output:
    - expense ledger
    - monthly P&L summary
    - bookkeeping quality signals
    """

    df = df.copy()

    # Ensure required columns
    if "expense_amount" not in df.columns:
        return {
            "ledger": [],
            "summary": {},
            "issues": ["Expense data missing"]
        }

    # Optional description support
    if "description" not in df.columns:
        df["description"] = ""

    categories = []
    confidence = []

    for desc in df["description"]:
        cat, conf = categorize(desc)
        categories.append(cat)
        confidence.append(conf)

    df["account"] = categories
    df["confidence"] = confidence

    # Expense Ledger
    ledger = (
        df.groupby("account")["expense_amount"]
        .sum()
        .reset_index()
        .sort_values(by="expense_amount", ascending=False)
    )

    # P&L-style summary
    total_expenses = df["expense_amount"].sum()
    uncategorized = df[df["account"] == "Uncategorized"]["expense_amount"].sum()

    summary = {
        "total_expenses": float(total_expenses),
        "uncategorized_ratio": round(
            (uncategorized / total_expenses) if total_expenses else 0, 2
        )
    }

    issues = []
    if summary["uncategorized_ratio"] > 0.25:
        issues.append("High proportion of uncategorized expenses")

    return {
        "ledger": ledger.to_dict(orient="records"),
        "summary": summary,
        "issues": issues
    }
