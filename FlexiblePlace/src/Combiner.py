from FlexiblePlace.src.Aligner import Aligner
from FlexiblePlace.src.CombinerColumn import CombinerColumn

class Combiner:
    """Combines aligned location components into complete locations."""

    def __init__(self, locations: list[list[str]]) -> None:
        """Initialize a Combiner from location component lists.

        These location components are stored most specific to least specific 
        (e.g. [["Walla Walla", "Washington", "United States"]])

        Args:
            locations (list[list[str]]): The location component lists to align and combine.
        """
        aligner: Aligner = Aligner(locations)
        aligned_locations: list[list[str]] = aligner.get_locations()
        component_matches: list[list[set[int]]] = aligner.get_links()
        self.columns: list[CombinerColumn] = [CombinerColumn() for _ in range(aligner.column_count)] 
        self._load_columns(aligned_locations, component_matches)

    def _load_columns(self, aligned_locations: list[list[str]], component_matches: list[list[set[int]]]) -> None:
        """Load aligned components and their match groups into columns.

        Args:
            aligned_locations (list[list[str]]): The aligned location components.
            component_matches (list[list[set[int]]]): The row matches for each component.
        """
        for row in range(len(aligned_locations)):
            for column in range(len(self.columns)):
                component: str = aligned_locations[row][column]
                match_group: set[int] = component_matches[row][column]
                combiner_column: CombinerColumn = self.columns[column]
                combiner_column.add_component(component)
                combiner_column.add_match_group(match_group)

    def get_column_count(self) -> int:
        """Return the number of component columns.

        Returns:
            int: The number of columns in the combiner.
        """
        return len(self.columns)

    def get_row_count(self) -> int:
        """Return the number of unremoved rows.

        Returns:
            int: The number of unremoved rows represented by the first column.
        """
        first_column: CombinerColumn = self.columns[0]
        return len(first_column.empty_indices) + sum(len(match_group) for match_group in first_column.match_groups)

    def remove_outliers(self) -> None:
        """Remove rows with match groups smaller than the largest group in each column."""
        for column in self.columns[::-1]:
            max_match_count: int = max((len(match_group) for match_group in column.match_groups), default=0)
            for match_group in column.match_groups.copy():
                if len(match_group) < max_match_count:
                    self._remove_rows(match_group.copy())

    def _remove_rows(self, match_group: set[int]) -> None:
        """Remove a set of rows from every component column.

        Uses the remove_match_group method of each column to remove a set of 
        rows from each column.

        Args:
            match_group (set[int]): The row indices to remove.
        """
        for column in self.columns:
            column.remove_match_group(match_group)

    def remove_least_precise(self) -> None:
        """Remove the highest-indexed partial row from the least precise column.
        
        In the case that "New York, New York, '' " and " '', New York, United States" are in the Combiner, 
        "New York, New York, '' " would be removed because it is the least precise of the two."""
        for column in self.columns[::-1]:
            if column.match_groups and column.empty_indices:
                partial_row: int = max(column.empty_indices)
                self._remove_rows({partial_row})
                break

    def remove_smallest_component(self) -> None:
        """Remove the row containing the smallest component."""
        for column in self.columns[::-1]:
            smallest_component_row: int | None = column.smallest_component()
            if smallest_component_row != None:
                self._remove_rows({smallest_component_row})
                return

    def remove_last(self) -> None:
        """Remove the last possible row from the combiner."""
        if self.is_empty():
            return
        column: CombinerColumn = self.columns[0]
        possible_rows: list[int] = column.get_possible_rows()
        last_row: int = max(possible_rows)
        self._remove_rows({last_row})

    def is_empty(self) -> bool:
        """Return whether the combiner has no remaining possible rows.

        Returns:
            bool: True when no match groups or empty indices remain; otherwise False.
        """
        first_column: CombinerColumn = self.columns[0]
        return not first_column.match_groups and not first_column.empty_indices

    def fill_in(self, combined_place: list[str]) -> bool:
        """Fill empty location components with the consensus from each column.

        The 'column consensus' refers to the longest string in the column, given that
        each item in the column has been determined to be the same. For example if a column
        column contained `["Washington", "Washington State", "Worshington"]` then the column
        consensus would be `"Washington State"`. However, in a situation where there are outliers,
        no consensus indices will be returned.

        Args:
            combined_place (list[str]): The location components to complete in place.
        Returns:
            bool: True if at least one component was filled; otherwise False.
        """
        has_changed: bool = False
        for index, column in enumerate(self.columns):
            consensus: str = column.column_consensus()
            if consensus and not combined_place[index]:
                combined_place[index] = consensus
                has_changed = True
        return has_changed
                
    @staticmethod
    def is_not_filled(combined_location: list[str]) -> bool:
        """Return whether a combined location contains an empty component.

        Args:
            combined_location (list[str]): The location components to inspect.
        Returns:
            bool: True if any component is empty; otherwise False.
        """
        return "" in combined_location

    @staticmethod
    def resize(combined_location: list[str]) -> None:
        """Remove empty components from a combined location in place.

        Args:
            combined_location (list[str]): The location components to resize.
        """
        combined_location[:] = [component for component in combined_location if component]
