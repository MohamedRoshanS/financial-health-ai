from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from app.services.pdf_report import generate_pdf_report
from app.services.ai_insights import generate_ai_insights
from datetime import datetime
import logging
import traceback

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/report")
async def generate_report(payload: dict):
    try:
        logger.info("Received report generation request")
        
        analysis = payload.get("analysis")
        if not analysis:
            logger.error("Missing analysis data in request")
            return JSONResponse(
                status_code=400,
                content={"error": "Missing analysis data"}
            )
        
        logger.info(f"Generating PDF report for analysis with score: {analysis.get('score', 'N/A')}")
        
        # Generate AI insights (with fallback)
        try:
            ai_insights = generate_ai_insights(analysis)
            logger.info("AI insights generated successfully")
        except Exception as e:
            logger.warning(f"Failed to generate AI insights: {str(e)}")
            ai_insights = "AI insights unavailable. Please try again later."
        
        # Generate PDF
        try:
            pdf_buffer = generate_pdf_report(analysis, ai_insights)
            logger.info("PDF buffer created successfully")
        except Exception as e:
            logger.error(f"PDF generation failed: {str(e)}")
            logger.error(traceback.format_exc())
            return JSONResponse(
                status_code=500,
                content={"error": f"PDF generation failed: {str(e)}"}
            )
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"financial_health_report_{timestamp}.pdf"
        
        logger.info(f"Returning PDF with filename: {filename}")
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except Exception as e:
        logger.error(f"Unexpected error in report endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )