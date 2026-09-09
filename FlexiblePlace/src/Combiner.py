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

    def get_column_count(self):
        return len(self.columns)

    def get_row_count(self):
        first_column: CombinerColumn = self.columns[0]
        return len(first_column.empty_indeces) + sum(len(match_group) for match_group in first_column.match_groups)

    def remove_outliers(self) -> None:
        for column in self.columns[::-1]:
            max_match_count: int = max((len(match_group) for match_group in column.match_groups), default=0)
            for match_group in column.match_groups.copy():
                if len(match_group) < max_match_count:
                    self._remove_rows(match_group.copy())

    def _remove_rows(self, match_group: set[int]) -> None:
        for column in self.columns:
            column.remove_match_group(match_group)

    def remove_least_precise(self) -> None:
        for column in self.columns[::-1]:
            if column.match_groups and column.empty_indeces:
                partial_row: int = max(column.empty_indeces)
                self._remove_rows({partial_row})
                break

    def remove_smallest_component(self) -> None:
        for column in self.columns[::-1]:
            smallest_component_row: int | None = column.smallest_component()
            if smallest_component_row != None:
                self._remove_rows({smallest_component_row})

    def remove_last(self) -> None:
        if self.is_empty():
            return
        column: CombinerColumn = self.columns[0]
        possible_rows: list[int] = column.get_possible_rows()
        last_row: int = max(possible_rows)
        self._remove_rows({last_row})

    def is_empty(self):
        first_column: CombinerColumn = self.columns[0]
        return not first_column.match_groups and not first_column.empty_indeces

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

    @staticmethod
    def resize(combined_location: list[str]) -> None:
        combined_location[:] = [component for component in combined_location if component]
