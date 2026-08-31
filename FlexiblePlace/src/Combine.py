from FlexiblePlace.src.LocationMatrix import LocationMatrix

class Combine:
    @staticmethod
    def align_components(locations: list[list[str]]) -> list[list[str]]:
        """Aligns two lists of strings representing locations.

        Relies heavily on the built-in component alignment functionality of the LocationMatrix class.

        Args:
            location_a (list[str]): First list of location component strings.
            location_b (list[str]): Second list of location component strings.

        Returns:
            list[list[str]]: A list containing the two aligned location component lists."""
        location_matrix = LocationMatrix(locations)
        return location_matrix.get_locations()

    @staticmethod
    def isNotFilled(combined_location: list[str]) -> bool:
        return "" in combined_location

    