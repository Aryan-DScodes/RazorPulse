import scipy.stats as stats
from typing import List, Dict

def synthetic_coordination_index(cohort_amounts: List[float], baseline_freq: Dict[int, float]) -> float:
    # FLAW 5 MITIGATION: The Synthetic Coordination Index
    # We discard the formal p-value (due to independence violation) and use raw Chi-Square.
    
    digit_counts = {i: 0 for i in range(1, 10)}
    for amount in cohort_amounts:
        first_digit = int(str(amount).replace('.', '').lstrip('0')[0])
        if 1 <= first_digit <= 9:
            digit_counts[first_digit] += 1
            
    observed = [digit_counts[i] for i in range(1, 10)]
    total_obs = sum(observed)
    
    if total_obs == 0:
        return 0.0
        
    expected = [baseline_freq[i] * total_obs for i in range(1, 10)]
    
    # Calculate raw statistic, explicitly ignoring the p-value
    chi2_stat, p_value = stats.chisquare(f_obs=observed, f_exp=expected)
    
    return float(chi2_stat)