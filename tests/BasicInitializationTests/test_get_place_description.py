import pytest

from FlexiblePlace.src.FlexiblePlace import FlexiblePlace


class TestGetPlaceDescription:
    """Tests for FlexiblePlace.place_description when initialized online."""

    def test_flexible_place_online_initializes_place_description_for_eagle_ada_idaho_united_states(self):
        """Eagle, Ada, Idaho, United States should resolve to #4000719."""
        flexible_place = FlexiblePlace("Eagle, Ada, Idaho, United States", online=True)

        assert flexible_place.place_description == "#4000719"

    def test_flexible_place_online_initializes_place_description_for_horseshoe_bend_boise_idaho_united_states(self):
        """Horseshoe Bend, Boise, Idaho, United States should resolve to #4001402."""
        flexible_place = FlexiblePlace("Horseshoe Bend, Boise, Idaho, United States", online=True)

        assert flexible_place.place_description == "#4001402"

    def test_flexible_place_online_initializes_place_description_for_united_states(self):
        """United States should resolve to #1."""
        flexible_place = FlexiblePlace("United States", online=True)

        assert flexible_place.place_description == "#1"

    def test_flexible_place_online_initializes_place_description_for_la_pastora_libertador_distrito_capital_venezuela(self):
        """La Pastora, Libertador, Distrito Capital, Venezuela should resolve to #2107883."""
        flexible_place = FlexiblePlace("La Pastora, Libertador, Distrito Capital, Venezuela", online=True)

        assert flexible_place.place_description == "#2107883"

    def test_flexible_place_online_initializes_place_description_for_merida_libertador_merida_venezuela(self):
        """Mérida, Libertador, Mérida, Venezuela should resolve to #2101109."""
        flexible_place = FlexiblePlace("Mérida, Libertador, Mérida, Venezuela", online=True)

        assert flexible_place.place_description == "#2101109"

    def test_flexible_place_online_initializes_place_description_for_merida_merida_venezuela(self):
        """Mérida, Mérida, Venezuela should resolve to #2101109."""
        flexible_place = FlexiblePlace("Mérida, Mérida, Venezuela", online=True)

        assert flexible_place.place_description == "#2101109"

    def test_flexible_place_online_initializes_place_description_for_nuestra_senora_de_las_misericordias_maiquetia_vargas_la_guaira_venezuela(self):
        """Nuestra Señora de las Misericordias, Maiquetía, Vargas, La Guaira, Venezuela should resolve to #2111324."""
        flexible_place = FlexiblePlace("Nuestra Señora de las Misericordias, Maiquetía, Vargas, La Guaira, Venezuela", online=True)

        assert flexible_place.place_description == "#2111324"

    def test_flexible_place_online_initializes_place_description_for_maiquetia_vargas_venezuela(self):
        """Maiquetía, Vargas, Venezuela should resolve to #2111324."""
        flexible_place = FlexiblePlace("Maiquetía, Vargas, Venezuela", online=True)

        assert flexible_place.place_description == "#2111324"

    def test_flexible_place_online_initializes_place_description_for_sigurd_sevier_utah_united_states(self):
        """Sigurd, Sevier, Utah, United States should resolve to #5312299."""
        flexible_place = FlexiblePlace("Sigurd, Sevier, Utah, United States", online=True)

        assert flexible_place.place_description == "#5312299"

    def test_flexible_place_online_initializes_place_description_for_moses_lake_grant_washington_united_states(self):
        """Moses Lake, Grant, Washington, United States should resolve to #5197325."""
        flexible_place = FlexiblePlace("Moses Lake, Grant, Washington, United States", online=True)

        assert flexible_place.place_description == "#5197325"

    def test_flexible_place_online_initializes_place_description_for_moses_lake_washington_united_states(self):
        """Moses Lake, Washington, United States should resolve to #5197325."""
        flexible_place = FlexiblePlace("Moses Lake, Washington, United States", online=True)

        assert flexible_place.place_description == "#5197325"

    def test_flexible_place_online_initializes_place_description_for_la_palma_el_paso_santa_cruz_de_tenerife_canarias_spain(self):
        """La Palma, El Paso, Santa Cruz de Tenerife, Canarias, Spain should resolve to #3460975."""
        flexible_place = FlexiblePlace("La Palma, El Paso, Santa Cruz de Tenerife, Canarias, Spain", online=True)

        assert flexible_place.place_description == "#3460975"

    def test_flexible_place_online_initializes_place_description_for_el_paso_la_palma_santa_cruz_de_tenerife_canary_islands_spain(self):
        """El Paso, La Palma, Santa Cruz de Tenerife, Canary Islands, Spain should resolve to #3460975."""
        flexible_place = FlexiblePlace("El Paso, La Palma, Santa Cruz de Tenerife, Canary Islands, Spain", online=True)

        assert flexible_place.place_description == "#3460975"

    def test_flexible_place_online_initializes_place_description_for_venezuela(self):
        """Venezuela should resolve to #152."""
        flexible_place = FlexiblePlace("Venezuela", online=True)

        assert flexible_place.place_description == "#152"
