from rapidfuzz import fuzz
from functools import cache
from FlexiblePlace.src.LocationMatrix import LocationMatrix

class Compare:
    @staticmethod
    def align_components(location_a: list[str], location_b: list[str]) -> list[list[str]]:
        location_matrix = LocationMatrix([location_a, location_b])
        return location_matrix.get_locations()

    @staticmethod
    def compare_each_component(locations: list[list[str]]) -> list[float]:
        location_a: list[str] = locations[0]
        location_b: list[str] = locations[1]
        return [Compare._compare_components(component_a, component_b) for component_a, component_b in zip(location_a, location_b)]

    @cache
    @staticmethod
    def _compare_components(component_a: str, component_b: str) -> float:
        if not component_a or not component_b:
            return 100.0
        return fuzz.ratio(component_a, component_b)

    @staticmethod
    def adjust_scores(scores_list: list[float]):
        scores_list[:] = [Compare._forgive_small_differences(score, index) for index, score in enumerate(scores_list)]  

    @staticmethod
    def _forgive_small_differences(score: float, index: int) -> float:
        """Forgives small differences in the fuzzy score based on the index of the component being compared.
        The higher the index, the less important the component is, and thus the more forgiving the score should be.
        For example, a difference in the country component should be less forgiving than a difference in the city 
        component.
        
        Args:
            fuzzy_score (float): The fuzzy score to forgive.
            index (int): The index of the component being compared.
        Returns:
            float: The new score.
        """
        component_penalty: float = 0.5 # How harshly to penalize differences in components (With 0.5, about 65% of a 
        # difference in street address will be forgiven as opposed to 30% with the state)
        forgiveness_factor: float = (1 - 2 ** -(index * component_penalty)) # As index increases, more forgiveness is granted.
        redeemed_points: float = (100 - score) * forgiveness_factor # Redeems a certain percentage of lost points
        return score + redeemed_points