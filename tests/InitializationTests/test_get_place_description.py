import pytest

from FlexiblePlace.src.FlexiblePlace import FlexiblePlace
from unittest.mock import AsyncMock, patch
from tests.testdata.fs_api_mocker import fs_api_mocker

class TestGetPlaceDescription:
    """Tests for FlexiblePlace.place_description accuracy when initialized online."""

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
    async def test_country_by_itself(self):
        """'Venezuela' should resolve to '152'."""
        flexible_place = await FlexiblePlace.online("Venezuela")

        assert flexible_place.place_description == "152"

    @pytest.mark.asyncio
    async def test_city_county_state_country(self):
        """'Eagle, Ada, Idaho, United States' should resolve to '4000719'."""
        flexible_place = await FlexiblePlace.online("Eagle, Ada, Idaho, United States")

        assert flexible_place.place_description == "4000719"

    @pytest.mark.asyncio
    async def test_preset_place_description(self):
        """'La Pastora, Libertador, Distrito Capital, Venezuela' should resolve to '2107883', if already set to that value"""
        flexible_place = await FlexiblePlace.online("La Pastora, Libertador, Distrito Capital, Venezuela", "2107883")

        assert flexible_place.place_description == "2107883"

    @pytest.mark.asyncio
    async def test_different_specificity_can_map_to_same_location(self):
        """'Mérida, Libertador, Mérida, Venezuela' and 'Mérida, Mérida, Venezuela' should resolve to '2101109'."""
        more_specific_flexible_place = await FlexiblePlace.online("Mérida, Libertador, Mérida, Venezuela")
        less_specific_flexible_place = await FlexiblePlace.online("Mérida, Mérida, Venezuela")

        assert more_specific_flexible_place.place_description == less_specific_flexible_place.place_description
        assert more_specific_flexible_place.place_description == "2101109"

    @pytest.mark.asyncio
    async def test_place_matches_with_different_named_place(self):
        """'Moses Lake, Washington, United States' should resolve to '5197325' which is labeled as 'Moses Lake, Grant, Washington, United States'."""
        flexible_place = await FlexiblePlace.online("Moses Lake, Washington, United States")

        assert flexible_place.place_description == "5197325"

    @pytest.mark.asyncio
    async def test_null_input(self):
        """Empty string should be handled gracefully."""
        flexible_place = await FlexiblePlace.online("")

        assert flexible_place.place_description == ""

    @pytest.mark.asyncio
    async def test_whitespace_only(self):
        """String with only whitespace should be handled gracefully."""
        flexible_place = await FlexiblePlace.online("   ")

        assert flexible_place.place_description == ""

    @pytest.mark.asyncio
    async def test_place_with_leading_trailing_spaces(self):
        """Place name with leading and trailing spaces should resolve correctly."""
        flexible_place = await FlexiblePlace.online("  Venezuela  ")

        assert flexible_place.place_description == "152"

    @pytest.mark.asyncio
    async def test_string_with_numbers(self):
        """Place name with numbers 'Encino 75, Texas, United States' should be handled correctly."""
        flexible_place = await FlexiblePlace.online("Encino 75, Texas, United States")

        assert flexible_place.place_description == "5177603"

    @pytest.mark.asyncio
    async def test_string_with_apostrophe(self):
        """Place name with apostrophe 'Saint John's, Newfoundland, Canada' should resolve correctly."""
        flexible_place = await FlexiblePlace.online("Saint John's, Newfoundland, Canada")

        assert flexible_place.place_description == "2241580"

    @pytest.mark.asyncio
    async def test_string_with_hyphens(self):
        """Place name with hyphens 'Winston-Salem, North Carolina, United States' should resolve correctly."""
        flexible_place = await FlexiblePlace.online("Winston-Salem, North Carolina, United States")

        assert flexible_place.place_description == "4757877"

    @pytest.mark.asyncio
    async def test_fake_place(self):
        """Non-existent place 'Fakeville, Nonexistent, Country' should not resolve to a valid place_description."""
        flexible_place = await FlexiblePlace.online("Fakeville, Nonexistent, Country")

        assert flexible_place.place_description == ""

    @pytest.mark.asyncio
    async def test_garbage_input(self):
        """Bad input 'Wal*? w4lla, W^5#1N70N, un1t3d $t@te$' should not resolve to a valid place_description."""
        flexible_place = await FlexiblePlace.online("Wal*? w4lla, W^5#1N70N, un1t3d $t@te$")

        assert flexible_place.place_description == ""
