import pytest
from FlexiblePlace.src.location_matrix import LocationMatrix
from FlexiblePlace.src.FlexiblePlace import FlexiblePlace


class TestLocationMatrixAlignment:
    """Test LocationMatrix construction and alignment."""

    def test_empty_pair_constructs_with_correct_dimensions_and_format(self) -> None:
        """Verify that two empty location strings create a 2x0 matrix with proper string representation."""
        a, b = "", ""
        p1 = FlexiblePlace(a, auto_fill=False)
        p2 = FlexiblePlace(b, auto_fill=False)
        lm = LocationMatrix([p1.location, p2.location])
        
        expected = "|  |\n|  |"
        assert str(lm) == expected

    def test_single_location_group_constructs_and_formats_correctly(self) -> None:
        """Verify that a group with a single location constructs with correct dimensions and formats properly."""
        group = ["Belgium"]
        fps = [FlexiblePlace(s, auto_fill=False) for s in group]
        lm = LocationMatrix([fp.location for fp in fps])
        
        expected = "| belgium |"
        assert str(lm) == expected


    def test_first_empty_second_populated_pair_constructs_and_formats_correctly(self) -> None:
        """Verify that a pair with the first location empty and second populated aligns and formats correctly."""
        a, b = "", "Paterson, Passaic, New Jersey, United States"
        p1 = FlexiblePlace(a, auto_fill=False)
        p2 = FlexiblePlace(b, auto_fill=False)
        lm = LocationMatrix([p1.location, p2.location])
        
        expected = (
            "| united states | new jersey | passaic | paterson |\n"
            "|               |            |         |          |"
        )
        assert str(lm) == expected

    def test_similar_nested_locations_pair_aligns_and_formats_correctly(self) -> None:
        """Verify that similar locations with different levels of detail align correctly and format properly."""
        a, b = "Camden, New Jersey, United States", "Camden, Camden, New Jersey, United States"
        p1 = FlexiblePlace(a, auto_fill=False)
        p2 = FlexiblePlace(b, auto_fill=False)
        lm = LocationMatrix([p1.location, p2.location])
        
        expected = (
            "| united states | new jersey | camden | camden |\n"
            "| united states | new jersey | camden |        |"
        )
        assert str(lm) == expected

    def test_different_detail_levels_pair_aligns_and_formats_correctly(self) -> None:
        """Verify that locations with different detail levels align properly and format with correct structure."""
        a, b = "Houston, Texas", "Houston, Harris, Texas, United States"
        p1 = FlexiblePlace(a, auto_fill=False)
        p2 = FlexiblePlace(b, auto_fill=False)
        lm = LocationMatrix([p1.location, p2.location])
        
        expected = (
            "| united states | texas | harris | houston |\n"
            "|               | texas |        | houston |"
        )
        assert str(lm) == expected

    def test_multi_level_camden_group_aligns_and_formats_correctly(self) -> None:
        """Verify that a group with Camden at different detail levels aligns correctly and formats properly."""
        group = [
            "Camden, New Jersey",
            "Camden, Camden, New Jersey, United States",
            "reallylongcityname, reallylongcountyname, reallylongstatename, reallylongcountryname"
        ]
        fps = [FlexiblePlace(s, auto_fill=False) for s in group]
        lm = LocationMatrix([fp.location for fp in fps])
        
        expected = (
            "| united states         | new jersey          | camden               | camden             |\n"
            "| reallylongcountryname | reallylongstatename | reallylongcountyname | reallylongcityname |\n"
            "|                       | new jersey          | camden               |                    |"
        )
        assert str(lm) == expected

    def test_springfield_illinois_group_aligns_and_formats_correctly(self) -> None:
        """Verify that Springfield, Illinois with various detail levels aligns correctly and formats properly."""
        group = [
            "Springfield, Sangamon, Illinois",
            "Springfield, Illinois, United States",
            "reallylongcityname, Sangamon, Illinois, United States"
        ]
        fps = [FlexiblePlace(s, auto_fill=False) for s in group]
        lm = LocationMatrix([fp.location for fp in fps])
        
        expected = (
            "| united states | illinois | sangamon | reallylongcityname |\n"
            "|               | illinois | sangamon | springfield        |\n"
            "| united states | illinois |          | springfield        |"
        )
        assert str(lm) == expected

    def test_paris_disambiguation_group_aligns_and_formats_correctly(self) -> None:
        """Verify that Paris in different countries disambiguates and aligns correctly and formats properly."""
        group = [
            "Paris, France",
            "Paris, Texas",
            "Texas, United States"
        ]
        fps = [FlexiblePlace(s, auto_fill=False) for s in group]
        lm = LocationMatrix([fp.location for fp in fps])
        
        expected = (
            "| france        |       | paris |\n"
            "|               | texas | paris |\n"
            "| united states | texas |       |"
        )
        assert str(lm) == expected

    def test_massachusetts_bay_colony_group_aligns_and_formats_correctly(self) -> None:
        """Verify that a larger set of inputs can still be aligned properly."""
        group = [
            "Massachusetts Bay Colony, British Colonial America",
            "British Colonial America",
            "Lincoln, Massachusetts Bay Colony",
            "Bucksport, Lincoln, Massachusetts Bay Colony",
            "Lincoln, Massachusetts Bay Colony, British Colonial America",
            "reallysuperlongcityname, reallysuperlongcountyname, reallysuperlongstatename, reallysuperlongcountryname",
            "Belgium"
        ]
        fps = [FlexiblePlace(s, auto_fill=False) for s in group]
        lm = LocationMatrix([fp.location for fp in fps])
        
        expected = (
            "| reallysuperlongcountryname | reallysuperlongstatename | reallysuperlongcountyname | reallysuperlongcityname |\n"
            "|                            | massachusetts bay colony | lincoln                   | bucksport               |\n"
            "| british colonial america   | massachusetts bay colony | lincoln                   |                         |\n"
            "| british colonial america   | massachusetts bay colony |                           |                         |\n"
            "|                            | massachusetts bay colony | lincoln                   |                         |\n"
            "| british colonial america   |                          |                           |                         |\n"
            "| belgium                    |                          |                           |                         |"
        )
        assert str(lm) == expected
