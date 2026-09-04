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