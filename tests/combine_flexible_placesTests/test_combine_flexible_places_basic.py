import unittest
from FlexiblePlace.src.FlexiblePlace import FlexiblePlace, combine_flexible_places


class TestCombineFlexiblePlacesBasic(unittest.TestCase):
    """Basic tests for FlexiblePlace.combine_flexible_places static method"""

    def test_null_returns_null(self) -> None:
        """Null returns null."""
        places = []
        result = combine_flexible_places(places)
        self.assertFalse(result)

    def test_single_object_returns_same_object(self) -> None:
        """Single object returns the same object."""
        places = [FlexiblePlace("Belgium")]
        result = combine_flexible_places(places)
        self.assertEqual(str(result), "Belgium")

    def test_duplicate_objects_return_same_object(self) -> None:
        """
        Duplicate objects return same object
        ("Belgium" and "Belgium" returns "Belgium").
        """
        places = [FlexiblePlace("Belgium"), FlexiblePlace("Belgium")]
        result = combine_flexible_places(places)
        self.assertEqual(str(result), "Belgium")

    def test_indecision_yields_longest_string(self) -> None:
        """
        Indecision yields longest string
        ("Paris" and "Belgium" returns "Belgium").
        """
        places = [FlexiblePlace("Paris"), FlexiblePlace("Belgium")]
        result = combine_flexible_places(places)
        self.assertEqual(str(result), "Belgium")

    def test_tie_yields_first(self) -> None:
        """
        Tie in string length yields first
        ("Egypt" and "Japan" returns "Egypt").
        """
        places = [FlexiblePlace("Egypt"), FlexiblePlace("Japan")]
        result = combine_flexible_places(places)
        self.assertEqual(str(result), "Egypt")


if __name__ == "__main__":
    unittest.main()
