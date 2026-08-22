from fastapi import FastAPI
from app.ingestion.event_router import router as event_router

app = FastAPI(title="Ledger-Genesis", version="0.1-tracer")
app.include_router(event_router, prefix="/v1/events")

@app.get("/health")
async def health_check():
    return {"status": "ok"}