import pytest
from FlexiblePlace.src.FlexiblePlace import FlexiblePlace, compare_places


class TestCompareTwoPlacesPerfectMatch:
    """Test for perfect matches for FlexiblePlace.compare_places static method."""

    def test_null_returns_100(self) -> None:
        """Null returns 100"""
        place1 = FlexiblePlace("")
        place2 = FlexiblePlace("")
        result = compare_places(place1, place2)
        assert result == 100

    def test_object_compared_with_null_returns_100(self) -> None:
        """Object compared with null returns 100
        ("Paterson, Passaic, New Jersey, United States", "" returns 100)."""
        place1 = FlexiblePlace("Paterson, Passaic, New Jersey, United States")
        place2 = FlexiblePlace("")
        result = compare_places(place1, place2)
        assert result == 100

    def test_same_place_case_insensitive_returns_100(self) -> None:
        """Place comparison should be case-insensitive
        ("belgium", "Belgium" returns 100)."""
        place1 = FlexiblePlace("belgium")
        place2 = FlexiblePlace("Belgium")
        result = compare_places(place1, place2)
        assert result == 100

    def test_specific_compared_with_less_specific_returns_100_new_jersey(self) -> None:
        """Specific compared with less specific returns 100
        ("Camden, New Jersey, United States", "Camden, Camden, New Jersey, United States" returns 100)."""
        place1 = FlexiblePlace("Camden, New Jersey, United States")
        place2 = FlexiblePlace("Camden, Camden, New Jersey, United States")
        result = compare_places(place1, place2)
        assert result == 100

    def test_specific_compared_with_less_specific_returns_100_new_york(self) -> None:
        """Specific compared with less specific returns 100
        ("No Croghan J*, New York, United States", "New York, United States" returns 100)."""
        place1 = FlexiblePlace("No Croghan J*, New York, United States")
        place2 = FlexiblePlace("New York, United States")
        result = compare_places(place1, place2)
        assert result == 100

    def test_whitespace_only_strings(self) -> None:
        """Whitespace-only strings should be treated as null
        ("   ", "   " returns 100)."""
        place1 = FlexiblePlace("   ")
        place2 = FlexiblePlace("   ")
        result = compare_places(place1, place2)
        assert result == 100

    def test_match_misaligned_components(self) -> None:
        """Misaligned components should still be compared correctly
        ("Houston, Texas", "Houston, Harris, Texas, United States" returns 100)."""
        place1 = FlexiblePlace("Houston, Texas")
        place2 = FlexiblePlace("Houston, Harris, Texas, United States")
        result = compare_places(place1, place2)
        assert result == 100
