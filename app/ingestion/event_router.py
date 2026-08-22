from fastapi import APIRouter
from app.schemas import AccountEvent, CheckoutEvent
import json

router = APIRouter()

@router.post("/score/account")
async def score_account_event(event: AccountEvent):
    # Stub: Day 1 plumbing trace
    with open("local_events_log.json", "a") as f:
        f.write(event.model_dump_json() + "\n")
    return {"risk_score": 0.5, "layer": "speed"}

@router.post("/score/checkout")
async def score_checkout_event(event: CheckoutEvent):
    # Stub: Day 1 plumbing trace
    with open("local_events_log.json", "a") as f:
        f.write(event.model_dump_json() + "\n")
    return {"risk_score": 0.5, "layer": "speed"}