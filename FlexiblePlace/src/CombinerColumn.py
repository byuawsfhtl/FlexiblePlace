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