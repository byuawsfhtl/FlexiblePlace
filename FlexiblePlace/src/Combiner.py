from FlexiblePlace.src.LocationMatrix import LocationMatrix

class Combiner:
    def __init__(self, locations: list[list[str]]) -> None:
        location_matrix: LocationMatrix = LocationMatrix(locations)
        # aligned_locations: list[list[str]] = location_matrix.get_locations()
        # component_matches: list[list[set[int]]] = location_matrix.get_links()
        # self.columns: list[CombinerColumn] = [CombinerColumn() for i in location_matrix.column_count] 
        # self.load_columns(aligned_locations, component_matches)
        return
    
    # def load_columns(self, aligned_locations: list[list[str]], component_matches list[set[int]]) -> None:
        for row in range(len(aligned_locations)):
            for column in range(len(self.columns)):
                component: str = aligned_locations[row][column]
                match_group: set[int] = component_matches[row][column]
                combiner_column: CombinerColumn = self.columns[column]
                combiner_column.add_component(component)
                combiner_column.add_match_group(match_group)

    @staticmethod
    def is_not_filled(combined_location: list[str]) -> bool:
        return "" in combined_location