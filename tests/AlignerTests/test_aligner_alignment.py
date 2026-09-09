import pytest
from FlexiblePlace.src.Aligner import Aligner
from FlexiblePlace.src.FlexiblePlace import FlexiblePlace


class TestAlignerAlignment:
    """Test Aligner construction and alignment."""

    def test_empty_pair_constructs_with_correct_dimensions_and_format(self) -> None:
        """Verify that two empty location strings create a 2x0 matrix with proper string representation."""
        a, b = "", ""
        p1 = FlexiblePlace(a, auto_fill=False)
        p2 = FlexiblePlace(b, auto_fill=False)
        aligner = Aligner([p1.location, p2.location])
        
        expected = "|  |\n|  |"
        assert str(aligner) == expected

    def test_single_location_group_constructs_and_formats_correctly(self) -> None:
        """Verify that a group with a single location constructs with correct dimensions and formats properly."""
        group = ["Belgium"]
        fps = [FlexiblePlace(s, auto_fill=False) for s in group]
        aligner = Aligner([fp.location for fp in fps])
        
        expected = "| belgium |"
        assert str(aligner) == expected


    def test_first_empty_second_populated_pair_constructs_and_formats_correctly(self) -> None:
        """Verify that a pair with the first location empty and second populated aligns and formats correctly."""
        a, b = "", "Paterson, Passaic, New Jersey, United States"
        p1 = FlexiblePlace(a, auto_fill=False)
        p2 = FlexiblePlace(b, auto_fill=False)
        aligner = Aligner([p1.location, p2.location])
        
        expected = (
            "| paterson | passaic | new jersey | united states |\n"
            "|          |         |            |               |"
        )
        assert str(aligner) == expected

    def test_similar_nested_locations_pair_aligns_and_formats_correctly(self) -> None:
        """Verify that similar locations with different levels of detail align correctly and format properly."""
        a, b = "Camden, New Jersey, United States", "Camden, Camden, New Jersey, United States"
        p1 = FlexiblePlace(a, auto_fill=False)
        p2 = FlexiblePlace(b, auto_fill=False)
        aligner = Aligner([p1.location, p2.location])
        
        expected = (
            "| camden | camden | new jersey | united states |\n"
            "|        | camden | new jersey | united states |"
        )
        assert str(aligner) == expected

    def test_different_detail_levels_pair_aligns_and_formats_correctly(self) -> None:
        """Verify that locations with different detail levels align properly and format with correct structure."""
        a, b = "Houston, Texas", "Houston, Harris, Texas, United States"
        p1 = FlexiblePlace(a, auto_fill=False)
        p2 = FlexiblePlace(b, auto_fill=False)
        aligner = Aligner([p1.location, p2.location])
        
        expected = (
            "| houston | harris | texas | united states |\n"
            "| houston |        | texas |               |"
        )
        assert str(aligner) == expected

    def test_multi_level_camden_group_aligns_and_formats_correctly(self) -> None:
        """Verify that a group with Camden at different detail levels aligns correctly and formats properly."""
        group = [
            "Camden, New Jersey",
            "Camden, Camden, New Jersey, United States",
            "reallylongcityname, reallylongcountyname, reallylongstatename, reallylongcountryname"
        ]
        fps = [FlexiblePlace(s, auto_fill=False) for s in group]
        aligner = Aligner([fp.location for fp in fps])
        
        expected = (
            "| camden             | camden               | new jersey          | united states         |\n"
            "| reallylongcityname | reallylongcountyname | reallylongstatename | reallylongcountryname |\n"
            "|                    | camden               | new jersey          |                       |"
        )
        assert str(aligner) == expected

    def test_springfield_illinois_group_aligns_and_formats_correctly(self) -> None:
        """Verify that Springfield, Illinois with various detail levels aligns correctly and formats properly."""
        group = [
            "Springfield, Sangamon, Illinois",
            "Springfield, Illinois, United States",
            "reallylongcityname, Sangamon, Illinois, United States"
        ]
        fps = [FlexiblePlace(s, auto_fill=False) for s in group]
        aligner = Aligner([fp.location for fp in fps])
        
        expected = (
            "| reallylongcityname | sangamon | illinois | united states |\n"
            "| springfield        | sangamon | illinois |               |\n"
            "| springfield        |          | illinois | united states |"
        )
        assert str(aligner) == expected

    def test_paris_disambiguation_group_aligns_and_formats_correctly(self) -> None:
        """Verify that Paris in different countries disambiguates and aligns correctly and formats properly."""
        group = [
            "Paris, France",
            "Paris, Texas",
            "Texas, United States"
        ]
        fps = [FlexiblePlace(s, auto_fill=False) for s in group]
        aligner = Aligner([fp.location for fp in fps])
        
        expected = (
            "| paris |       | france        |\n"
            "| paris | texas |               |\n"
            "|       | texas | united states |"
        )
        assert str(aligner) == expected

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
        aligner = Aligner([fp.location for fp in fps])
        
        expected = (
            "| reallysuperlongcityname | reallysuperlongcountyname | reallysuperlongstatename | reallysuperlongcountryname |\n"
            "| bucksport               | lincoln                   | massachusetts bay colony |                            |\n"
            "|                         | lincoln                   | massachusetts bay colony | british colonial america   |\n"
            "|                         |                           | massachusetts bay colony | british colonial america   |\n"
            "|                         | lincoln                   | massachusetts bay colony |                            |\n"
            "|                         |                           |                          | british colonial america   |\n"
            "|                         |                           |                          | belgium                    |"
        )
        assert str(aligner) == expected
