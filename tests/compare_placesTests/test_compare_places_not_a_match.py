from FlexiblePlace.src.FlexiblePlace import FlexiblePlace

compare_places = FlexiblePlace.compare_places

class TestCompareTwoPlacesNotAMatch:
    """Test for low scoring matches for FlexiblePlace.compare_places static method."""

    def test_completely_different(self) -> None:
        """Completely different locations should return a score lower than 40"""
        place1 = FlexiblePlace("Walla Walla, Washington, United States")
        place2 = FlexiblePlace("Paris, Île-de-France, France")
        result = compare_places(place1, place2)
        assert result > 30
        assert result < 40

    def test_only_city_matches(self) -> None:
        """Different locations but same state name should return a score lower than 60"""
        place1 = FlexiblePlace("Paris, Île-de-France, France")
        place2 = FlexiblePlace("Paris, Texas, United States")
        result = compare_places(place1, place2)
        assert result > 50
        assert result < 60

    def test_only_state_matches(self) -> None:
        """Different locations but same state name should return a score lower than 70"""
        place1 = FlexiblePlace("Manus, Amazonas, Brazil")
        place2 = FlexiblePlace("Leticia, Amazonas, Colombia")
        result = compare_places(place1, place2)
        assert result > 60
        assert result < 70

    def test_only_country_matches(self) -> None:
        """Different locations but same country should return a score lower than 70"""
        place1 = FlexiblePlace("Walla Walla, Washington, United States")
        place2 = FlexiblePlace("Provo, Utah, United States")
        result = compare_places(place1, place2)
        assert result > 60
        assert result < 70

    def test_different_specificity(self) -> None:
        """Different locations of different specificity levels should return a score lower than 75"""
        place1 = FlexiblePlace("Walla Walla, Washington, United States")
        place2 = FlexiblePlace("Belgium")
        result = compare_places(place1, place2)
        assert result > 65
        assert result < 75
