import pytest
from pydantic import BaseModel
from app.eval.point_in_time_guard import audit_schema, enforce_as_of_cutoff

def test_static_schema_audit_fails_on_leakage():
    # We deliberately create a leaky schema to test our trap
    class LeakyEvent(BaseModel):
        account_id: str
        is_fraud: bool  # This should trigger the alarm!

    violations = audit_schema(LeakyEvent)
    assert "is_fraud" in violations, "Flaw 9 Fail: Static guard missed a banned future field!"

def test_runtime_cutoff_enforcement():
    t0_authorization_time = 1700000000.0
    future_chargeback_time = 1700000500.0 
    
    # Assert that the system crashes if it tries to look into the future
    with pytest.raises(ValueError, match="Temporal Leakage"):
        enforce_as_of_cutoff(event_ts=future_chargeback_time, as_of_ts=t0_authorization_time)