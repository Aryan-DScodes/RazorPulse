import math
from typing import List
from app.schemas import AccountEvent

def compute_feature_weights(events_window: List[AccountEvent]) -> dict:
    weights = {}
    total_events = len(events_window)
    
    if total_events == 0:
        return weights
        
    subnet_counts = {}
    for ev in events_window:
        subnet = ev.ip_subnet
        subnet_counts[subnet] = subnet_counts.get(subnet, 0) + 1
        
    for subnet, count in subnet_counts.items():
        # # # IDF formula: log(Total Events / Count of this Subnet)
        # # weights[subnet] = math.log(total_events / count)
        # THIS LINE ABOVE IS DUMB

        # Laplace smoothed IDF to prevent zero-weight matrix crashes
        weights[subnet] = math.log((total_events + 1) / (count + 1)) + 0.001
        
    return weights