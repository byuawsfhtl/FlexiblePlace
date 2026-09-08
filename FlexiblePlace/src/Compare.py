from rapidfuzz import fuzz
from functools import cache
from FlexiblePlace.src.location_matrix import LocationMatrix

class Compare:
    """Provides component-level string comparison and alignment utilities for location comparison.

    Helper class containing methods to align location component lists, calculate component
    similarity scores, and adjust comparison scores based on component specificity.
    """
    @staticmethod
    def align_components(location_a: list[str], location_b: list[str]) -> list[list[str]]:
        """Aligns two lists of strings representing locations.

        Relies heavily on the built-in component alignment functionality of the LocationMatrix class.

        Args:
            location_a (list[str]): First list of location component strings.
            location_b (list[str]): Second list of location component strings.

        Returns:
            list[list[str]]: A list containing the two aligned location component lists."""
        location_matrix = LocationMatrix([location_a, location_b])
        return location_matrix.get_locations()

    @staticmethod
    def compare_each_component(locations: list[list[str]]) -> list[float]:
        """Compares corresponding components of two aligned location lists.

        Args:
            locations (list[list[str]]): A list containing two equal-length location component lists.
        
        Returns:
            list[float]: Fuzzy similarity scores (0.0 to 100.0) for each aligned component pair."""
        location_a: list[str] = locations[0]
        location_b: list[str] = locations[1]
        return [Compare._compare_components(component_a, component_b) for component_a, component_b in zip(location_a, location_b)]

    @cache
    @staticmethod
    def _compare_components(component_a: str, component_b: str) -> float:
        """Calculates the fuzzy similarity ratio between two string components.

        Args:
            component_a (str): The first component string.
            component_b (str): The second component string.
        
        Returns:
            float: Similarity score from 0.0 to 100.0. Returns 100.0 if either component is empty."""
        if not component_a or not component_b:
            return 100.0
        return fuzz.ratio(component_a, component_b)

    @staticmethod
    def adjust_scores(scores_list: list[float]) -> None:
        """Adjusts a list of similarity scores in-place based on component specificity.

        Args:
            scores_list (list[float]): List of component fuzzy scores to adjust in-place.

        Returns:
            None."""
        scores_list[:] = [Compare._forgive_small_differences(score, index) for index, score in enumerate(scores_list[::-1])][::-1]  

    @staticmethod
    def _forgive_small_differences(score: float, index: int) -> float:
        """Forgives small differences in the fuzzy score based on the index of the component being compared.
        
        The higher the index (scores are ordered from least to most specificity), the less important the
        component is, and thus the more forgiving the score should be. For example, a difference in the country
        component should be less forgiving than a difference in the city component.
        
        Args:
            score (float): The fuzzy score to forgive.
            index (int): The index of the component being compared.
        Returns:
            float: The new score.
        """
        component_penalty: float = 0.5 # How harshly to penalize differences in components (With 0.5, about 65% of a 
        # difference in street address will be forgiven as opposed to 30% with the state)
        forgiveness_factor: float = (1 - 2 ** -(index * component_penalty)) # As specificity increases, more forgiveness is granted.
        redeemed_points: float = (100 - score) * forgiveness_factor # Redeems a certain percentage of lost points
        return score + redeemed_points