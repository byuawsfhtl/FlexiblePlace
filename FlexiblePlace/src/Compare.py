from rapidfuzz import fuzz
from functools import cache
from FlexiblePlace.src.Aligner import Aligner

class Compare:
    """Provides component-level string comparison and alignment utilities for location comparison.

    Helper class containing methods to align location component lists, calculate component
    similarity scores, and adjust comparison scores based on component specificity.
    """
    @staticmethod
    def align_components(location_a: list[str], location_b: list[str]) -> list[list[str]]:
        """Aligns two lists of strings representing locations.

        Relies heavily on the built-in component alignment functionality of the Aligner class.

        Args:
            location_a (list[str]): First list of location component strings.
            location_b (list[str]): Second list of location component strings.

        Returns:
            list[list[str]]: A list containing the two aligned location component lists."""
        aligner = Aligner([location_a, location_b])
        return aligner.get_locations()

    @staticmethod
    def compare_each_component(locations: list[list[str]]) -> list[float]:
        """Compares corresponding components of two aligned location lists.

        A missing component is represented by -1 rather than removed, preserving
        component order and spacing. This sentinel is ignored during score
        adjustment and does not penalize the comparison.

        Args:
            locations (list[list[str]]): A list containing two equal-length location component lists.
        
        Returns:
            list[float]: Similarity scores from 0.0 to 100.0; -1 marks a missing component."""
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
            return -1
        return fuzz.ratio(component_a, component_b)

    @staticmethod
    def adjust_scores(scores_list: list[float]) -> None:
        """Adjusts similarity scores in place based on component specificity.

        The -1 sentinel marks a missing place component. It is retained to
        preserve score order and spacing, and is ignored rather than penalized.

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
        if score == -1:
            return -1
        component_penalty: float = 0.5 # How harshly to penalize differences in components (With 0.5, about 65% of a 
        # difference in street address will be forgiven as opposed to 30% with the state)
        forgiveness_factor: float = (1 - 2 ** -(index * component_penalty)) # As specificity increases, more forgiveness is granted.
        redeemed_points: float = (100 - score) * forgiveness_factor # Redeems a certain percentage of lost points
        return score + redeemed_points

    @staticmethod
    def get_average(scores_list: list[float]) -> float:
        """Calculates the average while ignoring scores for missing components.

        A -1 score marks a missing component and is retained in aligned score
        lists to preserve component order and spacing. It is excluded from the
        average so a missing component does not penalize the comparison.

        Args:
            scores_list: Scores to average; negative scores are ignored.

        Returns:
            The average of the nonnegative scores, or 100.0 if none remain.
        """
        nonnegative_scores: list[float] = [score for score in scores_list if score >= 0]
        score_count = len(nonnegative_scores)
        if score_count == 0:
            return 100.0
        return sum(nonnegative_scores)/score_count