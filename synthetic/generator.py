import json
import time
import random
from faker import Faker
from datetime import datetime

fake = Faker()

def generate_account_event():
    return {
        "account_id": fake.uuid4(),
        "signup_ts": time.time(),
        "ip_subnet": f"{fake.ipv4_private_class_c().rsplit('.', 1)[0]}.0/24",
        "device_hash": fake.sha256()[:16],
        "email_local_shingle": fake.email().split('@')[0][:4],
        "mcc_category": random.choice(["5732", "5812", "5691"]) # Electronics, Dining, Clothing
    }

def generate_checkout_event(account_id):
    return {
        "account_id": account_id,
        "txn_id": fake.uuid4(),
        "amount": round(random.choice([99.0, 499.0, random.uniform(10, 1000)]), 2),
        "ts": time.time(),
        "payment_instrument_hash": fake.sha256()[:16]
    }

if __name__ == "__main__":
    print("Generating baseline synthetic traffic...")
    with open("local_events_log.json", "a") as f:
        for _ in range(10): # Generate 10 clean accounts
            acc = generate_account_event()
            f.write(json.dumps(acc) + "\n")
            
            # Each account does 1-3 checkouts
            for _ in range(random.randint(1, 3)):
                chk = generate_checkout_event(acc["account_id"])
                f.write(json.dumps(chk) + "\n")
    print("Traffic appended to local_events_log.json")