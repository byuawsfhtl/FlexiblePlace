from rapidfuzz import fuzz
from FlexiblePlace.src.FlexiblePlace import FlexiblePlace

class LocationMatrix:
    """A class that represents a matrix of locations, where each row corresponds to a FlexiblePlace object
    and each column corresponds to a location component (e.g. street address, city, state/province, country).
    This class is used to align locations for comparison, ensuring that each component is compared with the 
    correct component in other locations."""
    def __init__(self, locations: list[FlexiblePlace]):
        self.rows: int = len(locations)
        self.columns: int = 0
        self.matrix: list[list[str]] = []
        self.load_places(locations)
    
    def load_places(self, places: list[FlexiblePlace]):
        for flexible_place in places:
            current_location_components: list[str] = flexible_place.get_location_components()
            self.matrix.append(current_location_components)
            location_size: int = len(current_location_components)
            if location_size > self.columns:
                self.__resize__(location_size)
                self.columns = location_size

    def __resize__(self, new_size: int):
        for row in self.matrix:
            while len(row) < new_size:
                row.append("")
