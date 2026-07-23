from rapidfuzz import fuzz
from FlexiblePlace.src.LocationMatrix import LocationMatrix

class FlexiblePlace:
    """Represents a geographic location with multiple hierarchical components stored in reverse order.
    
    Normalizes location input (string or list) to lowercase and reverses component order for standardized
    comparison. Provides methods to compare locations by similarity, retrieve components, and combine
    multiple locations into a comprehensive representation.
    
    Attributes:
        location (list[str]): Location components in reverse order (least to most specific), all lowercase.
    """
    def __init__(self, location: str | list[str], place_description: str = "") -> None:
        """Initializes a FlexiblePlace object from a location string or list of location components.
        
        Parses the input location and stores its components in reverse order (from most specific to least specific)
        and converts all components to lowercase for standardized comparison.
        
        Args:
            location (str | list[str]): Either a comma-separated string of location components 
                (e.g., "Paris, France") or a list of location component strings.
            place_description (str): FamilySearch uses PlaceDescriptions to standardize places to geo-coordinates.
        Returns:
            None.
        """
        if isinstance(location, str):
            location_components = location.split(",")
        else:
            location_components = location
        self.location: list[str] = [location_component.strip().lower() for location_component in location_components[::-1]]
        self.place_description = place_description


    def __str__(self) -> str:
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
    
    def __repr__(self) -> str:
        """FamilySearch-standardized string representation of the FlexiblePlace object.
        
        Args:
            None
        Returns:
            str: The FamilySearch PlaceDescription number
        """
        return f"{self.place_description}"
    
    def __eq__(self, other: object) -> bool:
        """Checks if two FlexiblePlace objects are equal by comparing their location components.
        
        Args:
            other (object): The object to compare with.
        Returns:
            bool: True if both objects are FlexiblePlace instances with identical location components, False otherwise.
        """
        if isinstance(other, FlexiblePlace):
            return self.location == other.location
        return False
    
    def __bool__(self) -> bool:
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
     - More specific location components will be weighted lower than less specific ones (countries are weighted heavier than cities).

    Args:
        place_a (FlexiblePlace): The first FlexiblePlace object to compare.
        place_b (FlexiblePlace): The second FlexiblePlace object to compare.
    Returns:
        float: The similarity score out of 100."""
    score: float = 100
    if not place_a or not place_b:
        return score
    scores_list: list[float] = []
    location_matrix: LocationMatrix = LocationMatrix([place_a.get_location_components(), place_b.get_location_components()])
    for i in range(location_matrix.column_count):
        component_a: str = location_matrix.get(0,i).value
        component_b: str = location_matrix.get(1,i).value
        if not component_a or not component_b:
            scores_list.append(100)
            continue
        component_score: float = fuzz.ratio(component_a, component_b)
        scores_list.append(_forgive_small_differences(component_score, i))
    score = sum(scores_list) / len(scores_list)
    return score

def _forgive_small_differences(fuzzy_score: float, index: int) -> float:
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
    # TODO: MAKE SURE TO KEEP THE place_description CONSISTANT WHEN COMBINING
    """Combines multiple FlexiblePlace objects into a single FlexiblePlace object by aligning and merging
    their location components. This function attempts to intelligently resolve conflicts and fill gaps
    across multiple place definitions to create a comprehensive location representation.
    Merging algorithm:
    *The algorithm does not move unto the next step until the current step fails to change merged_location
        1) Align components of the locations provided:
            "Washington, Utah"             ->  |             | Washington | Utah          |
            "Walla Walla, Washington"      ->  | Walla Walla | Washington |               |
            "Washington, United States"    ->  |             | Washington | United States |
            "bad data, bad data, bad data" ->  | bad data    | bad data   | bad data      |

            merged_location -> | ___ | ___ | ___ |
        2) Remove clear outliers:
            |             | Washington | Utah          |  ->  |             | Washington | Utah          |
            | Walla Walla | Washington |               |  ->  | Walla Walla | Washington |               |
            |             | Washington | United States |  ->  |             | Washington | United States |
            | bad data    | bad data   | bad data      |  ->  

            merged_location -> | Walla Walla | Washington | ___ |
        3) Remove least precise inputs:
            |             | Washington | Utah          |  ->  |             | Washington | Utah          |
            | Walla Walla | Washington |               |  ->  
            |             | Washington | United States |  ->  |             | Washington | United States |

            merged_location -> | Walla Walla | Washington | ___ |
        4) Remove inputs with the smallest components:
            |             | Washington | Utah          |  ->  
            |             | Washington | United States |  ->  |             | Washington | United States |

            merged_location -> | Walla Walla | Washington | United States |
        5) Remove the last input:
            *At this point in the example, the algorithm would have terminated after step 4 because the merged_location
            was completely filled. If the merged_location had been filled earlier in the algorithm, it would have stopped
            earlier as well. In the case that this step is reached, the last row in the location matrix is removed, then
            gets inspected to see if a new component can be determined from the remaining information.
        6) Return merged_location:
            *In the event that merged_location is unable to fill all necessary components, it is resized and returned as 
            the result.
        
    Args:
        places (list[FlexiblePlace]): A list of FlexiblePlace objects to combine.
    Returns:
        FlexiblePlace: A new FlexiblePlace object representing the combined locations.
    """
    location_matrix: LocationMatrix = LocationMatrix([place.get_location_components() for place in places])
    combined_place: list[str] = [""] * location_matrix.column_count
    while True:
        has_changed: bool = False
        for index in (i for i, comp in enumerate(combined_place) if not comp):
            location_matrix.remove_outliers(index)
            has_changed = _add_place_component(location_matrix, combined_place, index)
        if not has_changed:
            if _isFull(combined_place):
                break
            elif not location_matrix:
                combined_place = [component for component in combined_place if component]
                break
            else:
                _eliminate_partial_rows(location_matrix)
    return FlexiblePlace(combined_place)

def _add_place_component(location_matrix: LocationMatrix, combined_place: list[str], index: int) -> bool:
    """Attempt to determine and add a component for a given column index into the combined_place.
    Args:
        location_matrix (LocationMatrix): The matrix containing aligned LocationComponent objects.
        combined_place (list[str]): The target merged-place list to be filled in-place. Empty slots are represented by "".
        index (int): The column index (component position) to attempt to resolve and add.
    Returns:
        bool: True if a component was added to combined_place at index (i.e., consensus existed),
              False if no consensus could be determined and combined_place was not changed."""
    if not location_matrix:
        return False
    component_to_keep = location_matrix.column_consensus(index)
    if component_to_keep:
        combined_place[index] = component_to_keep
        return True
    else:
        return False

def _isFull(combined_place: list[str]) -> bool:
    """Return whether the merged place has no empty components.
    Args:
        combined_place (list[str]): The merged-place list to check.
    Returns:
        bool: True if combined_place contains no empty strings (all components filled), False otherwise."""
    return not "" in combined_place

def _eliminate_partial_rows(lm: LocationMatrix):
    """A row needs to be elimintated. This function picks which one by prioritizing the least empty cells"""
    if not lm.remove_least_accurate_row() and not lm.remove_row_with_smallest_component():
        lm.remove_last_row()
