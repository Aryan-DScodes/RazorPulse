import requests
import time
import random
import threading
import sys

API_URL = "http://localhost:8000/v1/events/score/checkout"

def send_checkout(is_bot=False):
    """Fires a single HTTP POST to the backend."""
    if is_bot:
        payload = {
            "account_id": f"bot-farm-{random.randint(100, 999)}", 
            "txn_id": f"txn-{int(time.time()*1000)}", 
            "amount": 99.0, # The heuristic trigger for our Flaw 7 bot
            "ts": time.time(), 
            "payment_instrument_hash": "stolen_hash",
            "ip_subnet": "10.0.0.99/24"
        }
    else:
        payload = {
            "account_id": f"human-{random.randint(1000, 9999)}", 
            "txn_id": f"txn-{int(time.time()*1000)}", 
            "amount": round(random.uniform(10.0, 500.0), 2), 
            "ts": time.time(), 
            "payment_instrument_hash": f"secure_hash_{random.randint(1, 100)}",
            "ip_subnet": f"192.168.{random.randint(1,255)}.0/24"
        }
        
    try:
        requests.post(API_URL, json=payload)
    except requests.exceptions.ConnectionError:
        pass # Silently fail if server is off during testing

def run_baseline_traffic():
    """Endless loop simulating continuous human checkouts."""
    print("🟢 [Baseline] Starting continuous human traffic stream...")
    while True:
        send_checkout(is_bot=False)
        time.sleep(0.4) # Control the speed of the baseline heartbeat

def trigger_adversarial_burst():
    """Injects a highly coordinated synthetic burst."""
    print("\n🚨 [ATTACK] Injecting high-density adversarial burst (Flaw 7)...")
    for _ in range(40):
        send_checkout(is_bot=True)
        time.sleep(0.02) # Extremely fast burst
    print("🚨 [ATTACK] Burst complete.\n")

if __name__ == "__main__":
    print("🛡️ RazorPulse Synthetic Traffic Generator")
    print("----------------------------------------")
    
    # Start the continuous background heartbeat
    baseline_thread = threading.Thread(target=run_baseline_traffic, daemon=True)
    baseline_thread.start()
    
    # Interactive CLI to trigger bursts manually
    try:
        while True:
            cmd = input("Press [ENTER] to inject an Adversarial Burst, or [CTRL+C] to quit: \n")
            trigger_adversarial_burst()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down traffic generator.")
        sys.exit(0)