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

    def test_null_input(self):
        """Empty string should handle gracefully."""
        flexible_place = FlexiblePlace("", online=True)

        assert flexible_place.place_description is None or flexible_place.place_description == ""

    def test_fake_place(self):
        """Non-existent place 'Fakeville, Nonexistent, Country' should not resolve to a valid ID."""
        flexible_place = FlexiblePlace("Fakeville, Nonexistent, Country", online=True)

        assert flexible_place.place_description is None or flexible_place.place_description == ""

    def test_string_with_numbers(self):
        """Place name with numbers 'Area 51, Nevada, United States' should handle correctly."""
        flexible_place = FlexiblePlace("Area 51, Nevada, United States", online=True)

        assert flexible_place.place_description is not None

    def test_string_with_special_characters(self):
        """Place name with special characters 'São Paulo, Brazil' should resolve correctly."""
        flexible_place = FlexiblePlace("São Paulo, Brazil", online=True)

        assert flexible_place.place_description is not None and flexible_place.place_description != ""

    def test_string_with_apostrophe(self):
        """Place name with apostrophe 'Saint John's, Newfoundland, Canada' should resolve correctly."""
        flexible_place = FlexiblePlace("Saint John's, Newfoundland, Canada", online=True)

        assert flexible_place.place_description is not None

    def test_string_with_hyphens(self):
        """Place name with hyphens 'San Juan, Puerto Rico, United States' should resolve correctly."""
        flexible_place = FlexiblePlace("San Juan, Puerto Rico, United States", online=True)

        assert flexible_place.place_description is not None and flexible_place.place_description != ""

    def test_whitespace_only(self):
        """String with only whitespace should handle gracefully."""
        flexible_place = FlexiblePlace("   ", online=True)

        assert flexible_place.place_description is None or flexible_place.place_description == ""

    def test_place_with_leading_trailing_spaces(self):
        """Place name with leading and trailing spaces should resolve correctly."""
        flexible_place = FlexiblePlace("  Venezuela  ", online=True)

        assert flexible_place.place_description == "152"