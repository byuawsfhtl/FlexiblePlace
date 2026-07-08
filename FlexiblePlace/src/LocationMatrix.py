from FlexiblePlace.src import CompareLocations
from FlexiblePlace.src.LocationComponent import LocationComponent
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
        self.matrix: list[list[LocationComponent]] = []
        
        self.load_places(locations)
    
    def load_places(self, places: list[FlexiblePlace]):
        for row, flexible_place in enumerate(places):
            current_location_components: list[LocationComponent] = [LocationComponent((row,column), component) for column, component in enumerate(flexible_place.get_location_components())]
            self.matrix.append(current_location_components)
            location_size: int = len(current_location_components)
            if location_size > self.column_count:
                self._resize(location_size)
                self.column_count = location_size
            self.row_count: int = len(self.matrix)

    def _resize(self, new_size: int):
        for i, row in enumerate(self.matrix):
            while len(row) < new_size:
                row.append(LocationComponent((i,len(row))))

    # def _link(self, component_a: LocationComponent, component_b: LocationComponent):
        # if _illegal_move(component_a, component_b): # Not finished
            # return
        # closest_component: LocationComponent = _get_closest(component_a, component_b)
        # distance: int = abs(component_a.column - component_b.column)
        # move(closest_component, distance)
        # component_a.link(component_b)
    
    # def _illegal_move(self, component_a: LocationComponent, component_b: LocationComponent) -> bool:
        # if not component_a or not component_b:
            # return True
        ## if there is a link in the way return True else return False

    # def _get_closest(self, component_a: LocationComponent, component_b: LocationComponent):
        # if component_a.column < component_b.column:
            # return component_a
        # else:
            # return component_b
        
    # def _move(self, component: LocationComponent, distance: int):
        # for i in range(distance):
            # shift_right(component)
    
    # def _shift_right(self, component: LocationComponent)
        # current_column: int = component.column
        # if current_column == (self.column_count - 1):
            # self._resize(column_count + 1)
            # self._shift_right(component)
        # elif not component:
            # return
        # else:
            # row: int = component.row
            # column: int = component.column
            # self.matrix[row][column] = LocationComponent(([row][column]))
            # component.column += 1
            # column += 1
            # _shift_right(self.matrix[row][column])
            # self.matrix[row][column] = component
            # for linked_component in components.links:
                # distance: int = abs(component.column - linked_component.column)
                # self._move(linked_component, distance)

def align(location_matrix: LocationMatrix):
    for row in range(len(location_matrix.matrix)):
        while (True):
            match: tuple[tuple[int, int], tuple[int, int]] = _find_best_match(location_matrix, row)
            if not match:
                break
            component_a: LocationComponent = location_matrix.matrix[match[0][0]][match[0][1]]
            component_b: LocationComponent = location_matrix.matrix[match[1][0]][match[1][1]]
            # _link(location_matrix, row, column, matched_component)

def _find_best_match(location_matrix: LocationMatrix, row: int) -> tuple[tuple[int, int], tuple[int, int]]:
    best_score: float = 80.0    # This (80) is the threshold for a match
    best_match: tuple[tuple[int, int], tuple[int, int]] | tuple = ()
    for column in range(len(location_matrix.matrix[row])):
        for i in range(row):
            for j in range(location_matrix.column_count):
                component_a: LocationComponent = location_matrix.matrix[row][column]
                component_b: LocationComponent = location_matrix.matrix[i][j]
                score: float = CompareLocations.basic_comparison_algorithm(component_a, component_b)
                if score > best_score:
                    best_score = score
                    best_match = ((row,column), (i, j))
    return best_match

    