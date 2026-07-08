class LocationComponent:
    def __init__(self, pair: tuple[int,int], value: str = ""):
        self.row: int = pair[0]
        self.column: int = pair[1]
        self.value: str = value
        self.links: set[LocationComponent] | set = set()
    
    def __bool__(self):
        return bool(self.value)

    def link(self, other):
        if type(other) == LocationComponent:
            self.links.add(other)
            other.link(self)
        