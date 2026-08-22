from typing import Dict
from app.schemas import AccountEvent

# Hardcoded fallback baselines derived from synthetic MCC aggregates
MCC_BASELINES = {
    "5732": {1: 0.30, 2: 0.17, 3: 0.12, 4: 0.10, 5: 0.08, 6: 0.06, 7: 0.06, 8: 0.06, 9: 0.05}, # Electronics
    "5812": {1: 0.11, 2: 0.11, 3: 0.11, 4: 0.11, 5: 0.11, 6: 0.11, 7: 0.11, 8: 0.11, 9: 0.12}, # Dining
    "DEFAULT": {i: 1.0/9.0 for i in range(1, 10)} # Uniform fallback
}

def get_baseline(merchant_id: str, mcc_category: str, clean_txn_count: int) -> Dict[int, float]:
    # FLAW 8 MITIGATION: The New-Merchant Cold Start
    MIN_LOCAL_BASELINE_N = 10000 
    
    if clean_txn_count < MIN_LOCAL_BASELINE_N:
        # Fallback to category-level proxy if insufficient local history
        return MCC_BASELINES.get(mcc_category, MCC_BASELINES["DEFAULT"])
    else:
        # In production, this would load the merchant's specific computed baseline from Redis/DB
        return MCC_BASELINES["DEFAULT"]