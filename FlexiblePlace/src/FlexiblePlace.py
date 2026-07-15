from rapidfuzz import fuzz
from FlexiblePlace.src.LocationMatrix import LocationMatrix

class FlexiblePlace:
    def __init__(self, location: str | list[str]):
        """Initializes a FlexiblePlace object from a location string or list of location components.
        
        Parses the input location and stores its components in reverse order (from most specific to least specific)
        and converts all components to lowercase for standardized comparison.
        
        Args:
            location (str | list[str]): Either a comma-separated string of location components 
                (e.g., "Paris, France") or a list of location component strings.
        Returns:
            None
        """
        if isinstance(location, str):
            location_components = location.split(",")
        else:
            location_components = location
        self.location: list[str] = [location_component.strip().lower() for location_component in location_components[::-1]]


    def __str__(self):
        """Returns a human-readable string representation of the FlexiblePlace object.
        
        Converts the location components back to title case and joins them with commas.
        Note: This currently has limitations with abbreviations (e.g., "United States" vs "Usa", "D.C." vs "D.c").
        
        Args:
            None
        Returns:
            str: A formatted location string with title-cased components.
        """
        #Needs work to be able to output abreviations well (e.g. United States vs Usa, D.C. vs D.c)
        return ", ".join(map(str.title, self.location))
    
    def __repr__(self):
        """Returns a developer-friendly string representation of the FlexiblePlace object.
        
        Args:
            None
        Returns:
            str: A string representing the FlexiblePlace object and its internal location list.
        """
        return f"FlexiblePlace({self.location})"
    
    def __eq__(self, other: object):
        """Checks if two FlexiblePlace objects are equal by comparing their location components.
        
        Args:
            other (object): The object to compare with.
        Returns:
            bool: True if both objects are FlexiblePlace instances with identical location components, False otherwise.
        """
        if isinstance(other, FlexiblePlace):
            return self.location == other.location
        return False
    
    def __bool__(self):
        """Checks if the FlexiblePlace object contains any location components.
        
        Args:
            None
        Returns:
            bool: True if the location list is non-empty, False otherwise.
        """
        return bool(self.location)
    
    def get_location_components(self) -> list[str]:
        """Returns the list of location components for this FlexiblePlace object.
        
        Args:
            None
        Returns:
            list[str]: The internal location components list in reverse order (most specific to least specific).
        """
        return self.location
    
    def compare(self, other: object) -> float | int:
        """Compares this FlexiblePlace with another object and returns a similarity score.
        
        Args:
            other (object): The object to compare with.
        Returns:
            float | int: A similarity score out of 100, as returned by compare_places().
        """
        return compare_places(self, other)
    

@staticmethod
def compare_places(place_a: FlexiblePlace, place_b: FlexiblePlace) -> float:
    """Compares two FlexiblePlace objects and returns a similarity score out of 100. Assumes that places
    are given in a standardized order (e.g. City, County, State/Province, Country).
    It is effectively a glorified string comparator (Texas, USA and Texas, United States will score very low).
    Note: 
     - All location components will be compared (e.g Paris, Tx and Paris, Fl will score higher than Tx and Fl)
     - More specific location components will be weighted lower than less specific ones (countries are weighted heavier than cities)

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
    location_matrix: LocationMatrix = LocationMatrix([place_a.get_location_components(), place_b.get_location_components()])
    for i in range(location_matrix.column_count):
        component_a: str = location_matrix.matrix[0][i].value
        component_b: str = location_matrix.matrix[1][i].value
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
    For example, a difference in the country component should be less forgiving than a difference in the city 
    component.
    
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

@staticmethod
def combine_flexible_places(places: list[FlexiblePlace]) -> FlexiblePlace:
    """UPDATE THIS DOCSTRING
    Combines multiple FlexiblePlace objects into a single FlexiblePlace object by aligning and merging
    their location components. This function attempts to intelligently resolve conflicts and fill gaps
    across multiple place definitions to create a comprehensive location representation.
    
    Args:
        places (list[FlexiblePlace]): A list of FlexiblePlace objects to combine.
    Returns:
        FlexiblePlace: A new FlexiblePlace object representing the combined locations.
    """
    # THE PSEUDOCODE BELOW IS ALSO OUTDATED
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
