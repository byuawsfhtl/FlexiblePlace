from __future__ import annotations

from functools import cache
from FlexiblePlace.src.LocationMatrix import LocationMatrix
from FlexiblePlace.src.auto_fill_location import auto_fill_location
from FlexiblePlace.src.get_place_description import get_place_description
from FlexiblePlace.src.Compare import Compare
from FlexiblePlace.src.Combiner import Combiner

class FlexiblePlace:
    """Represents a geographic location with multiple hierarchical components stored in reverse order.
    
    Normalizes location input (string or list) to lowercase and reverses component order for standardized
    comparison. Provides methods to compare locations by similarity, retrieve components, and combine
    multiple locations into a comprehensive representation.
    
    Attributes:
        location (list[str]): Location components in reverse order (least to most specific), all lowercase.
    """
    def __init__(self, location: str | list[str], place_description: str = "", auto_fill: bool = True) -> None:
        """Initializes a FlexiblePlace object from a location string or list of location components.
        
        Parses the input location and stores its components in reverse order (from most specific to least specific)
        and converts all components to lowercase for standardized comparison.
        
        Args:
            location (str | list[str]): Either a comma-separated string of location components 
                (e.g., "Paris, France") or a list of location component strings.
            place_description (str): FamilySearch uses PlaceDescriptions to standardize places to geo-coordinates.
            auto_fill (bool): If True, this FlexiblePlace object will guess missing data within the location (e.g. append 'United States' to 'Washington')
        Returns:
            None.
        """
        if isinstance(location, str):
            location_components = location.split(",")
        else:
            location_components = location
        self.location: list[str] = [location_component.strip().lower() for location_component in location_components]
        if auto_fill:
            auto_fill_location(self.location)
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
        return ", ".join(map(str.title, self.get_location()))
    
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

    def __hash__(self) -> int:
        """Hashes the FlexiblePlace object
        Returns:
            None."""
        location_tuple: tuple[str, ...] = tuple(self.location)
        return hash((location_tuple, self.place_description))
    
    def __bool__(self) -> bool:
        """Checks if the FlexiblePlace object contains any location components.
        
        Args:
            None
        Returns:
            bool: True if the location list is non-empty, False otherwise.
        """
        return bool(self.location)

    @staticmethod
    async def online(location: str | list[str], description: str = "", auto_fill: bool = True) -> FlexiblePlace:
        """Creates a FlexiblePlace object, retrieving the place description online if necessary.
        Args:
            location (str | list[str]): The location string or list of location components.
            description (str, optional): The place description. Defaults to "".
            auto_fill (bool, optional): Whether to auto-fill missing location components. Defaults to True.
        Returns:
            FlexiblePlace: The created FlexiblePlace object.
        """
        temp = FlexiblePlace(location, auto_fill=auto_fill)
        place_description = await get_place_description(str(temp)) if not description else description
        return FlexiblePlace(str(temp), place_description, auto_fill=auto_fill)
    
    def get_location(self) -> list[str]:
        """Returns the list of location components for this FlexiblePlace object.
        
        Args:
            None
        Returns:
            list[str]: The internal location components list in reverse order (most specific to least specific).
        """
        return self.location
    
    def compare(self, other: FlexiblePlace) -> float | int:
        """Compares this FlexiblePlace with another object and returns a similarity score.
        
        Args:
            other (object): The object to compare with.
        Returns:
            float | int: A similarity score out of 100, as returned by compare_places().
        """
        return FlexiblePlace.compare_places(self, other)

    @cache
    @staticmethod
    def compare_places(place_a: FlexiblePlace, place_b: FlexiblePlace) -> float:
        """Compares two FlexiblePlace objects and returns a similarity score out of 100.
        
        Assumes that places are given in a standardized order (e.g. City, County, State/Province, Country).
        It is effectively a glorified string comparator (Texas, USA and Texas, United States will score very low).
        Note: 
         - All location components will be compared (e.g Paris, Tx and Paris, Fl will score higher than Tx and Fl)
         - More specific location components will be weighted lower than less specific ones (countries are weighted heavier than cities).

        Args:
            place_a (FlexiblePlace): The first FlexiblePlace object to compare.
            place_b (FlexiblePlace): The second FlexiblePlace object to compare.
        Returns:
            float: The similarity score out of 100."""
        if not place_a or not place_b:
            return 100.0
        aligned_places: list[list[str]] = Compare.align_components(place_a.location, place_b.location)
        scores_list: list[float] = Compare.compare_each_component(aligned_places)
        Compare.adjust_scores(scores_list)
        average_score = sum(scores_list) / len(scores_list)
        return average_score

    @staticmethod
    def combine_flexible_places(places: list[FlexiblePlace]) -> FlexiblePlace:
        """Combines multiple FlexiblePlace objects into a single FlexiblePlace object.
        
        Args:
            places (list[FlexiblePlace]): A list of FlexiblePlace objects to combine.
        Returns:
            FlexiblePlace: A new FlexiblePlace object representing the combined locations."""
        combined_place: list[str] = FlexiblePlace._generate_combined_place(places)
        closest_match: FlexiblePlace = FlexiblePlace._find_closest_match(combined_place, places)
        place_description: str = closest_match.place_description
        return FlexiblePlace(combined_place, place_description)

    # @staticmethod
    # def _generate_combined_place(places: list[FlexiblePlace]) -> list[str]:
        """Generates a combined place from a list of FlexiblePlace objects.

        This method intelligently resolves conflicts and fills gaps across multiple place definitions 
        to create a comprehensive location representation. See merging algorithm below.
        (Note: The algorithm does not move unto the next step until the current step fails to change
        merged_location).
            
            1. Align components of the locations provided (LocationMatrix auto-aligns everything).
                ```
                "Washington, D.C."             ->  |             | Washington | D.C.          |
                "Walla Walla, Washington"      ->  | Walla Walla | Washington |               |
                "Washington, United States"    ->  |             | Washington | United States |
                "bad data, bad data, bad data" ->  | bad data    | bad data   | bad data      |

                merged_location -> | ___ | ___ | ___ |
                ```
            
            2. Remove clear outliers (checks column by column, beginning with the least specific component).
                ```
                |             | Washington | D.C.          |  ->  |             | Washington | D.C.          |
                | Walla Walla | Washington |               |  ->  | Walla Walla | Washington |               |
                |             | Washington | United States |  ->  |             | Washington | United States |
                | bad data    | bad data   | bad data      |  ->  

                merged_location -> | Walla Walla | Washington | ___ |
                ```
            
            3. Remove least precise inputs (meaning those with empty columns).
                ```
                |             | Washington | D.C.          |  ->  |             | Washington | D.C.          |
                | Walla Walla | Washington |               |  ->  
                |             | Washington | United States |  ->  |             | Washington | United States |

                merged_location -> | Walla Walla | Washington | ___ |
                ```
            
            4. Remove inputs with the smallest components ('smallest' meaning least characters).
                ```
                |             | Washington | D.C.          |  ->  
                |             | Washington | United States |  ->  |             | Washington | United States |

                merged_location -> | Walla Walla | Washington | United States |
                ```

            5. Remove the last input.
                *At this point in the example, the algorithm would have terminated after step 4 because the merged_location
                was completely filled. If the merged_location had been filled earlier in the algorithm, it would have stopped
                earlier as well. In the case that this step is reached, the last row in the location matrix is removed, then
                gets inspected to see if a new component can be determined from the remaining information.
            
            6. Return merged_location.
                *In the event that merged_location is still unable to fill all necessary components, it is resized and returned as 
                the result.
        
        Args:
            places (list[FlexiblePlace]): A list of FlexiblePlace objects to combine.
        Returns:
            list[str]: A list of location components representing the combined place
        """
        location_matrix: LocationMatrix = LocationMatrix([place.location for place in places])
        aligned_places: Combiner = Combiner([place.get_location() for place in places])
        combined_place: list[str] = [""] * location_matrix.column_count
        while True:
            has_changed: bool = False
            for index in (i for i, comp in enumerate(combined_place) if not comp):
                location_matrix.remove_outliers(index)
                has_changed |= FlexiblePlace._add_place_component(location_matrix, combined_place, index)
            if not has_changed:
                if FlexiblePlace._isFull(combined_place):
                    break
                elif not location_matrix:
                    combined_place = [component for component in combined_place if component]
                    break
                else:
                    FlexiblePlace._eliminate_partial_rows(location_matrix)
        return combined_place[::-1]

    @staticmethod
    def _generate_combined_place(places: list[FlexiblePlace]) -> list[str]:
        """Generates a combined place from a list of FlexiblePlace objects.

        This method intelligently resolves conflicts and fills gaps across multiple place definitions 
        to create a comprehensive location representation. See merging algorithm below.
        (Note: The algorithm does not move unto the next step until the current step fails to change
        merged_location).
            
            1. Align components of the locations provided (LocationMatrix auto-aligns everything).
                ```
                "Washington, D.C."             ->  |             | Washington | D.C.          |
                "Walla Walla, Washington"      ->  | Walla Walla | Washington |               |
                "Washington, United States"    ->  |             | Washington | United States |
                "bad data, bad data, bad data" ->  | bad data    | bad data   | bad data      |

                merged_location -> | ___ | ___ | ___ |
                ```
            
            2. Remove clear outliers (checks column by column, beginning with the least specific component).
                ```
                |             | Washington | D.C.          |  ->  |             | Washington | D.C.          |
                | Walla Walla | Washington |               |  ->  | Walla Walla | Washington |               |
                |             | Washington | United States |  ->  |             | Washington | United States |
                | bad data    | bad data   | bad data      |  ->  

                merged_location -> | Walla Walla | Washington | ___ |
                ```
            
            3. Remove least precise inputs (meaning those with empty columns).
                ```
                |             | Washington | D.C.          |  ->  |             | Washington | D.C.          |
                | Walla Walla | Washington |               |  ->  
                |             | Washington | United States |  ->  |             | Washington | United States |

                merged_location -> | Walla Walla | Washington | ___ |
                ```
            
            4. Remove inputs with the smallest components ('smallest' meaning least characters).
                ```
                |             | Washington | D.C.          |  ->  
                |             | Washington | United States |  ->  |             | Washington | United States |

                merged_location -> | Walla Walla | Washington | United States |
                ```

            5. Remove the last input.
                *At this point in the example, the algorithm would have terminated after step 4 because the merged_location
                was completely filled. If the merged_location had been filled earlier in the algorithm, it would have stopped
                earlier as well. In the case that this step is reached, the last row in the location matrix is removed, then
                gets inspected to see if a new component can be determined from the remaining information.
            
            6. Return merged_location.
                *In the event that merged_location is still unable to fill all necessary components, it is resized and returned as 
                the result.
        
        Args:
            places (list[FlexiblePlace]): A list of FlexiblePlace objects to combine.
        Returns:
            list[str]: A list of location components representing the combined place
        """
        aligned_places: Combiner = Combiner([place.get_location() for place in places])
        combined_place: list[str] = [""] * aligned_places.get_column_count()
        eliminate_row_strategies = [
            aligned_places.remove_outliers,
            aligned_places.remove_least_precise,
            aligned_places.remove_smallest_component,
            aligned_places.remove_last
        ]
        while Combiner.is_not_filled(combined_place):
            for strategy in eliminate_row_strategies:
                starting_row_count: int = aligned_places.get_row_count()
                strategy()
                has_changed = aligned_places.fill_in(combined_place)
                if has_changed or starting_row_count > aligned_places.get_row_count():
                    break
            if aligned_places.is_empty():
                Combiner.resize(combined_place)
        return combined_place


    @staticmethod
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

    @staticmethod
    def _isFull(combined_place: list[str]) -> bool:
        """Return whether the merged place has no empty components.
        Args:
            combined_place (list[str]): The merged-place list to check.
        Returns:
            bool: True if combined_place contains no empty strings (all components filled), False otherwise."""
        return not "" in combined_place

    @staticmethod
    def _eliminate_partial_rows(lm: LocationMatrix) -> None:
        """A row needs to be eliminated. This function picks which one by prioritizing the least empty cells.
        Args: 
            lm (LocationMatrix): LocationMatrix object to be pruned.
        Returns:
            None."""
        if not lm.remove_least_accurate_row() and not lm.remove_row_with_smallest_component():
            lm.remove_last_row()

    @staticmethod
    def _find_closest_match(combined_place: list[str], places: list[FlexiblePlace]) -> FlexiblePlace:
        """The place_description of the most similar FlexiblePlace to the target is returned.
        Args:
            combined_place (list[str]): The target location to be compared with.
            places (list[FlexiblePlace]): FlexiblePlace objects to compare.
        Returns:
            str: The place_description of the closest match. (Ties are broken by number of components)."""
        target: FlexiblePlace = FlexiblePlace(combined_place, auto_fill = False)
        scores: list[float] = [target.compare(place) for place in places]
        max_score: float = max(scores, default=0)
        if max_score < 90:
            max_score = 101 # If the closest match is worse than a 90% match, then there will be no "best match." Method will just return `target`
        best_matches: list[FlexiblePlace] = [places[i] for i in range(len(scores)) if scores[i] == max_score and places[i].place_description]
        best_match: FlexiblePlace = max(best_matches, key=lambda place: len(place.location), default=target)
        return best_match

    @staticmethod
    async def combine_flexible_places_online(places: list[FlexiblePlace]) -> FlexiblePlace:
        """Combines multiple FlexiblePlace objects into a single FlexiblePlace object. Retrieves the place description online if necessary.
        Args:
            places (list[FlexiblePlace]): The list of FlexiblePlace objects to combine.
        Returns:
            FlexiblePlace: The combined FlexiblePlace object."""
        combined_place: list[str] = FlexiblePlace._generate_combined_place(places)
        closest_match: FlexiblePlace = FlexiblePlace._find_closest_match(combined_place, places)
        temp: FlexiblePlace = FlexiblePlace(combined_place)
        place_description: str = await get_place_description(str(temp)) if not closest_match.place_description or len(closest_match.location) < len(temp.location) else closest_match.place_description
        return FlexiblePlace(combined_place, place_description)
