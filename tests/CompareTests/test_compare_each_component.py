from FlexiblePlace.src.Compare import Compare
from rapidfuzz import fuzz

class TestCompareEachComponent:
    def test_compare_each_location(self) -> None:
        """Tests that this method outputs the same float as the fuzzy string comparison"""
        place_a = ["walla walla", "washington", "united states"]
        place_b = ["walla walla", "wrongstate", "usa"]
        expected = [fuzz.ratio(place_a[i],place_b[i]) for i in range(len(place_a))]
        assert Compare.compare_each_component([place_a, place_b]) == expected