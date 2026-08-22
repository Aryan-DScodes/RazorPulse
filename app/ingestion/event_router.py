from fastapi import APIRouter
from app.schemas import AccountEvent, CheckoutEvent
from app.speed_layer.lsh import compute_lsh_signature
from app.speed_layer.redis_client import get_bucket_score
import json

router = APIRouter()

@router.post("/score/account")
async def score_account_event(event: AccountEvent):
    bucket_id = compute_lsh_signature(event)
    score = get_bucket_score(bucket_id)
    
    if score is None:
        score = 0.5  # Default fallback on cache miss
        
    with open("local_events_log.json", "a") as f:
        f.write(event.model_dump_json() + "\n")
        
    return {"risk_score": score, "layer": "speed"}

@router.post("/score/checkout")
async def score_checkout_event(event: CheckoutEvent):
    # Stub orchestrator for checkout
    with open("local_events_log.json", "a") as f:
        f.write(event.model_dump_json() + "\n")
    return {"risk_score": 0.5, "layer": "speed"}