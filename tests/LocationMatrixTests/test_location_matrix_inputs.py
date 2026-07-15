import unittest
from FlexiblePlace.src.LocationMatrix import LocationMatrix
from FlexiblePlace.src.FlexiblePlace import FlexiblePlace


class TestLocationMatrixInputsFromOtherTests(unittest.TestCase):
    """Test LocationMatrix construction and alignment with various inputs from compare/combine tests."""

    def test_empty_pair_constructs_with_correct_dimensions_and_format(self):
        """Verify that two empty location strings create a 2x0 matrix with proper string representation."""
        a, b = "", ""
        p1 = FlexiblePlace(a)
        p2 = FlexiblePlace(b)
        lm = LocationMatrix([p1.get_location_components(), p2.get_location_components()])
        
        expected = "|  |\n|  |"
        self.assertEqual(str(lm), expected)

    def test_first_empty_second_populated_pair_constructs_and_formats_correctly(self):
        """Verify that a pair with the first location empty and second populated aligns and formats correctly."""
        a, b = "", "Paterson, Passaic, New Jersey, United States"
        p1 = FlexiblePlace(a)
        p2 = FlexiblePlace(b)
        lm = LocationMatrix([p1.get_location_components(), p2.get_location_components()])
        
        expected = (
            "|               |            |         |          |\n"
            "| united states | new jersey | passaic | paterson |"
        )
        self.assertEqual(str(lm), expected)

    def test_first_populated_second_empty_pair_constructs_and_formats_correctly(self):
        """Verify that a pair with the first location populated and second empty aligns and formats correctly."""
        a, b = "Paterson, Passaic, New Jersey, United States", ""
        p1 = FlexiblePlace(a)
        p2 = FlexiblePlace(b)
        lm = LocationMatrix([p1.get_location_components(), p2.get_location_components()])
        
        expected = (
            "| united states | new jersey | passaic | paterson |\n"
            "|               |            |         |          |"
        )
        self.assertEqual(str(lm), expected)

    def test_identical_locations_pair_formats_correctly(self):
        """Verify that two identical locations form a matrix with matching aligned components and proper formatting."""
        a, b = "Belgium", "Belgium"
        p1 = FlexiblePlace(a)
        p2 = FlexiblePlace(b)
        lm = LocationMatrix([p1.get_location_components(), p2.get_location_components()])
        
        expected = (
            "| belgium |\n"
            "| belgium |"
        )
        self.assertEqual(str(lm), expected)

    def test_similar_nested_locations_pair_aligns_and_formats_correctly(self):
        """Verify that similar locations with different levels of detail align correctly and format properly."""
        a, b = "Camden, New Jersey, United States", "Camden, Camden, New Jersey, United States"
        p1 = FlexiblePlace(a)
        p2 = FlexiblePlace(b)
        lm = LocationMatrix([p1.get_location_components(), p2.get_location_components()])
        
        expected = (
            "| united states | new jersey | camden |        |\n"
            "| united states | new jersey | camden | camden |"
        )
        self.assertEqual(str(lm), expected)

    def test_misspelled_location_pair_aligns_and_formats_correctly(self):
        """Verify that a pair with misspelled/typo locations aligns despite differences and formats correctly."""
        a, b = "No Croghan J*, New York, United States", "New York, United States"
        p1 = FlexiblePlace(a)
        p2 = FlexiblePlace(b)
        lm = LocationMatrix([p1.get_location_components(), p2.get_location_components()])
        
        expected = (
            "| united states | new york | no croghan j* |\n"
            "| united states | new york |               |"
        )
        self.assertEqual(str(lm), expected)

    def test_whitespace_only_pair_constructs_and_formats_correctly(self):
        """Verify that a pair of whitespace-only strings constructs without error and formats properly."""
        a, b = "   ", "   "
        p1 = FlexiblePlace(a)
        p2 = FlexiblePlace(b)
        lm = LocationMatrix([p1.get_location_components(), p2.get_location_components()])
        
        expected = "|  |\n|  |"
        self.assertEqual(str(lm), expected)

    def test_different_detail_levels_pair_aligns_and_formats_correctly(self):
        """Verify that locations with different detail levels align properly and format with correct structure."""
        a, b = "Houston, Texas", "Houston, Harris, Texas, United States"
        p1 = FlexiblePlace(a)
        p2 = FlexiblePlace(b)
        lm = LocationMatrix([p1.get_location_components(), p2.get_location_components()])
        
        expected = (
            "|               | texas |        | houston |\n"
            "| united states | texas | harris | houston |"
        )
        self.assertEqual(str(lm), expected)

    def test_single_location_group_constructs_and_formats_correctly(self):
        """Verify that a group with a single location constructs with correct dimensions and formats properly."""
        group = ["Belgium"]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = "| belgium |"
        self.assertEqual(str(lm), expected)

    def test_duplicate_locations_group_aligns_and_formats_correctly(self):
        """Verify that a group with duplicate identical locations aligns all rows and formats correctly."""
        group = ["Belgium", "Belgium"]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = (
            "| belgium |\n"
            "| belgium |"
        )
        self.assertEqual(str(lm), expected)

    def test_similar_and_different_locations_group_aligns_and_formats_correctly(self):
        """Verify that a group mixing similar locations and different ones aligns correctly and formats properly."""
        group = ["Paris", "Belgium"]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = (
            "| paris   |\n"
            "| belgium |"
        )
        self.assertEqual(str(lm), expected)

    def test_misspelled_location_group_aligns_and_formats_correctly(self):
        """Verify that a group with misspelled variants aligns despite typos and formats correctly."""
        group = ["Melgium", "Belgium"]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = (
            "| melgium |\n"
            "| belgium |"
        )
        self.assertEqual(str(lm), expected)

    def test_multi_level_camden_group_aligns_and_formats_correctly(self):
        """Verify that a group with Camden at different detail levels aligns correctly and formats properly."""
        group = [
            "Camden, New Jersey",
            "Camden, Camden, New Jersey, United States",
            "reallylongcityname, reallylongcountyname, reallylongstatename, reallylongcountryname"
        ]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = (
            "|                       | new jersey          | camden               |                    |\n"
            "| united states         | new jersey          | camden               | camden             |\n"
            "| reallylongcountryname | reallylongstatename | reallylongcountyname | reallylongcityname |"
        )
        self.assertEqual(str(lm), expected)

    def test_multi_level_new_york_group_aligns_and_formats_correctly(self):
        """Verify that a group with New York at different levels aligns correctly and formats properly."""
        group = [
            "New York, New York, United States",
            "New York, United States",
            "reallylongcityname, reallylongstatename, United States"
        ]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = (
            "| united states | new york            | new york           |\n"
            "| united states | new york            |                    |\n"
            "| united states | reallylongstatename | reallylongcityname |"
        )
        self.assertEqual(str(lm), expected)

    def test_lawrence_massachusetts_group_aligns_and_formats_correctly(self):
        """Verify that Lawrence, Massachusetts variations align correctly and format properly."""
        group = [
            "Lawrence, Massachusetts, United States",
            "Lawrence, Essex, Massachusetts, United States"
        ]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = (
            "| united states | massachusetts |       | lawrence |\n"
            "| united states | massachusetts | essex | lawrence |"
        )
        self.assertEqual(str(lm), expected)

    def test_buffalo_new_york_group_aligns_and_formats_correctly(self):
        """Verify that Buffalo, New York variations align correctly and format properly."""
        group = [
            "Buffalo, New York, United States",
            "Buffalo, Erie, New York"
        ]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = (
            "| united states | new york |      | buffalo |\n"
            "|               | new york | erie | buffalo |"
        )
        self.assertEqual(str(lm), expected)

    def test_springfield_illinois_group_aligns_and_formats_correctly(self):
        """Verify that Springfield, Illinois with various detail levels aligns correctly and formats properly."""
        group = [
            "Springfield, Sangamon, Illinois",
            "Springfield, Illinois, United States",
            "reallylongcityname, Sangamon, Illinois, United States"
        ]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = (
            "|               | illinois | sangamon | springfield        |\n"
            "| united states | illinois |          | springfield        |\n"
            "| united states | illinois | sangamon | reallylongcityname |"
        )
        self.assertEqual(str(lm), expected)

    def test_philadelphia_abbreviated_group_aligns_and_formats_correctly(self):
        """Verify that Philadelphia abbreviated variations align correctly and format properly."""
        group = [
            "Phila, Pennsylvania, United States",
            "Philadelphia, Pennsylvania"
        ]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = (
            "| united states | pennsylvania | phila        |\n"
            "|               | pennsylvania | philadelphia |"
        )
        self.assertEqual(str(lm), expected)

    def test_elder_township_pennsylvania_two_location_group_aligns_and_formats_correctly(self):
        """Verify that Elder Township, Pennsylvania variations align correctly and format properly."""
        group = [
            "Elder Twp, Pennsylvania, United States",
            "Elder Township, Cambria, Pennsylvania"
        ]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = (
            "| united states | pennsylvania |         | elder twp      |\n"
            "|               | pennsylvania | cambria | elder township |"
        )
        self.assertEqual(str(lm), expected)

    def test_elder_township_pennsylvania_three_location_group_aligns_and_formats_correctly(self):
        """Verify that Elder Township, Pennsylvania with three variations aligns correctly and formats properly."""
        group = [
            "Elder Twp, Pennsylvania, United States",
            "Elder Township, Cambria, Pennsylvania",
            "reallylongcityname, Pennsylvania, United States"
        ]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = (
            "| united states | pennsylvania |         | elder twp      |\n"
            "|               | pennsylvania | cambria | elder township |\n"
            "| united states | pennsylvania |         |                |"
        )
        self.assertEqual(str(lm), expected)

    def test_philadelphia_monthly_meeting_group_aligns_and_formats_correctly(self):
        """Verify that Philadelphia variations aligns correctly and formats properly."""
        group = [
            "Phila, Pennsylvania, United States",
            "Philadelphia Monthly Meeting, Philadelphia, Pennsylvania"
        ]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = (
            "| united states | pennsylvania | phila        |                              |\n"
            "|               | pennsylvania | philadelphia | philadelphia monthly meeting |"
        )
        self.assertEqual(str(lm), expected)

    def test_sugarloaf_township_pennsylvania_group_aligns_and_formats_correctly(self):
        """Verify that Sugarloaf Township, Pennsylvania with county information aligns correctly and formats properly."""
        group = [
            "Sugarloaf Township, Pennsylvania, United States",
            "Luzerne, Pennsylvania",
            "Sugarloaf Township, Luzerne, Pennsylvania"
        ]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = (
            "| united states | pennsylvania |         | sugarloaf township |\n"
            "|               | pennsylvania | luzerne |                    |\n"
            "|               | pennsylvania | luzerne | sugarloaf township |"
        )
        self.assertEqual(str(lm), expected)

    def test_paris_disambiguation_group_aligns_and_formats_correctly(self):
        """Verify that Paris in different countries disambiguates and aligns correctly and formats properly."""
        group = [
            "Paris, France",
            "Paris, Texas",
            "Texas, United States"
        ]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = (
            "| france        |       | paris |\n"
            "|               | texas | paris |\n"
            "| united states | texas |       |"
        )
        self.assertEqual(str(lm), expected)

    def test_new_york_disambiguation_group_aligns_and_formats_correctly(self):
        """Verify that New York in different locations disambiguates and aligns correctly and formats properly."""
        group = [
            "New York, Iowa, United States",
            "New York, New York, United States",
            "New York, United States"
        ]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = (
            "| united states | iowa     | new york |\n"
            "| united states | new york | new york |\n"
            "| united states | new york |          |"
        )
        self.assertEqual(str(lm), expected)

    def test_washington_disambiguation_group_aligns_and_formats_correctly(self):
        """Verify that Washington in different states disambiguates and aligns correctly and formats properly."""
        group = [
            "Washington, Utah",
            "Walla Walla, Washington",
            "Washington, United States"
        ]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = (
            "| utah          | washington |             |\n"
            "|               | washington | walla walla |\n"
            "| united states | washington |             |"
        )
        self.assertEqual(str(lm), expected)

    def test_complex_washington_group_aligns_and_formats_correctly(self):
        """Verify that a complex group with multiple Washington variations aligns correctly and formats properly."""
        group = [
            "United States",
            "Belgium",
            "Washington, Utah",
            "Walla Walla, Washington",
            "Washington, United States"
        ]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = (
            "| united states |            |             |\n"
            "| belgium       |            |             |\n"
            "| utah          | washington |             |\n"
            "|               | washington | walla walla |\n"
            "| united states | washington |             |"
        )
        self.assertEqual(str(lm), expected)

    def test_massachusetts_bay_colony_group_aligns_and_formats_correctly(self):
        """Verify that historical locations like Massachusetts Bay Colony align correctly with modern locations and format properly."""
        group = [
            "Massachusetts Bay Colony, British Colonial America",
            "British Colonial America",
            "Lincoln, Massachusetts Bay Colony",
            "Bucksport, Lincoln, Massachusetts Bay Colony",
            "Lincoln, Massachusetts Bay Colony, British Colonial America",
            "reallysuperlongcityname, reallysuperlongcountyname, reallysuperlongstatename, reallysuperlongcountryname",
            "Belgium"
        ]
        fps = [FlexiblePlace(s) for s in group]
        lm = LocationMatrix([fp.get_location_components() for fp in fps])
        
        expected = (
            "| british colonial america   | massachusetts bay colony | reallysuperlongcountyname |                         |\n"
            "| british colonial america   |                          |                           |                         |\n"
            "|                            | massachusetts bay colony | lincoln                   |                         |\n"
            "|                            | massachusetts bay colony | lincoln                   | bucksport               |\n"
            "| british colonial america   | massachusetts bay colony | lincoln                   |                         |\n"
            "| reallysuperlongcountryname | reallysuperlongstatename | reallysuperlongcountyname | reallysuperlongcityname |\n"
            "| belgium                    |                          |                           |                         |"
        )
        self.assertEqual(str(lm), expected)


if __name__ == "__main__":
    unittest.main()