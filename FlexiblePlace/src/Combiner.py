from FlexiblePlace.src.LocationMatrix import LocationMatrix
from FlexiblePlace.src.CombinerColumn import CombinerColumn

class Combiner:
    def __init__(self, locations: list[list[str]]) -> None:
        location_matrix: LocationMatrix = LocationMatrix(locations)
        aligned_locations: list[list[str]] = location_matrix.get_locations()
        component_matches: list[list[set[int]]] = location_matrix.get_links()
        self.columns: list[CombinerColumn] = [CombinerColumn() for i in range(location_matrix.column_count)] 
        self._load_columns(aligned_locations, component_matches)

    def _load_columns(self, aligned_locations: list[list[str]], component_matches: list[list[set[int]]]) -> None:
        for row in range(len(aligned_locations)):
            for column in range(len(self.columns)):
                component: str = aligned_locations[row][column]
                match_group: set[int] = component_matches[row][column]
                combiner_column: CombinerColumn = self.columns[column]
                combiner_column.add_component(component)
                combiner_column.add_match_group(match_group)

    def remove_outliers(self) -> None:
        for column in self.columns[::-1]:
            max_match_count: int = max((len(match_group) for match_group in column.match_groups), default=0)
            for match_group in column.match_groups:
                if len(match_group) < max_match_count:
                    self._remove_rows(match_group.copy())

    def _remove_rows(self, match_group: set[int]) -> None:
        for column in self.columns:
            column.remove_match_group(match_group)

    def fill_in(self, combined_place: list[str]) -> bool:
        has_changed: bool = False
        for index, column in enumerate(self.columns):
            consensus: str = column.column_consensus()
            if consensus and not combined_place[index]:
                combined_place[index] = consensus
                has_changed = True
        return has_changed
                
    @staticmethod
    def is_not_filled(combined_location: list[str]) -> bool:
        return "" in combined_location