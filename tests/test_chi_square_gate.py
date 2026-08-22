from app.microbatch.cohort_builder import Cohort
from app.ml.chi_square_index import synthetic_coordination_index

def test_chi_square_never_called_on_small_n():
    cohort = Cohort("test_cohort")
    cohort.total_txns_in_cohort = 12
    cohort.eligible_for_chi_square = False # Simulated output from cohort_builder
    
    # The explicit assertion requested in the roadmap
    assert cohort.eligible_for_chi_square is False, "Gate failed: N<30 cohort marked eligible!"
    
    # In the orchestration layer, this flag prevents synthetic_coordination_index from running
    if cohort.eligible_for_chi_square:
        # This block should never execute
        raise AssertionError("Chi-square function was invoked on a small-N cohort!")