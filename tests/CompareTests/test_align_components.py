from FlexiblePlace.src.Compare import Compare

class TestAlignComponents:
    def test_get_locations(self) -> None:
        """Tests that the get_locations method works"""
        place_a = ["washington", "united states"]
        place_b = ["walla walla", "washingon"]
        expected = [
            ["", "washington", "united states"],
            ["walla walla", "washingon", ""]
        ]
        assert Compare.align_components(place_a, place_b) == expected