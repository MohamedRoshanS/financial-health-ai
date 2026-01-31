BENCHMARKS = {
    "Retail": {
        "profit_margin": 0.22,
        "expense_ratio": 0.58,
        "debt_ratio": 0.15,
        "liquidity_ratio": 1.2
    },
    "Manufacturing": {
        "profit_margin": 0.30,
        "expense_ratio": 0.50,
        "debt_ratio": 0.20,
        "liquidity_ratio": 1.4
    },
    "Services": {
        "profit_margin": 0.35,
        "expense_ratio": 0.45,
        "debt_ratio": 0.10,
        "liquidity_ratio": 1.6
    }
}
def compute_business_metrics(df):
    total_revenue = df["revenue"].sum()
    total_expenses = df["expense_amount"].sum()
    total_emi = df["loan_emi"].sum()

    profit_margin = (total_revenue - total_expenses) / max(total_revenue, 1)
    expense_ratio = total_expenses / max(total_revenue, 1)
    debt_ratio = total_emi / max(total_revenue, 1)

    receivables = df["accounts_receivable"].mean()
    payables = max(df["accounts_payable"].mean(), 1)
    liquidity_ratio = receivables / payables

    return {
        "profit_margin": round(profit_margin, 2),
        "expense_ratio": round(expense_ratio, 2),
        "debt_ratio": round(debt_ratio, 2),
        "liquidity_ratio": round(liquidity_ratio, 2)
    }
def compare_with_benchmark(df, industry):
    if industry not in BENCHMARKS:
        return None

    business = compute_business_metrics(df)
    benchmark = BENCHMARKS[industry]

    comparison = {}

    for metric in benchmark:
        diff = business[metric] - benchmark[metric]
        comparison[metric] = {
            "business": business[metric],
            "industry_avg": benchmark[metric],
            "difference": round(diff, 2),
            "status": (
                "Better" if diff > 0 else
                "Worse" if diff < 0 else
                "Same"
            )
        }

    return comparison
