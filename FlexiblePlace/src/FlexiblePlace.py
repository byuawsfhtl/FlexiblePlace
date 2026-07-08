from rapidfuzz import fuzz

class FlexiblePlace:
    def __init__(self, location: str | list[str]):
        if isinstance(location, str):
            location_components = location.split(",")
        else:
            location_components = location
        self.location: list[str] = [location_component.strip().lower() for location_component in location_components[::-1]]


    def __str__(self):
        #Needs work to be able to output abreviations well (e.g. United States vs Usa, D.C. vs D.c)
        return ", ".join(map(str.title, self.location))
    
    def __repr__(self):
        return f"FlexiblePlace({self.location})"
    
    def __eq__(self, other: object):
        if isinstance(other, FlexiblePlace):
            return self.location == other.location
        return False
    
    def __bool__(self):
        return bool(self.location)
    
    def get_location_components(self) -> list[str]:
        return self.location
    
    def compare(self, other: object) -> float | int:
        return compare_places(self, other)
    

@staticmethod
def compare_places(place_a: FlexiblePlace, place_b: FlexiblePlace) -> float:
    """Compares two FlexiblePlace objects and returns a similarity score out of 100. Assumes that places
    are given in a standardized order (e.g. Street address, City, County, State/Province, Country).
    It is effectively a glorified string comparator (Texas, USA and Texas, United States will score very low).
    Note: 
     - All address components will be compared (e.g Paris, Tx and Paris, Fl will score higher than Tx and Fl)
     - More specific address components will be weighted lower than less specific ones (countries are weighted heavier than cities)

    Args:
        place_a (FlexiblePlace): The first FlexiblePlace object to compare.
        place_b (FlexiblePlace): The second FlexiblePlace object to compare.
    Returns:
        float: The similarity score out of 100.
    """
    score: float = 100
    if not place_a or not place_b:
        return score
    scores_list: list[float] = []
    place_a_components: list[str] = place_a.location
    place_b_components: list[str] = place_b.location
    minLen: int = min(len(place_a_components), len(place_b_components))
    for i in range(minLen):
        component_a: str = place_a_components[i]
        component_b: str = place_b_components[i]
        if not component_a or not component_b:
            scores_list.append(100)
            continue
        component_score: float = fuzz.ratio(component_a, component_b)
        scores_list.append(forgive_small_differences(component_score, i))
    score = sum(scores_list) / len(scores_list)
    return score

def forgive_small_differences(fuzzy_score: float, index: int) -> float:
    """Forgives small differences in the fuzzy score based on the index of the component being compared.
    The higher the index, the less important the component is, and thus the more forgiving the score should be.
    For example, a difference in the country component (index 0) should be less forgiving than a difference
    in the city component (index 1).
    
    Args:
        fuzzy_score (float): The fuzzy score to forgive.
        index (int): The index of the component being compared.
    Returns:
        float: The new score.
    """
    component_penalty: float = 0.5 # How harshly to penalize differences in components (With 0.5, about 65% of a 
    # difference in street address will be forgiven as opposed to 30% with the state)
    forgiveness_factor: float = (1 - 2 ** -(index * component_penalty)) # As index increases, more forgiveness is granted.
    redeemed_points: float = (100 - fuzzy_score) * forgiveness_factor # Redeems a certain percentage of lost points
    return fuzzy_score + redeemed_points
    
# def align_places(places: list[FlexiblePlace]) -> LocationMatrix:
    # aligned_places: LocationMatrix = LocationMatrix()
    # aligned_places.load_places(places)
    # aligned_places.align()
    # return aligned_places

@staticmethod
def combine_flexible_places(places: list[FlexiblePlace]) -> FlexiblePlace:
    # aligned_places: LocationMatrix = align_places(places)
    # combined_place: list[str] = generate_combined_place_format(aligned_places)
    # while true:
        # empty_indeces: list[int] = find_empty_indeces(combined_place)
        # for index in empty_indeces:
            # remove_outliers(aligned_places, index)
            # add_place_component(aligned_places, combined_place, index)
        # if nothing_has_changed:
            # if isFull(combined_place):
                # break
            # elif isEmpty(aligned_places):
                # resize_combined_place(combined_place)
                # break
            # else:
                # eliminate_partial_rows(aligned_places)
    # return FlexiblePlace(combined_place)
    return FlexiblePlace("place holder")
