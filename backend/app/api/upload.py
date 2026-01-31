from fastapi import APIRouter, UploadFile, File
from app.services.parser import parse_file
from app.services.normalizer import normalize_data

router = APIRouter()

@router.post("/upload")
async def upload_financial_file(file: UploadFile = File(...)):
    df = parse_file(file)
    monthly_df, warnings = normalize_data(df)

    return {
        "monthly_data": monthly_df.to_dict(orient="records"),
        "warnings": warnings
    }