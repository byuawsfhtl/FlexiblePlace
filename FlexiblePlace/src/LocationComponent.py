class LocationComponent:
    """Represents a single location component within a LocationMatrix object.
    Stores the location (row and column) and string value of the component."""
    def __init__(self, pair: tuple[int,int], value: str = "") -> None:
        """Initializes a LocationComponent with position and optional value.
        
        Args:
            pair (tuple[int, int]): A tuple of (row, column) coordinates for this component's position in the matrix.
            value (str): The string value of this location component. Defaults to an empty string.
        Returns:
            None.
        """
        self.row: int = pair[0]
        self.column: int = pair[1]
        self.value: str = value
        self.links: set[LocationComponent] | set = set()
    
    def __bool__(self) -> bool:
        """Checks if the LocationComponent has a non-empty value.
        
        Args:
            None
        Returns:
            bool: True if the value is non-empty, False otherwise.
        """
        return bool(self.value)

    def __str__(self) -> str:
        """Returns a string representation of the LocationComponent with its value and coordinates.
        
        Args:
            None
        Returns:
            str: A formatted string containing the value and (row, column) position.
        """
        return f"{self.value} ({self.row}, {self.column})"

    def link(self, other: object) -> None:
        """Creates a bidirectional link between this LocationComponent and another LocationComponent
        All linked components share the same set of links
    
        Args:
            other: The object to link with (typically a LocationComponent).
        Returns:
            None.
    """
        if type(other) == LocationComponent:
            self.links.add(other)
            other.links.add(self)
            merged_set = self.links | other.links
            for component in merged_set:
                component.links = merged_set
        