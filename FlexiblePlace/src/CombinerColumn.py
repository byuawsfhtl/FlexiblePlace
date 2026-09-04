class CombinerColumn:
    def __init__(self) -> None:
        self.components: list[str] = []
        self.match_groups: list[set[int]] = []
        self.empty_indeces: set[int] = set()

    def add_component(self, component: str) -> None:
        if not component:
            self.empty_indeces.add(len(self.components))
        self.components.append(component)

    def add_match_group(self, match_group: set[int]):
        if match_group and match_group not in self.match_groups:
            self.match_groups.append(match_group)

    def remove_match_group(self, match_group_to_remove: set[int]) -> None:
        empty_match_groups: list[set[int]] = []
        for row_reference in match_group_to_remove:
            self.empty_indeces.discard(row_reference)
            for match_group in self.match_groups:
                match_group.discard(row_reference)
                if not match_group:
                    empty_match_groups.append(match_group)
        for match_group in empty_match_groups:
            self.match_groups.remove(match_group)

    def column_consensus(self) -> str:
        if len(self.match_groups) != 1:
            return ""
        return max((self.components[index] for index in self.match_groups[0]), key=len, default="")

    def smallest_component(self) -> int | None:
        smallest: str = ""
        smallest_index: int | None = None
        for match_group in self.match_groups:
            for component_index in match_group:
                component = self.components[component_index]
                if not smallest:
                    smallest = component
                if len(component) < len(smallest):
                    smallest = component
                    smallest_index = component_index 
        return smallest_index

    def get_possible_rows(self):
        possible_rows: list[int] = []
        for match_group in self.match_groups:
            possible_rows.extend(match_group)
        possible_rows.extend(self.empty_indeces)
        return possible_rows