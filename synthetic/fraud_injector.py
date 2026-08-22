import random
import time
from typing import List, Tuple
from app.schemas import AccountEvent, CheckoutEvent

def inject_burst(burst_size: int, is_adversarial: bool = False) -> Tuple[List[AccountEvent], List[CheckoutEvent]]:
    """
    Injects a highly coordinated bot ring burst.
    """
    burst_accounts = []
    burst_checkouts = []
    
    # Highly coordinated telemetry (Flaw 3 & 4 triggers)
    shared_ip = "10.0.0.99/24"
    shared_device = "bot_farm_hash_xyz"
    base_time = time.time()
    
    for i in range(burst_size):
        acc_id = f"synthetic_bot_{i}"
        
        # Tight signup window (all within 5 seconds)
        burst_accounts.append(AccountEvent(
            account_id=acc_id,
            signup_ts=base_time + random.uniform(0, 5),
            ip_subnet=shared_ip,
            device_hash=shared_device,
            email_local_shingle=f"promo_abuser_{i}",
            mcc_category="5732"
        ))
        
        # 1-2 transactions per account (Flaw 2 behavior)
        for _ in range(random.randint(1, 2)):
            if is_adversarial:
                # FLAW 7 EVASION ATTEMPT: Mimics the merchant's charm pricing
                amt = random.choice([99.0, 499.0])
            else:
                # Naive bot: draining max promo value
                amt = random.uniform(800.0, 1000.0)
                
            burst_checkouts.append(CheckoutEvent(
                account_id=acc_id,
                txn_id=f"bot_txn_{random.randint(1000,9999)}",
                amount=amt,
                ts=base_time + random.uniform(10, 60),
                payment_instrument_hash="stolen_card_hash_001"
            ))
            
    return burst_accounts, burst_checkouts