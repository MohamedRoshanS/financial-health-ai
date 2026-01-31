from fastapi import APIRouter
from app.services.ai_insights import generate_ai_insights
from app.services.translator import translate_text

router = APIRouter()

@router.post("/insights")
def get_ai_insights(payload: dict):
    analysis = payload["analysis"]
    language = payload.get("language", "en")

    insights = generate_ai_insights(analysis)
    translated = translate_text(insights, language)

    return {
        "language": language,
        "insights": translated
    }
