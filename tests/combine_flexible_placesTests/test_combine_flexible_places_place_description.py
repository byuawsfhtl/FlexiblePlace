from FlexiblePlace.src.FlexiblePlace import FlexiblePlace
from unittest.mock import patch
from tests.resources.fs_api_mocker import fs_api_mocker

combine_flexible_places = FlexiblePlace.combine_flexible_places
combine_flexible_places_online = FlexiblePlace.combine_flexible_places_online

class TestPlaceDescriptionOfCombinedPlace:
    def setup_method(self):
        self.patcher = patch('FlexiblePlace.src.get_place_description.requests.get', side_effect=fs_api_mocker)
        self.mock_get = self.patcher.start()

    def teardown_method(self):
        self.patcher.stop()

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

    def test_most_specific_place_description_maintained(self) -> None:
        """If a more specific match doesn't have a place_description, a less specific match with a
        place description will be favored."""
        places = [
            FlexiblePlace("Washington, United States", "CORRECT"),
            FlexiblePlace("Walla Walla"),
            FlexiblePlace("Walla Walla, Washington, United States")
        ]
        result = combine_flexible_places(places)
        assert str(result) == "Walla Walla, Washington, United States"
        assert result.place_description == "CORRECT"

    def test_online_version_adds_place_description(self):
        """If no description is provided, online version will look up the place_description."""
        places = [
            FlexiblePlace("Washington, United States"),
            FlexiblePlace("Walla Walla"),
            FlexiblePlace("Walla Walla, Washington, United States")
        ]
        result = combine_flexible_places_online(places)
        assert str(result) == "Walla Walla, Washington, United States"
        assert result.place_description == "396089"

    def test_online_version_doesnt_replace_place_description(self):
        """If description is provided (and place is specific), online version will not look up the place_description."""
        places = [
            FlexiblePlace("Washington, United States"),
            FlexiblePlace("Walla Walla"),
            FlexiblePlace("Walla Walla, Washington, United States", "CORRECT")
        ]
        result = combine_flexible_places_online(places)
        assert str(result) == "Walla Walla, Washington, United States"
        assert result.place_description == "CORRECT"

    def test_online_version_unspecific_place_description(self):
        """If description is provided and location is not specific, online version will look up the place_description."""
        places = [
            FlexiblePlace("Washington, United States", "incorrect"),
            FlexiblePlace("Walla Walla"),
            FlexiblePlace("Walla Walla, Washington, United States")
        ]
        result = combine_flexible_places_online(places)
        assert str(result) == "Walla Walla, Washington, United States"
        assert result.place_description == "396089"
