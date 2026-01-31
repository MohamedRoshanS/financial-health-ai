def calculate_health_score(df):
    total_revenue = df["revenue"].sum()
    total_expenses = df["expense_amount"].sum()
    total_emi = df["loan_emi"].sum()

    monthly_cash = df["revenue"] - df["expense_amount"] - df["loan_emi"]
    positive_months = (monthly_cash > 0).sum()
    total_months = len(df)

    cash_flow_score = (positive_months / total_months) * 25

    profit_margin = (total_revenue - total_expenses) / max(total_revenue, 1)
    if profit_margin >= 0.2:
        profitability_score = 20
    elif profit_margin >= 0.1:
        profitability_score = 15
    elif profit_margin > 0:
        profitability_score = 8
    else:
        profitability_score = 0

    expense_ratio = total_expenses / max(total_revenue, 1)
    if expense_ratio <= 0.6:
        expense_score = 15
    elif expense_ratio <= 0.75:
        expense_score = 10
    elif expense_ratio <= 0.9:
        expense_score = 5
    else:
        expense_score = 0

    receivables = df["accounts_receivable"].mean()
    payables = max(df["accounts_payable"].mean(), 1)
    liquidity_ratio = receivables / payables

    if liquidity_ratio >= 1.5:
        liquidity_score = 15
    elif liquidity_ratio >= 1.0:
        liquidity_score = 10
    elif liquidity_ratio >= 0.7:
        liquidity_score = 5
    else:
        liquidity_score = 0

    debt_ratio = total_emi / max(total_revenue, 1)
    if debt_ratio <= 0.1:
        debt_score = 15
    elif debt_ratio <= 0.2:
        debt_score = 10
    elif debt_ratio <= 0.3:
        debt_score = 5
    else:
        debt_score = 0

    gst_months_paid = (df["gst_due"] == 0).sum()
    if "gst_due" in df.columns:
        tax_score = (gst_months_paid / total_months) * 10
    else:
        tax_score = 3

    total_score = round(
        cash_flow_score + profitability_score + expense_score +
        liquidity_score + debt_score + tax_score
    )

    return {
        "total_score": total_score,
        "breakdown": {
            "cash_flow": round(cash_flow_score, 1),
            "profitability": profitability_score,
            "expenses": expense_score,
            "liquidity": liquidity_score,
            "debt": debt_score,
            "tax": round(tax_score, 1)
        }
    }
def health_status(score):
    if score >= 75:
        return "Healthy"
    elif score >= 50:
        return "Watch"
    else:
        return "At Risk"
