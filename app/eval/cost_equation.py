import app.config as cfg

def compute_cost(fp_count: int, fn_count: int) -> float:
    # Cost of blocking a legitimate customer
    c_fp = (cfg.AVG_ORDER_VALUE * cfg.GOOD_CUSTOMER_BLOCK_RATE) + \
           (cfg.CHURN_PROB_GIVEN_FLAGGED * cfg.LTV) + \
           cfg.MANUAL_REVIEW_COST
           
    # Cost of missing a synthetic burst
    c_fn = cfg.AVG_BURST_PROMO_VALUE + \
           (cfg.NETWORK_PENALTY_PROB * cfg.PENALTY_FEE) + \
           (cfg.DETECTION_LAG_MINS * cfg.BLEED_RATE_PER_MIN)
           
    total_cost = (c_fp * fp_count) + (c_fn * fn_count)
    return total_cost