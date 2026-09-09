from FlexiblePlace.src.location_component import LocationComponent
from math import floor as math_floor
from rapidfuzz.fuzz import ratio as fuzz_ratio
from functools import lru_cache

# This is where the magic happens when deciding if two LocationComponents are a close enough match to link
# together. Most issues with compare FlexiblePlace objects and combining them together can be traced back to 
# how accurately the components line up. Thus, the comparison algorithms in this file will be the primary method
# to costumization as to how precisely FlexiblePlace objects are compared and combined 

@lru_cache(1000)
def basic_comparison_algorithm(location_one: LocationComponent, location_two: LocationComponent) -> float:
    """Calculates a score out of 100 of the likelihood that 2 location components refer to the same location.
    This is done by taking the fuzzy string score of the two components and then deducting points for these reasons:
        1. The strings are short.
        2. The strings are misaligned (the algorithm will favor location components that are already aligned).

    Args:
        location_one (LocationComponent): first component.
        location_two (LocationComponent): second component.
    Returns:
        A percent score (float) out of 100
    """
    
    component_one: str = location_one.value
    component_two: str = location_two.value
    if component_one == "" or component_two == "":
        return 0.0

    # If we don't use math floor, this could round unusually due to python rounding
    fuzzy_score: float = math_floor(fuzz_ratio(component_one, component_two))
    deduction_for_small_component_length: float = 2 ** -(len(component_two) - 1) # More letters = smaller score deduction
    misalignment: int = abs(location_one.column - location_two.column)
    deduction_for_misalignment: int = misalignment ** 3 # A street address compared with a country will have a high deduction
    
    return (fuzzy_score - deduction_for_small_component_length - deduction_for_misalignment)
