from FlexiblePlace.src.FlexiblePlace import FlexiblePlace


class TestGetPlaceDescription:
    """Tests for FlexiblePlace.place_description accuracy when initialized online."""

    def test_country_by_itself(self):
        """'Venezuela' should resolve to '152'."""
        flexible_place = FlexiblePlace("Venezuela", online=True)

        assert flexible_place.place_description == "152"

    def test_city_county_state_country(self):
        """'Eagle, Ada, Idaho, United States' should resolve to '4000719'."""
        flexible_place = FlexiblePlace("Eagle, Ada, Idaho, United States", online=True)

        assert flexible_place.place_description == "4000719"

    def test_preset_place_description(self):
        """'La Pastora, Libertador, Distrito Capital, Venezuela' should resolve to '2107883', if already set to that value"""
        flexible_place = FlexiblePlace("La Pastora, Libertador, Distrito Capital, Venezuela", "2107883", online=True)

        assert flexible_place.place_description == "2107883"

    def test_different_specificity_can_map_to_same_location(self):
        """'Mérida, Libertador, Mérida, Venezuela' and 'Mérida, Mérida, Venezuela' should resolve to '2101109'."""
        more_specific_flexible_place = FlexiblePlace("Mérida, Libertador, Mérida, Venezuela", online=True)
        less_specific_flexible_place = FlexiblePlace("Mérida, Mérida, Venezuela", online=True)

        assert more_specific_flexible_place.place_description == less_specific_flexible_place.place_description
        assert more_specific_flexible_place.place_description == "2101109"

    def test_place_matches_with_different_named_place(self):
        """'Moses Lake, Washington, United States' should resolve to '5197325' which is labled as 'Moses Lake, Grant, Washington, United States'."""
        flexible_place = FlexiblePlace("Moses Lake, Washington, United States", online=True)

        assert flexible_place.place_description == "5197325"