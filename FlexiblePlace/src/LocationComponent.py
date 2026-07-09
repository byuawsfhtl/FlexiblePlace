class LocationComponent:
    """Represents a single location component within a LocationMatrix object.
    Stores the location (row and column) and string value of the component"""
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
            other.links.add(self)
        