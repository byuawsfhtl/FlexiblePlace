from FlexiblePlace.src import compare_location_components
from FlexiblePlace.src.location_component import LocationComponent

class LocationMatrix:
    """A class that represents a matrix of locations, where each row corresponds to the string array of a 
    FlexiblePlace object and each column corresponds to a location component (e.g. city, county state/province, 
    country). This class is used to align locations for comparison, ensuring that each component is compared
    with the correct component in other locations. Rows are ordered by length.
    
    Example:
    locations = [FlexiblePlace("Washington, United States").get_location_components,
                 FlexiblePlace("Walla Walla, Washingon").get_location_components,
                 FlexiblePlace("Walla Walla, Washingon, United States").get_location_components]
        location_matrix = LocationMatrix(locations)
        print(location_matrix)
        # | united states | washington | walla walla |
        # | united states | washington |             |
        # |               | washington | walla walla |
    """

    def __init__(self, locations: list[list[str]]) -> None:
        """Initializes a LocationMatrix from a list of location component lists.
        
        Creates a matrix structure where each row represents a location and automatically aligns
        components across rows based on similarity matching.
        
        Args:
            locations (list[list[str]]): A list of location component lists, where each inner list represents 
                the components of a single location. Defaults to an empty list.
        Returns:
            None.
        """
        self.row_count: int = 0
        self.column_count: int = 0
        self.matrix: list[list[LocationComponent]] = []        
        self.load_places(sorted(locations, key=len, reverse=True))
        self.align()

    def __bool__(self) -> bool:
        """If the matrix is empty, returns False. Otherwise, returns True.
        
        Returns:
            bool"""
        return bool(self.matrix)
    
    def __str__(self) -> str:
        """Returns a formatted string representation of the LocationMatrix.
        
        Renders the matrix as a pipe-separated table with columns aligned based on the longest
        value in each column. Empty rows result in an empty string.
        
        Args:
            None
        Returns:
            str: A formatted string representing the matrix as a table, or an empty string if the matrix is empty.
        """
        # If no rows, return an empty string
        if not self.matrix:
            return ""
        # Determine the width for each column based on the longest string in that column
        widths: list[int] = []
        for col in range(self.column_count):
            max_len = 0
            for row in range(len(self.matrix)):
                # Guard against rows shorter than column_count (shouldn't happen after resizing)
                if col < len(self.get_row(row)):
                    val = self.get(row,col).value or ""
                    max_len = max(max_len, len(val))
            widths.append(max_len)
        # Build each row as a pipe-separated string with left-aligned padding
        lines: list[str] = []
        for row in range(len(self.matrix)):
            cells: list[str] = []
            for col in range(self.column_count):
                val = ""
                if col < len(self.get_row(row)):
                    val = self.get(row, col).value or ""
                cells.append(val.ljust(widths[col]))
            line = "| " + " | ".join(cells) + " |"
            lines.append(line)
        return "\n".join(lines)
    
    def get(self, row: int, col: int) -> LocationComponent:
        """Return the LocationComponent at the specified row and column.
        Args:
            row (int): Zero-based row index.
            col (int): Zero-based column index.
        Returns:
            LocationComponent: The LocationComponent instance at the specified location."""
        return self.matrix[row][col]
    
    def get_locations(self) -> list[list[str]]:
        """Return the locations in the matrix as a list of lists of strings.
        
        Returns: 
            list[list[str]]: List of all locations in matrix"""
        return [[component.value for component in row] for row in self.matrix]

    def get_row(self, row: int) -> list[LocationComponent]:
        """Return an entire row of LocationComponent objects.
        Args:
           row (int): Zero-based row index.
        Returns:
            list[LocationComponent]: The list of LocationComponent objects representing the row."""
        return self.matrix[row]

    def get_column(self, column: int) -> list[LocationComponent]:
        """Return a column from the matrix as a list of LocationComponent objects.
        Args:
            column (int): Zero-based column index.
        Returns:
            list[LocationComponent]: The column components in row order."""
        return [row[column] for row in self.matrix]
    
    def insert(self, component: LocationComponent) -> None:
        """Insert or replace a LocationComponent into the internal matrix at its (row, column).
        Args:
            component (LocationComponent): The LocationComponent to insert.
        Returns:
            None."""
        row: int = component.row
        col: int = component.column
        self.matrix[row][col] = component

    def load_places(self, places: list[list[str]]) -> None:
        """Populates the LocationMatrix with location components from a list of place component lists.
        Converts each string component into a LocationComponent object and adds it to the matrix. Automatically
        resizes the matrix to accommodate all components, ensuring all rows have the same number of columns.
        
        Args:
            places (list[list[str]]): A list of place component lists, where each inner list represents
                the components of a single location (e.g., [["123 Main St", "Springfield", "IL", "USA"]]).
        Returns:
            None
        """
        for row, place in enumerate(places):
            current_location_components: list[LocationComponent] = [LocationComponent((row,column), component) for column, component in enumerate(place)]
            self.matrix.append(current_location_components)
            location_size: int = len(current_location_components)
            if location_size > self.column_count:
                self._resize(location_size)
            elif location_size < self.column_count:
                self._resize(self.column_count)
        self.row_count: int = len(self.matrix)

    def _resize(self, new_size: int) -> None:
        """Resizes the LocationMatrix to have the specified number of columns by padding rows with empty
        LocationComponent objects as needed. Updates the column_count to reflect the new size. (Note: cannot
        be used to make matrix smaller than current size).
        
        Args:
            new_size (int): The new number of columns for the matrix.
        Returns:
            None."""
        for i, row in enumerate(self.matrix):
            while len(row) < new_size:
                row.append(LocationComponent((i,len(row))))
        self.column_count: int = new_size

    def align(self) -> None:
        """Aligns all rows in a LocationMatrix by finding best matches between components across rows and linking
        them together. Processes each row sequentially, comparing each unlinked component with components in previous
        rows to find optimal alignments based on similarity scores.
        
        Returns:
            None."""
        for row in range(1, len(self.matrix)):
            while (True):
                match: tuple[tuple[int, int], tuple[int, int]] = self._find_best_match(row)
                if not match:
                    break
                row_a: int = match[0][0]
                col_a: int = match[0][1]
                component_a: LocationComponent = self.get(row_a, col_a)
                row_b: int = match[1][0]
                col_b: int = match[1][1]
                component_b: LocationComponent = self.get(row_b, col_b)
                self.link(component_a, component_b)

    def _find_best_match(self, row: int) -> tuple[tuple[int, int], tuple[int, int]]:
        """Finds the best matching pair of LocationComponents between the specified row and all previous rows in
        the matrix. Compares each unlinked component in the row with all components in previous rows, returning the
        pair with the highest similarity score above a threshold of 80.0. Returns an empty tuple if no match is found.
    
        Args:
            row (int): The row index to find matches for.
        Returns:
            tuple[tuple[int, int], tuple[int, int]]: A tuple of two coordinate tuples ((row, col), (row, col)) 
                representing the best matching components, or an empty tuple if no match above threshold is found.
        """
        best_score: float = 80.0    # This (80) is the threshold for a match
        best_match: tuple[tuple[int, int], tuple[int, int]] | tuple = ()
        for column in range(len(self.get_row(row))):
            component_a: LocationComponent = self.get(row, column)
            if component_a.links:
                continue
            best_score, best_match = self._compare_with_previous(component_a, best_score, best_match)
        return best_match
    
    def _compare_with_previous(self, component_a: LocationComponent, best_score: float, best_match: tuple[tuple[int, int], tuple[int, int]]) -> tuple[float, tuple[tuple[int, int], tuple[int, int]]]:
        """Compares the current component with all components in previous rows. If it is a better match then 
        the previous best, best_match and best_score are updated.
        
        Args:
            component_a (LocationComponent): Current component being compared
            best_score (float): Current best score
            best_match (tuple[tuple[int, int], tuple[int, int]] | tuple): Current best match

        Returns:
            best_score (float): Current best score found 
            best_match (tuple[tuple[int, int], tuple[int, int]]): A tuple of two coordinate tuples ((row, col), (row, col)) 
                representing the best matching components, or an empty tuple if no match above threshold is found.
        """
        row: int = component_a.row
        column: int = component_a.column
        for i in range(row):
            for j in range(self.column_count):
                component_b: LocationComponent = self.get(i,j)
                score: float = compare_location_components.basic_comparison_algorithm(component_a, component_b)
                if score > best_score:
                    best_score = score
                    best_match = ((row,column), (i, j))
        return best_score, best_match

    def link(self, component_a: LocationComponent, component_b: LocationComponent) -> None:
        """Links two LocationComponents together by aligning them in the matrix. Moves the closer component
        to match the column of the farther component, and creates a link between them if the move is legal.
        Once the components are linked, an attempt to move one of them will the other to move with it.
        Example:
            print(location_matrix) # Note: the link is marked below with a '%', but will not be in a real print
            # |% washington  %|             |             |
            # |% washington  %| walla walla |             |
            # | united states | washington  | walla walla |
            component_a: LocationComponent = location_matrix.get(2,1) # 'washington' in last row
            component_b: LocationComponent = location_matrix.get(1,0) # 'washington' in 2nd row
            location_matrix.link(component_a, component_b)
            print(location_matrix) # Note: the link is marked below with a '%', but will not be in a real print
            # |               |% washington %|             |
            # |               |% washington %| walla walla |
            # | united states |% washington %| walla walla |.

        Args:
            component_a (LocationComponent): The first component to link.
            component_b (LocationComponent): The second component to link.
        Returns:
            None."""
        closest_component, farthest_component = self._order_components(component_a, component_b)
        if self._illegal_move(closest_component, farthest_component):
            component_a.link(component_a)
            return
        distance: int = farthest_component.column - closest_component.column
        self._move(closest_component, distance)
        component_a.link(component_b)
    
    def _order_components(self, component_a: LocationComponent, component_b: LocationComponent) -> tuple[LocationComponent, LocationComponent]:
        """Orders two LocationComponents by their column position, returning the component with the lower column
        first and the component with the higher column second.
        
        Args:
            component_a (LocationComponent): The first component.
            component_b (LocationComponent): The second component.
        Returns:
            tuple[LocationComponent, LocationComponent]: A tuple of (closest_to_start, farthest_from_start)."""
        if component_a.column < component_b.column:
            return component_a, component_b
        else:
            return component_b, component_a
    
    def _illegal_move(self, component_a: LocationComponent, component_b: LocationComponent) -> bool:
        """Checks for an illegal move. A move is illegal if the components being linked together are empty, or if
        other links in between the components that are being aligned make it impossible to align them.
        Args:
            component_a (LocationComponent): component closest to the beginning of the row and will be moved
            component_b (LocationComponent): component farthest from the beginning of the row and will not move
        Returns:
            True if the move is illegal, otherwise False."""
        if not component_a or not component_b:
            return True
        for i in range(component_a.column, component_b.column + 1):
            component_to_check: LocationComponent = self.get(component_a.row,i)
            if component_to_check.links and any(component.row == component_b.row for component in component_to_check.links):
                return True
        return False
    
    def _move(self, component: LocationComponent, distance: int) -> None:
        """Moves a LocationComponent to the right by the specified distance by repeatedly shifting it one column
        at a time, resizing the matrix if necessary.
        
        Args:
            component (LocationComponent): The component to move.
            distance (int): The number of columns to move the component to the right.
        Returns:
            None."""
        for i in range(distance):
            self._shift_right(component)
    
    def _shift_right(self, component: LocationComponent) -> None:
        """Shifts a LocationComponent one column to the right in the matrix, resizing the matrix if the component
        is at the end. Also recursively shifts all subsequent components in the row and updates linked components.
        
        Args:
            component (LocationComponent): The component to shift right.
        Returns:
            None."""
        current_column: int = component.column
        if not component:
            return
        elif current_column == (self.column_count - 1):
            self._resize(self.column_count + 1)
            self._shift_right(component)
        else:
            row: int = component.row
            column: int = component.column
            self.insert(LocationComponent((row,column)))
            component.column += 1
            column += 1
            self._shift_right(self.get(row,column))
            self.insert(component)
            for linked_component in component.links:
                distance: int = abs(component.column - linked_component.column)
                self._move(linked_component, distance)

    def remove_outliers(self, column: int) -> None:
        """Remove rows that are outliers for the specified column.

        Determines the maximum number of links for any component in the specified column,
        treats components with fewer links as outliers, and removes their rows from the matrix.
        This helps to prune rows that do not share consensus with the plurality in that column.

        Args:
            column (int): Zero-based column index to inspect for outliers.
        Returns:
            None"""
        if not self:
            return
        components_in_column: list[LocationComponent] = self.get_column(column)
        max_count: int = max(len(component.links) for component in components_in_column)
        rows_to_remove: list[int] = [component.row for component in components_in_column if component and len(component.links) < max_count]
        self._remove_rows(rows_to_remove)

    def _remove_rows(self, rows: list[int]) -> None:
        """Remove multiple rows by index from the matrix.
        Args:
            rows (list[int]): A list of zero-based row indices to remove.
        Returns:
            None."""
        for row in sorted(rows, reverse=True):
            self._remove_row(row)

    def _remove_row(self, row: int) -> None:
        """Remove a single row from the matrix.
        Args:
            row (int): Zero-based index of the row to remove.
        Returns:
            None."""
        for component in self.matrix.pop(row):
            component.links.discard(component)
        self.row_count -= 1
        for r in self.matrix[row:]:
            for component in r:
                component.row -= 1

    def column_consensus(self, column: int) -> str:
        """Return a consensus string for a given column if all non-empty components agree (or are linked).
        Args:
            column (int): Zero-based column index to compute consensus for.
        Returns:
            str: The consensus component string (the longest matching component's value) if consensus is found,
                otherwise an empty string."""
        components_in_column: list[LocationComponent] = [component for component in self.get_column(column) if component]
        if not all(component is components_in_column[0] or component in components_in_column[0].links
                   for component in components_in_column):
            return ""
        return max((component.value for component in components_in_column), key=len, default="")
    
    def remove_least_accurate_row(self) -> bool:
        """Remove the first row that lacks a component where other rows have one (i.e., the least accurate row).
        Args:
            None
        Returns:
            bool: True if a row was removed, False if no candidate row was found."""
        for column in range(self.column_count):
            if not any(component for component in self.get_column(column)):
                continue
            for row in range(self.row_count):
                if not self.get(row, column):
                    self._remove_row(row)
                    return True
        return False
    
    def remove_row_with_smallest_component(self) -> bool:
        """Remove a row that contains the uniquely smallest component (by string length) in any column.
        Args:
            None
        Returns:
            bool: True if a row was removed, False otherwise."""
        for column in range(self.column_count):
            column_components = self.get_column(column)
            min_len = len(min(column_components, key=lambda component: len(component.value)).value)
            min_indeces = [comp.row for comp in column_components if len(comp.value) == min_len]
            if len(min_indeces) == 1:
                self._remove_row(min_indeces[0])
                return True
        return False
    
    def remove_last_row(self) -> None:
        """Remove the last row in the matrix.
        Args:
            None.
        Returns:
            None."""
        self._remove_row(self.row_count - 1)