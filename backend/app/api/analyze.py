from fastapi import APIRouter
import pandas as pd
from app.services.scoring import calculate_health_score, health_status
from app.services.risk_engine import identify_risks
from app.services.benchmarking import compare_with_benchmark
from app.services.forecasting import generate_forecast


router = APIRouter()

@router.post("/analyze")
def analyze_financials(payload: dict):
    df = pd.DataFrame(payload["monthly_data"])
    industry = payload.get("industry", "Retail")

    score_data = calculate_health_score(df)
    status = health_status(score_data["total_score"])
    risks = identify_risks(df)
    benchmarks = compare_with_benchmark(df, industry)
    forecast = generate_forecast(df)

    return {
        "score": score_data["total_score"],
        "status": status,
        "breakdown": score_data["breakdown"],
        "risks": risks,
        "benchmarks": benchmarks,
        "forecast": forecast
    }   