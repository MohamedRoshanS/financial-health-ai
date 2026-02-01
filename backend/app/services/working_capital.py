def compute_working_capital_metrics(monthly_df):
    """
    monthly_df: DataFrame with columns:
    revenue, receivable, payable, expense_amount
    """

    avg_revenue = monthly_df["revenue"].mean() if "revenue" in monthly_df else 0
    avg_receivable = monthly_df["receivable"].mean() if "receivable" in monthly_df else 0
    avg_payable = monthly_df["payable"].mean() if "payable" in monthly_df else 0
    expense_col = "expense_amount" if "expense_amount" in monthly_df.columns else (
    "expense" if "expense" in monthly_df.columns else None
    )

    avg_expense = monthly_df[expense_col].mean() if expense_col else 0

    dso = (avg_receivable / avg_revenue) * 30 if avg_revenue > 0 else 0
    dpo = (avg_payable / avg_expense) * 30 if avg_expense > 0 else 0

    ccc = dso - dpo

    risk = "Low"
    if ccc > 45:
        risk = "High"
    elif ccc > 30:
        risk = "Medium"

    actions = []

    if dso > 30:
        actions.append("Speed up receivables collection by tightening credit terms.")
    if dpo < 30:
        actions.append("Negotiate longer payment terms with suppliers.")
    if ccc > 45:
        actions.append("Consider short-term working capital financing to bridge cash gaps.")

    return {
        "dso": round(dso, 2),
        "dpo": round(dpo, 2),
        "cash_conversion_cycle": round(ccc, 2),
        "risk_level": risk,
        "actions": actions
    }
