from fastapi import APIRouter, UploadFile, File
from app.services.parser import parse_file
from app.services.normalizer import normalize_data
from app.services.pdf_parser import parse_pdf

router = APIRouter()

@router.post("/upload")
async def upload_financial_file(file: UploadFile = File(...)):
    try:
        if file.filename.endswith((".xls", ".xlsx", ".csv")):
            df = parse_file(file)
            monthly_df, warnings = normalize_data(df)
        elif file.filename.endswith(".pdf"):
            file_bytes = await file.read()
            df, confidence = parse_pdf(file_bytes)
            print(f"PDF DataFrame columns: {df.columns.tolist()}")  # Debug
            print(f"PDF DataFrame:\n{df.head()}")  # Debug
            monthly_df, warnings = normalize_data(df)
        else:
            return {"error": "Unsupported file format"}
        
        return {
            "monthly_data": monthly_df.to_dict(orient="records"),
            "warnings": warnings,
            "confidence": confidence if file.filename.endswith(".pdf") else 1.0

        }
    
    
    except Exception as e:
        return {
            "error": str(e),
            "type": type(e).__name__
        }