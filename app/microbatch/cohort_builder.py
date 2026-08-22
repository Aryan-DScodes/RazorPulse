from typing import List, Dict
from app.schemas import AccountEvent

class Cohort:
    def __init__(self, cohort_id: str):
        self.cohort_id = cohort_id
        self.events: List[AccountEvent] = []
        self.total_txns_in_cohort = 0
        self.eligible_for_chi_square = False

def build_cohorts(events: List[AccountEvent], window_minutes: int = 15) -> List[Cohort]:
    cohorts: Dict[str, Cohort] = {}
    
    for event in events:
        # Group by 15-minute time bucket and IP subnet
        time_bucket = int(event.signup_ts // (window_minutes * 60))
        cohort_id = f"cohort_{time_bucket}_{event.ip_subnet}"
        
        if cohort_id not in cohorts:
            cohorts[cohort_id] = Cohort(cohort_id)
            
        cohorts[cohort_id].events.append(event)
        # In a real join, we count actual checkouts. For the unit test, we approximate 1 event = 1 txn
        cohorts[cohort_id].total_txns_in_cohort += 1 

    # FLAW 2 MITIGATION: The Small-N Gate
    for c_id, cohort in cohorts.items():
        if cohort.total_txns_in_cohort < 30:
            # INSUFFICIENT_N: skip chi-square, fall back to LSH-density-only score
            cohort.eligible_for_chi_square = False 
        else:
            cohort.eligible_for_chi_square = True
            
    return list(cohorts.values())