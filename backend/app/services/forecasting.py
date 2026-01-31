def forecast_revenue(df, months=6):
    avg_revenue = df["revenue"].tail(3).mean()
    return [round(avg_revenue, 2)] * months

def calculate_cash_runway(df):
    avg_monthly_burn = (
        df["expense_amount"] + df["loan_emi"] - df["revenue"]
    ).mean()

    if avg_monthly_burn <= 0:
        return "Stable"

    avg_cash_buffer = df["revenue"].mean() * 0.5
    runway_months = avg_cash_buffer / avg_monthly_burn

    return round(runway_months, 1)

def generate_forecast(df):
    return {
        "revenue_forecast_6_months": forecast_revenue(df),
        "cash_runway_months": calculate_cash_runway(df)
    }
