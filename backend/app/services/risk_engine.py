def identify_risks(df):
    risks = []

    # Cash Flow Risk
    monthly_cash = df["revenue"] - df["expense_amount"] - df["loan_emi"]
    negative_months = (monthly_cash < 0).sum()
    if negative_months >= 3:
        risks.append({
            "type": "Cash Flow Risk",
            "severity": "High",
            "reason": "Negative cash flow in 3 or more months"
        })

    # Expense Risk
    total_revenue = df["revenue"].sum()
    total_expenses = df["expense_amount"].sum()
    expense_ratio = total_expenses / max(total_revenue, 1)
    if expense_ratio > 0.75:
        risks.append({
            "type": "Expense Risk",
            "severity": "Medium",
            "reason": "Expenses exceed 75% of revenue"
        })

    # Debt Risk
    total_emi = df["loan_emi"].sum()
    debt_ratio = total_emi / max(total_revenue, 1)
    if debt_ratio > 0.2:
        risks.append({
            "type": "Debt Risk",
            "severity": "High",
            "reason": "Loan EMIs consume more than 20% of revenue"
        })

    # Tax Compliance Risk
    delayed_gst_months = (df["gst_due"] > 0).sum()
    if delayed_gst_months >= 2:
        risks.append({
            "type": "Tax Compliance Risk",
            "severity": "Medium",
            "reason": "GST dues pending in multiple months"
        })

    return risks
