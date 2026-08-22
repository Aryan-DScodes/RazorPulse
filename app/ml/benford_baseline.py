from typing import List, Dict

def learn_baseline(merchant_id: str, clean_txn_history: List[float]) -> Dict[int, float]:
    # FLAW 1 MITIGATION: Self-Referential Rolling Baseline
    if not clean_txn_history:
        # Fallback uniform distribution if N=0 (Cold start addressed in Day 6)
        return {i: 1.0/9.0 for i in range(1, 10)}
        
    digit_counts = {i: 0 for i in range(1, 10)}
    for amount in clean_txn_history:
        first_digit = int(str(amount).replace('.', '').lstrip('0')[0])
        if 1 <= first_digit <= 9:
            digit_counts[first_digit] += 1
            
    total = sum(digit_counts.values())
    return {d: count / total for d, count in digit_counts.items()}