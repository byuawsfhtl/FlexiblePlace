from FlexiblePlace.src.FlexiblePlace import FlexiblePlace

class LocationMatrix:
    """A class that represents a matrix of locations, where each row corresponds to a FlexiblePlace object
    and each column corresponds to a location component (e.g. street address, city, state/province, country).
    This class is used to align locations for comparison, ensuring that each component is compared with the 
    correct component in other locations.
    
    Example:
    locations = [FlexiblePlace("Washington, United States"),
                 FlexiblePlace("Walla Walla, Washingon"),
                 FlexiblePlace("Walla Walla, Washingon, United States")]
        location_matrix = LocationMatrix(locations)
        print(location_matrix)
        # | united states | washington |             |
        # |               | washington | walla walla |
        # | united states | washington | walla walla |
    """

    def __init__(self, locations: list[FlexiblePlace]=[]):
        self.row_count: int = 0
        self.column_count: int = 0
        self.matrix: list[list[str]] = []
        
        self.load_places(locations)
    
    def load_places(self, places: list[FlexiblePlace]):
        for flexible_place in places:
            current_location_components: list[str] = flexible_place.get_location_components()
            self.matrix.append(current_location_components)
            location_size: int = len(current_location_components)
            if location_size > self.column_count:
                self._resize(location_size)
                self.column_count = location_size
            self.row_count: int = len(self.matrix)

    def _resize(self, new_size: int):
        for row in self.matrix:
            while len(row) < new_size:
                row.append("")

# def align(location_matrix: LocationMatrix):
    # for row: int, location: list[str] in enumerate(location_matrix.locations):
        # while (true):
            # match: tuple[int, int] = _find_best_match(location_matrix, row)
            # if not match:
                # break
            # link(row, column, match)

# def _find_best_match(location_matrix: LocationMatrix, row: int) -> tuple[int, int]:
    # best_score: float = 80.0 # This (80) is the threshold for a match
    # best_match: tuple[int, int] = ()
    # for column: int in range(len(location_matrix.matrix[row])):
        # for i in range(row):
            # for j in range(location_matrix.column_count):
                # score: float = CompareLocations.basic_comparison_algorithm(location_matrix, row, column, i, j)
                # if score > best_score:
                    # best_score = score
                    # best_match = (i, j)

