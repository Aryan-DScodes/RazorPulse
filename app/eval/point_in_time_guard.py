from typing import Type
from pydantic import BaseModel

# The absolute blacklist of post-authorization fields
BANNED_POST_T0_FIELDS = {"chargeback_date", "is_fraud", "refund_status", "dispute_flag"}

def audit_schema(schema_cls: Type[BaseModel]) -> list:
    """FLAW 9 MITIGATION: Static schema audit."""
    violations = []
    for field_name in schema_cls.model_fields.keys():
        if field_name in BANNED_POST_T0_FIELDS:
            violations.append(field_name)
    return violations

def enforce_as_of_cutoff(event_ts: float, as_of_ts: float):
    """FLAW 9 MITIGATION: Runtime leakage check."""
    if event_ts > as_of_ts:
        raise ValueError("Temporal Leakage Detected: Accessing future event data!")