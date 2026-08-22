from typing import Optional

def get_bucket_score(bucket_id: str) -> Optional[float]:
    # Day 1 Stub: Always simulate a cache miss (because the batch layer isn't running yet)
    return None

def set_bucket_score(bucket_id: str, score: float, ttl: int) -> None:
    # Day 1 Stub: Print instead of actual Redis SETEX
    print(f"[REDIS STUB] SETEX {bucket_id} {ttl} {score}")