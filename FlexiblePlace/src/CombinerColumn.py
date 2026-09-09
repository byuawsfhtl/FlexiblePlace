class CombinerColumn:
    """Store components and row match groups for one aligned location column."""

    def __init__(self) -> None:
        """Initialize an empty combiner column."""
        self.components: list[str] = []
        self.match_groups: list[set[int]] = []
        self.empty_indeces: set[int] = set()

    def add_component(self, component: str) -> None:
        """Add a component and track its row when the component is empty.

        Args:
            component (str): The location component to add.
        """
        if not component:
            self.empty_indeces.add(len(self.components))
        self.components.append(component)

    def add_match_group(self, match_group: set[int]) -> None:
        """Add a non-empty match group unless it is already present.

        Args:
            match_group (set[int]): The row indices represented by the match group.
        """
        if match_group and match_group not in self.match_groups:
            self.match_groups.append(match_group)

    def remove_match_group(self, match_group_to_remove: set[int]) -> None:
        """Remove row references from this column's match groups.

        Args:
            match_group_to_remove (set[int]): The row references to remove.
        """
        empty_match_groups: list[set[int]] = []
        for row_reference in match_group_to_remove:
            self.empty_indeces.discard(row_reference)
            for match_group in self.match_groups:
                match_group.discard(row_reference)
                if not match_group and match_group not in empty_match_groups:
                    empty_match_groups.append(match_group)
        for match_group in empty_match_groups:
            self.match_groups.remove(match_group)

    def column_consensus(self) -> str:
        """Return the longest component when exactly one match group remains.

        Returns:
            str: The consensus component, or an empty string when no unique group exists.
        """
        if len(self.match_groups) != 1:
            return ""
        return max((self.components[index] for index in self.match_groups[0]), key=len, default="")

    def smallest_component(self) -> int | None:
        """Return the row index of the shortest component in the match groups.

        Returns:
            int | None: The shortest component's row index, or None when all are equal.
        """
        smallest: str = ""
        smallest_index: int | None = None
        if self._all_equal_length():
            return smallest_index
        for match_group in self.match_groups:
            for component_index in match_group:
                component = self.components[component_index]
                if not smallest or len(component) < len(smallest):
                    smallest = component
                    smallest_index = component_index 
        return smallest_index

    def _all_equal_length(self) -> bool:
        """Return whether all components in the match groups have equal lengths.

        Returns:
            bool: True when all grouped components have equal lengths; otherwise False.
        """
        first: str = ""
        for match_group in self.match_groups:
            for component_index in match_group:
                component = self.components[component_index]
                if not first:
                    first = component
                if not len(first) == len(component):
                    return False 
        return True

    def get_possible_rows(self) -> list[int]:
        """Return all row indices represented by groups or empty components.

        Returns:
            list[int]: The possible row indices in this column.
        """
        possible_rows: list[int] = []
        for match_group in self.match_groups:
            possible_rows.extend(match_group)
        possible_rows.extend(self.empty_indeces)
        return possible_rows