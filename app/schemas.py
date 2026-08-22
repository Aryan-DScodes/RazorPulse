from pydantic import BaseModel, Field

# FLAW 9 ENFORCEMENT: Strictly T0 authorization telemetry only.
# Do NOT include post-T0 fields (e.g., chargeback_flag, refund_status).

class AccountEvent(BaseModel):
    account_id: str
    signup_ts: float = Field(..., description="Unix timestamp of signup")
    ip_subnet: str = Field(..., description="First 3 octets of IP or IPv6 equivalent")
    device_hash: str
    email_local_shingle: str = Field(..., description="Hash of the email prefix before the @")
    mcc_category: str = Field(..., description="Merchant Category Code proxy")

class CheckoutEvent(BaseModel):
    account_id: str
    txn_id: str
    amount: float
    ts: float = Field(..., description="Unix timestamp of checkout attempt")
    payment_instrument_hash: str