import pytest

from unittest.mock import patch, AsyncMock
from tests.testdata.fs_api_mocker import fs_api_mocker

from pathlib import Path
from pyscripttestutils import PyScriptTestRunner
from FlexiblePlace.src.FlexiblePlace import FlexiblePlace

runner = PyScriptTestRunner(
    Path(__file__).resolve().parents[2] / "FlexiblePlaceTS" / "dist" / "test_bridge.js",
    deserializer=lambda d: FlexiblePlace(d["location"], d.get("placeDescription", ""), auto_fill=False),
)

runner.add_method(FlexiblePlace.__str__, "FlexiblePlace.toString", executor=lambda d: str(d))
runner.add_method(FlexiblePlace.__repr__, "FlexiblePlace.__repr__", executor=lambda d: repr(d))
runner.add_method(FlexiblePlace.__eq__, "FlexiblePlace.__eq__", executor=lambda d: d[0] == d[1])
runner.add_method(FlexiblePlace.__bool__, "FlexiblePlace.__bool__", executor=lambda d: bool(d))
runner.add_method(FlexiblePlace.get_location, "FlexiblePlace.get_location", executor=lambda d: d.get_location())
runner.add_method(FlexiblePlace.compare, "FlexiblePlace.compare", executor=lambda d: d[0].compare(d[1]))
runner.add_method(FlexiblePlace.compare_places, "FlexiblePlace.compare_places", executor=lambda d: FlexiblePlace.compare_places(d[0], d[1]))
runner.add_method(FlexiblePlace.combine_flexible_places, "FlexiblePlace.combine_flexible_places", executor=lambda d: FlexiblePlace.combine_flexible_places(d[0]))


combine_flexible_places = FlexiblePlace.combine_flexible_places
combine_flexible_places_online = FlexiblePlace.combine_flexible_places_online

class TestPlaceDescriptionOfCombinedPlaceOffline:
    """Tests for FlexiblePlace.place_description accuracy when combining multiple FlexiblePlace objects offline."""
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

class TestPlaceDescriptionOfCombinedPlaceOnline:
    """Tests for FlexiblePlace.place_description accuracy when combining multiple FlexiblePlace objects online."""
    @pytest.fixture(autouse=True)
    def patch_httpx_get(self):
        """Automatically mock httpx AsyncClient.get for all tests in this class."""
        with patch(
            'FlexiblePlace.src.get_place_description.httpx.AsyncClient.get',
            new_callable=AsyncMock,
            side_effect=fs_api_mocker
        ):
            yield

    @pytest.mark.asyncio
    async def test_online_version_adds_place_description(self):
        """If no description is provided, online version will look up the place_description."""
        places = [
            FlexiblePlace("Washington, United States"),
            FlexiblePlace("Walla Walla"),
            FlexiblePlace("Walla Walla, Washington, United States")
        ]
        result = await combine_flexible_places_online(places)
        assert str(result) == "Walla Walla, Washington, United States"
        assert result.place_description == "396089"

    @pytest.mark.asyncio
    async def test_online_version_doesnt_replace_place_description(self):
        """If description is provided (and place is specific), online version will not look up the place_description."""
        places = [
            FlexiblePlace("Washington, United States"),
            FlexiblePlace("Walla Walla"),
            FlexiblePlace("Walla Walla, Washington, United States", "CORRECT")
        ]
        result = await combine_flexible_places_online(places)
        assert str(result) == "Walla Walla, Washington, United States"
        assert result.place_description == "CORRECT"

    @pytest.mark.asyncio
    async def test_online_version_unspecific_place_description(self):
        """If description is provided and location is not specific, online version will look up the place_description."""
        places = [
            FlexiblePlace("Washington, United States", "incorrect"),
            FlexiblePlace("Walla Walla"),
            FlexiblePlace("Walla Walla, Washington, United States")
        ]
        result = await combine_flexible_places_online(places)
        assert str(result) == "Walla Walla, Washington, United States"
        assert result.place_description == "396089"
