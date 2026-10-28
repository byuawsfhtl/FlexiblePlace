from FlexiblePlace.src.LocationComponent import LocationComponent
from rapidfuzz import fuzz
from functools import cache

# This is where the magic happens when deciding if two LocationComponents are a close enough match to link
# together. Most issues with compare FlexiblePlace objects and combining them together can be traced back to 
# how accurately the components line up. Thus, the comparison algorithms in this file will be the primary method
# to costumization as to how precisely FlexiblePlace objects are compared and combined 

@cache
def basic_comparison_algorithm(location_a: LocationComponent, location_b: LocationComponent) -> float:
    """Calculates a score out of 100 of the likelihood that 2 location components refer to the same location.
    This is done by taking the fuzzy string score of the two components and then deducting points for these reasons:
        1. The strings are short.
        2. The strings are misaligned (the algorithm will favor location components that are already aligned).

    Args:
        location_a (LocationComponent): first component.
        location_b (LocationComponent): second component.
    Returns:
        Score (float) out of 100."""
    
    component_a: str = location_a.value
    component_b: str = location_b.value
    if component_a == "" or component_b == "":
        return 0.0
    
    fuzzy_score: float = fuzz.ratio(component_a, component_b)
    
    component_b_length: int = len(component_b)
    deduction_for_small_component_length: float = 2 ** -(component_b_length-1) # More letters = smaller score deduction

    column_a = location_a.column
    column_b = location_b.column
    misalignment: int = abs(column_a-column_b)
    deduction_for_misalignment: int = misalignment ** 3 # A street address compared with a country will have a high deduction
    
    return fuzzy_score - deduction_for_small_component_length - deduction_for_misalignment
