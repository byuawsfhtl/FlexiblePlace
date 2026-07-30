import pytest
from FlexiblePlace.src.FlexiblePlace import FlexiblePlace, compare_places


class TestCompareTwoPlacesCloseMatch:
    """Test for low scoring matches for FlexiblePlace.compare_places static method."""

    def test_different_countries(self) -> None:
        """Different countries (but otherwise agreeing info) should return 80 or higher."""
        place1 = FlexiblePlace("Richmond, Victoria, Australia")
        place2 = FlexiblePlace("Richmond, Victoria, Canada")
        result = compare_places(place1, place2)
        assert result >= 80

    def test_major_misspelled(self) -> None:
        """Same place but with major misspelled components should return 80 or higher."""
        place1 = FlexiblePlace("Walla Walla, Washington, United States")
        place2 = FlexiblePlace("Wahla Wahla, Worshingn, Yuneyded Stayts")
        result = compare_places(place1, place2)
        assert result >= 80    

    def test_minor_misspelled(self) -> None:
        """Same place but with minor misspelled components should return 90 or higher."""
        place1 = FlexiblePlace("Walla Walla, Washington, United States")
        place2 = FlexiblePlace("Wala Wala, Washingon, United Sates")
        result = compare_places(place1, place2)
        assert result >= 90
