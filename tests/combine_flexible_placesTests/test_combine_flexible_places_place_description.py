from FlexiblePlace.src.FlexiblePlace import FlexiblePlace

combine_flexible_places = FlexiblePlace.combine_flexible_places

class TestPlaceDescriptionOfCombinedPlace:
    def test_place_description_maintained(self) -> None:
        """The place_description should be saved if combined place closely matches a previous one."""
        places = [
            FlexiblePlace("Washington, United States", "incorrect place description"),
            FlexiblePlace("Walla Walla", "also incorrect"),
            FlexiblePlace("Walla Walla, Washington, United States", "CORRECT")
        ]
        result = combine_flexible_places(places)
        assert str(result) == "Walla Walla, Washington, United States"
        assert result.place_description == "CORRECT"

    