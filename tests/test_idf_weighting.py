import time
from app.schemas import AccountEvent
from app.ml.idf_weighting import compute_feature_weights

def test_cgnat_downweighting():
    events = []
    
    # Simulate 500 legitimate users on ONE Jio CGNAT IP
    for i in range(500):
        events.append(AccountEvent(
            account_id=f"legit_{i}", signup_ts=time.time(), 
            ip_subnet="49.36.0.0/24",  # A common Jio subnet
            device_hash=f"hash_{i}", email_local_shingle=f"user{i}", mcc_category="5732"
        ))
        
    # Simulate a small 10-account bot ring on a distinct, rare IP
    for i in range(10):
        events.append(AccountEvent(
            account_id=f"bot_{i}", signup_ts=time.time(), 
            ip_subnet="192.168.100.0/24", 
            device_hash="shared_bot_hash", email_local_shingle="bot", mcc_category="5732"
        ))
        
    weights = compute_feature_weights(events)
    
    jio_weight = weights.get("49.36.0.0/24", 1.0)
    bot_weight = weights.get("192.168.100.0/24", 1.0)
    
    # The common Jio IP should be severely down-weighted compared to the rare bot IP
    assert jio_weight < bot_weight, "Flaw 4 Fail: CGNAT IP was not down-weighted!"
    
    # The weight should not mathematically break our distance function (weight must be > 0)
    assert jio_weight > 0, f"Critical Math Failure: Jio IP weight is {jio_weight}. This will cause distance to become 0 and auto-flag as fraud!"