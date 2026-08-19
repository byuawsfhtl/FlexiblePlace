from rapidfuzz import fuzz
from functools import cache
from FlexiblePlace.src.LocationMatrix import LocationMatrix

def align_components(location_a: list[str], location_b: list[str]) -> list[list[str]]:
    location_matrix = LocationMatrix([location_a, location_b])
    return location_matrix.get_locations()

def compare_each_component(locations: list[list[str]]) -> list[float]:
    scores_list: list[float] = []
    location_a: list[str] = locations[0]
    location_b: list[str] = locations[1]
    return [_compare_components(component_a, component_b) for component_a, component_b in zip(location_a, location_b)]

@cache
def _compare_components(component_a: str, component_b: str) -> float:
    if not component_a or not component_b:
        return 100.0
    return fuzz.ratio(component_a, component_b)