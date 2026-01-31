from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.pdf_report import generate_pdf_report
from app.services.ai_insights import generate_ai_insights

router = APIRouter()

@router.post("/report")
def generate_report(payload: dict):
    analysis = payload["analysis"]

    ai_insights = generate_ai_insights(analysis)

    pdf_buffer = generate_pdf_report(analysis, ai_insights)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=financial_health_report.pdf"
        }
    )
