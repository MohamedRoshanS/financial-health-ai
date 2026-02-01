import pandas as pd

# Simple enterprise-grade rule engine
CATEGORY_RULES = {
    "Rent": ["rent", "lease"],
    "Salary": ["salary", "wages", "payroll"],
    "Utilities": ["electricity", "water", "internet", "phone"],
    "Marketing": ["ads", "advertising", "marketing", "promotion"],
    "Logistics": ["transport", "shipping", "delivery", "freight"],
    "Office Supplies": ["stationery", "office", "supplies"],
    "Other": []
}

def categorize_expense(description: str):
    if not description:
        return "Other", 0.3

    desc = description.lower()

    for category, keywords in CATEGORY_RULES.items():
        for k in keywords:
            if k in desc:
                return category, 0.9

    return "Other", 0.5


def run_bookkeeping(monthly_df: pd.DataFrame):
    """
    Adds:
    - expense_category
    - category_confidence
    - monthly_ledger
    """

    df = monthly_df.copy()

    # Ensure description column exists
    if "description" not in df.columns:
        df["description"] = ""

    categories = []
    confidences = []

    for desc in df["description"]:
        cat, conf = categorize_expense(desc)
        categories.append(cat)
        confidences.append(conf)

    df["expense_category"] = categories
    df["category_confidence"] = confidences

    # Monthly ledger summary
    ledger = (
        df.groupby("expense_category")["expense_amount"]
        .sum()
        .reset_index()
        .sort_values(by="expense_amount", ascending=False)
    )

    uncategorized_count = (df["expense_category"] == "Other").sum()

    return {
        "ledger": ledger.to_dict(orient="records"),
        "uncategorized_count": int(uncategorized_count)
    }
