from fastapi import APIRouter, HTTPException
import pandas as pd

from app.services.scoring import calculate_health_score, health_status
from app.services.risk_engine import identify_risks
from app.services.benchmarking import compare_with_benchmark
from app.services.forecasting import generate_forecast
from app.services.working_capital import compute_working_capital_metrics
from app.services.bookkeeping import run_bookkeeping
from app.services.gst import analyze_gst
from app.services.bank_adapter import fetch_bank_transactions
from app.services.cashflow_enrichment import enrich_with_bank_data

router = APIRouter()

@router.post("/analyze")
def analyze_financials(payload: dict):
    # -----------------------------
    # 1. Validate input contract
    # -----------------------------
    if "monthly_data" not in payload:
        raise HTTPException(status_code=400, detail="monthly_data missing in request")

    df = pd.DataFrame(payload["monthly_data"])

    # FIX: Check for empty DF before processing
    if df.empty:
        raise HTTPException(status_code=400, detail="monthly_data is empty")

    # -----------------------------
    # 2. Data Enrichment (Do this FIRST)
    # -----------------------------
    bank_account_id = payload.get("bank_account_id", "demo-account")
    transactions = fetch_bank_transactions(bank_account_id)
    
    # FIX: Enrich data first so Score and Risks use the same dataset
    df = enrich_with_bank_data(df, transactions) 
    
    # -----------------------------
    # 3. Sub-Services (Bookkeeping, GST)
    # -----------------------------
    bookkeeping = run_bookkeeping(df)

    industry = payload.get("industry", "Retail")
    gst_payload = payload.get("gst_data")
    gst_analysis = None

    if gst_payload:
        gst_analysis = analyze_gst(gst_payload, df)
    else:
        # FIX: Safe column access to prevent AttributeError
        gst_paid = df["gst_paid"].sum() if "gst_paid" in df.columns else 0.0
        gst_due = df["gst_due"].sum() if "gst_due" in df.columns else 0.0
        
        if gst_paid > 0 or gst_due > 0:
            gst_analysis = analyze_gst(
                {
                    "gst_paid": float(gst_paid),
                    "gst_due": float(gst_due),
                },
                df
            )

    # -----------------------------
    # 4. Core Analysis (Score, Risk, Forecast)
    # -----------------------------
    # Now calculating score on the Enriched DF
    score_data = calculate_health_score(df) 
    status = health_status(score_data["total_score"])
    
    risks = identify_risks(df)
    benchmarks = compare_with_benchmark(df, industry)
    forecast = generate_forecast(df)
    wc_metrics = compute_working_capital_metrics(df)

    # -----------------------------
    # 5. Final response
    # -----------------------------
    analysis = {
        "score": score_data["total_score"],
        "status": status,
        "breakdown": score_data["breakdown"],
        "risks": risks,
        "benchmarks": benchmarks,
        "forecast": forecast,
        "working_capital": wc_metrics,
        "bookkeeping": bookkeeping,
        "gst": gst_analysis,
        "bank_summary": {
            "inflows": sum(t["amount"] for t in transactions if t.get("type") == "credit"),
            "outflows": sum(t["amount"] for t in transactions if t.get("type") == "debit"),
            "transaction_count": len(transactions)
        }
    }

    return analysis