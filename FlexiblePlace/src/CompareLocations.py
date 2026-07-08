from FlexiblePlace.src.LocationMatrix import LocationMatrix
from rapidfuzz import fuzz

def basic_comparison_algorithm(location_matrix: LocationMatrix, row_a: int, column_a: int, row_b: int, column_b: int) -> float:
    """Calculates a score out of 100 of the likelihood that 2 location components refer to the same location.
    This is done by taking the fuzzy string score of the two components and then deducting points for these reasons:
        1. The strings are short
        2. The strings are misaligned (the algorithm will favor location components that are already aligned)

    Args:
        location_matrix (LocationMatrix): LocationMatrix instance holding the components to be compared
        row_a (int): row index of first component
        column_a (int): column index of first component
        row_b (int): row index of second component
        column_b (int): column index of second component
    Returns:
        Score (float) out of 100
    """
    
    component_a: str = location_matrix.matrix[row_a][column_a]
    component_b: str = location_matrix.matrix[row_b][column_b]
    if component_a == "" or component_b == "":
        return 0.0
    
    fuzzy_score: float = fuzz.ratio(component_a, component_b)
    
    component_b_length: int = len(component_a)
    deduction_for_small_component_length: float = 2 ** -(component_b_length-1) # More letters = smaller score deduction
    
    misalignment: int = abs(column_a-column_b)
    deduction_for_misalignment: int = misalignment ** 3 # A street address compared with a country will have a high deduction
    
    return fuzzy_score - deduction_for_small_component_length - deduction_for_misalignment
