from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.upload import router as upload_router 
from app.api.analyze import router as analyze_router 
from app.api.insights import router as insights_router
from app.api.report import router as report_router


app = FastAPI(title="Financial Health AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(upload_router)
app.include_router(analyze_router)
app.include_router(insights_router)
app.include_router(report_router)


@app.get("/")
def health_check():
    return {"status": "Backend running"}
