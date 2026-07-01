import unittest
from src.flexible_place import FlexiblePlace


class TestCombineFlexiblePlaces(unittest.TestCase):
    """Test suite for FlexiblePlace.combine_flexible_places static method"""

    def test_null_returns_null(self):
        """Test: Null returns null
        Input: []
        Output: None
        """
        places = []
        result = FlexiblePlace.combine_flexible_places(places)
        self.assertIsNone(result)

    def test_single_object_returns_same_object(self):
        """Test: Single object returns the same object
        Input: [FlexiblePlace("Belgium")]
        Output: FlexiblePlace("Belgium")
        """
        places = [FlexiblePlace("Belgium")]
        result = FlexiblePlace.combine_flexible_places(places)
        self.assertEqual(str(result), "Belgium")

    def test_duplicate_objects_return_same_object(self):
        """Test: Duplicate objects return same object
        Input: [FlexiblePlace("Belgium"),
                FlexiblePlace("Belgium")]
        Output: FlexiblePlace("Belgium")
        """
        places = [FlexiblePlace("Belgium"), FlexiblePlace("Belgium")]
        result = FlexiblePlace.combine_flexible_places(places)
        self.assertEqual(str(result), "Belgium")

    def test_indecision_yields_longest_string(self):
        """Test: Indecision yields longest string
        Input: [FlexiblePlace("Paris"),
                FlexiblePlace("Belgium")]
        Output: FlexiblePlace("Belgium")
        """
        places = [FlexiblePlace("Paris"), FlexiblePlace("Belgium")]
        result = FlexiblePlace.combine_flexible_places(places)
        self.assertEqual(str(result), "Belgium")

    def test_tie_yields_first(self):
        """Test: Tie yields first
        Input: [FlexiblePlace("Melgium"),
                FlexiblePlace("Belgium")]
        Output: FlexiblePlace("Melgium")
        """
        places = [FlexiblePlace("Melgium"), FlexiblePlace("Belgium")]
        result = FlexiblePlace.combine_flexible_places(places)
        self.assertEqual(str(result), "Melgium")

    def test_more_specific_replaces_less_specific_case_1(self):
        """Test: More specific replaces less specific if same location (Case 1)
        Input: [FlexiblePlace("Camden, New Jersey"),
                FlexiblePlace("Camden, Camden, New Jersey, United States")
                FlexiblePlace("reallylongcityname, reallylongcountyname, reallylongstatename, reallylongcountryname")]
        Output: FlexiblePlace("Camden, Camden, New Jersey, United States")
        """
        places = [FlexiblePlace("Camden, New Jersey"), FlexiblePlace("Camden, Camden, New Jersey, United States"), FlexiblePlace("reallylongcityname, reallylongcountyname, reallylongstatename, reallylongcountryname")]
        result = FlexiblePlace.combine_flexible_places(places)
        self.assertEqual(str(result), "Camden, Camden, New Jersey, United States")

    def test_more_specific_replaces_less_specific_case_2(self):
        """Test: More specific replaces less specific if same location (Case 2)
        Input: [FlexiblePlace("New York, New York, United States"),
                FlexiblePlace("New York, United States"),
                FlexiblePlace("reallylongcityname, reallylongstatename, UnitedStates")]
        Output: FlexiblePlace("New York, New York, United States")
        """
        places = [
            FlexiblePlace("New York, New York, United States"),
            FlexiblePlace("New York, United States"),
            FlexiblePlace("reallylongcityname, reallylongstatename, UnitedStates")
        ]
        result = FlexiblePlace.combine_flexible_places(places)
        self.assertEqual(str(result), "New York, New York, United States")

    def test_combining_location_with_county_versus_not_case_1(self):
        """Test: Combining location with county versus not with county (Case 1)
        Input: [FlexiblePlace("Lawrence, Massachusetts, United States"),
                FlexiblePlace("Lawrence, Essex, Massachusetts, United States")]
        Output: FlexiblePlace("Lawrence, Essex, Massachusetts, United States")
        """
        places = [
            FlexiblePlace("Lawrence, Massachusetts, United States"),
            FlexiblePlace("Lawrence, Essex, Massachusetts, United States")
        ]
        result = FlexiblePlace.combine_flexible_places(places)
        self.assertEqual(str(result), "Lawrence, Essex, Massachusetts, United States")

    def test_combining_location_with_county_versus_not_case_2(self):
        """Test: Combining location with county versus not with county (Case 2)
        Input: [FlexiblePlace("Buffalo, New York, United States"),
                FlexiblePlace("Buffalo, Erie, New York")]
        Output: FlexiblePlace("Buffalo, Erie, New York, United States")
        """
        places = [
            FlexiblePlace("Buffalo, New York, United States"),
            FlexiblePlace("Buffalo, Erie, New York")
        ]
        result = FlexiblePlace.combine_flexible_places(places)
        self.assertEqual(str(result), "Buffalo, Erie, New York, United States")

    def test_combining_location_with_county_versus_not_case_3(self):
        """Test: Combining location with county versus not with county (Case 3)
        Input: [FlexiblePlace("Springfield, Sangamon, Illinois"),
                FlexiblePlace("Springfield, Illinois, United States"),
                FlexiblePlace("reallylongcityname, Sangamon, Illinois, United States")]
        Output: FlexiblePlace("Springfield, Sangamon, Illinois, United States")
        """
        places = [
            FlexiblePlace("Springfield, Sangamon, Illinois"),
            FlexiblePlace("Springfield, Illinois, United States"),
            FlexiblePlace("reallylongcityname, Sangamon, Illinois, United States")
        ]
        result = FlexiblePlace.combine_flexible_places(places)
        self.assertEqual(str(result), "Springfield, Sangamon, Illinois, United States")

    def test_correctly_matches_abbreviations_case_1(self):
        """Test: Correctly matches abbreviations (Case 1)
        Input: [FlexiblePlace("Phila, Pennsylvania, United States"),
                FlexiblePlace("Philadelphia, Pennsylvania")]
        Output: FlexiblePlace("Philadelphia, Pennsylvania, United States")
        """
        places = [
            FlexiblePlace("Phila, Pennsylvania, United States"),
            FlexiblePlace("Philadelphia, Pennsylvania")
        ]
        result = FlexiblePlace.combine_flexible_places(places)
        self.assertEqual(str(result), "Philadelphia, Pennsylvania, United States")

    def test_correctly_matches_abbreviations_case_2(self):
        """Test: Correctly matches abbreviations (Case 2)
        Input: [FlexiblePlace("Elder Twp, Pennsylvania, United States"),
                FlexiblePlace("Elder Township, Cambria, Pennsylvania")]
        Output: FlexiblePlace("Elder Township, Cambria, Pennsylvania, United States")
        """
        places = [
            FlexiblePlace("Elder Twp, Pennsylvania, United States"),
            FlexiblePlace("Elder Township, Cambria, Pennsylvania")
        ]
        result = FlexiblePlace.combine_flexible_places(places)
        self.assertEqual(str(result), "Elder Township, Cambria, Pennsylvania, United States")

    def test_correctly_matches_abbreviations_case_3(self):
        """Test: Correctly matches abbreviations (Case 3)
        Input: [FlexiblePlace("Elder Twp, Pennsylvania, United States"),
                FlexiblePlace("Elder Township, Cambria, Pennsylvania"),
                FlexiblePlace("reallylongcityname, Pennsylvania, United States")]
        Output: FlexiblePlace("Elder Township, Cambria, Pennsylvania, United States")
        """
        places = [
            FlexiblePlace("Elder Twp, Pennsylvania, United States"),
            FlexiblePlace("Elder Township, Cambria, Pennsylvania"),
            FlexiblePlace("reallylongcityname, Pennsylvania, United States")
        ]
        result = FlexiblePlace.combine_flexible_places(places)
        self.assertEqual(str(result), "Elder Township, Cambria, Pennsylvania, United States")

    def test_correctly_matches_abbreviations_case_4(self):
        """Test: Correctly matches abbreviations (Case 4)
        Input: [FlexiblePlace("Phila, Pennsylvania, United States"),
                FlexiblePlace("Philadelphia Monthly Meeting, Philadelphia, Philadelphia, Pennsylvania")]
        Output: FlexiblePlace("Philadelphia Monthly Meeting, Philadelphia, Philadelphia, Pennsylvania, United States")
        """
        places = [
            FlexiblePlace("Phila, Pennsylvania, United States"),
            FlexiblePlace("Philadelphia Monthly Meeting, Philadelphia, Philadelphia, Pennsylvania")
        ]
        result = FlexiblePlace.combine_flexible_places(places)
        self.assertEqual(str(result), "Philadelphia Monthly Meeting, Philadelphia, Philadelphia, Pennsylvania, United States")

    def test_combines_data_from_incomplete_but_matching_sources(self):
        """Test: Combines data from incomplete, but matching, sources
        Input: [FlexiblePlace("Sugarloaf Township, Pennsylvania, United States"),
                FlexiblePlace("Luzerne, Pennsylvania"),
                FlexiblePlace("Sugarloaf Township, Luzerne, Pennsylvania")]
        Output: FlexiblePlace("Sugarloaf Township, Luzerne, Pennsylvania, United States")
        """
        places = [
            FlexiblePlace("Sugarloaf Township, Pennsylvania, United States"),
            FlexiblePlace("Luzerne, Pennsylvania"),
            FlexiblePlace("Sugarloaf Township, Luzerne, Pennsylvania")
        ]
        result = FlexiblePlace.combine_flexible_places(places)
        self.assertEqual(str(result), "Sugarloaf Township, Luzerne, Pennsylvania, United States")

    def test_disambiguates_multiple_locations_case_1(self):
        """Test: Disambiguates multiple locations (Case 1)
        Input: [FlexiblePlace("Paris, France"), FlexiblePlace("Paris, Texas"),
                FlexiblePlace("Texas, United States")]
        Output: FlexiblePlace("Paris, Texas, United States")
        """
        places = [
            FlexiblePlace("Paris, France"),
            FlexiblePlace("Paris, Texas"),
            FlexiblePlace("Texas, United States")
        ]
        result = FlexiblePlace.combine_flexible_places(places)
        self.assertEqual(str(result), "Paris, Texas, United States")

    def test_disambiguates_multiple_locations_case_2(self):
        """Test: Disambiguates multiple locations (Case 2)
        Input: [FlexiblePlace("United States"),
                FlexiblePlace("Belgium"),
                FlexiblePlace("Washington, Utah"),
                FlexiblePlace("Walla Walla, Washington"),
                FlexiblePlace("Washington, United States")]
        Output: FlexiblePlace("Walla Walla, Washington, United States")
        """
        places = [
            FlexiblePlace("United States"),
            FlexiblePlace("Belgium"),
            FlexiblePlace("Washington, Utah"),
            FlexiblePlace("Walla Walla, Washington"),
            FlexiblePlace("Washington, United States")
        ]
        result = FlexiblePlace.combine_flexible_places(places)
        self.assertEqual(str(result), "Walla Walla, Washington, United States")

    def test_works_with_a_ton_of_inputs_at_once(self):
        """Test: Works with a ton of inputs at once
        Input: [
            FlexiblePlace("Massachusetts Bay Colony, British Colonial America"),
            FlexiblePlace("British Colonial America"),
            FlexiblePlace("Lincoln, Massachusetts Bay Colony"),
            FlexiblePlace("Bucksport, Lincoln, Massachusetts Bay Colony"),
            FlexiblePlace("Lincoln, Massachusetts Bay Colony, British Colonial America"),
            FlexiblePlace("reallysuperlongcityname, reallysuperlongcountyname, reallysuperlongstatename, reallysuperlongcountryname"),
            FlexiblePlace("Belgium")
        ]
        Output: FlexiblePlace("Bucksport, Lincoln, Massachusetts Bay Colony, British Colonial America")
        """
        places = [
            FlexiblePlace("Massachusetts Bay Colony, British Colonial America"),
            FlexiblePlace("British Colonial America"),
            FlexiblePlace("Lincoln, Massachusetts Bay Colony"),
            FlexiblePlace("Bucksport, Lincoln, Massachusetts Bay Colony"),
            FlexiblePlace("Lincoln, Massachusetts Bay Colony, British Colonial America"),
            FlexiblePlace("reallysuperlongcityname, reallysuperlongcountyname, reallysuperlongstatename, reallysuperlongcountryname"),
            FlexiblePlace("Belgium")
        ]
        result = FlexiblePlace.combine_flexible_places(places)
        self.assertEqual(str(result), "Bucksport, Lincoln, Massachusetts Bay Colony, British Colonial America")


if __name__ == "__main__":
    unittest.main()
