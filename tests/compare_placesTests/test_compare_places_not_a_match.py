import unittest
from FlexiblePlace.src.FlexiblePlace import FlexiblePlace, compare_places


class TestCompareTwoPlacesNotAMatch(unittest.TestCase):
    """Test for low scoring matches for FlexiblePlace.compare_places static method."""

    def test_dont_match_different_components(self) -> None:
        """
        Different components should not return 100
        ("Paris, Texas", "Paris, France" does not return 100).
        """
        place1 = FlexiblePlace("Paris, Texas")
        place2 = FlexiblePlace("Paris, France")
        result = compare_places(place1, place2)
        self.assertLess(result, 30)


if __name__ == "__main__":
    unittest.main()
