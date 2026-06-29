import unittest
from src.flexible_place import FlexiblePlace


class TestCompareTwoPlaces(unittest.TestCase):
    """Test suite for FlexiblePlace.compare_two_places static method"""

    def test_null_returns_100(self):
        """Test: Null returns 100
        Input: FlexiblePlace(""), FlexiblePlace("")
        Output: 100
        """
        place1 = FlexiblePlace("")
        place2 = FlexiblePlace("")
        result = FlexiblePlace.compare_two_places(place1, place2)
        self.assertEqual(result, 100)

    def test_object_compared_with_null_returns_100(self):
        """Test: Object compared with null returns 100
        Input: FlexiblePlace("Paterson, Passaic, New Jersey, United States"), FlexiblePlace("")
        Output: 100
        """
        place1 = FlexiblePlace("Paterson, Passaic, New Jersey, United States")
        place2 = FlexiblePlace("")
        result = FlexiblePlace.compare_two_places(place1, place2)
        self.assertEqual(result, 100)

    def test_object_compared_with_null_returns_100_reverse_order(self):
        """Test: Null in first position, object in second position
        Input: FlexiblePlace(""), FlexiblePlace("Paterson, Passaic, New Jersey, United States")
        Output: 100
        """
        place1 = FlexiblePlace("")
        place2 = FlexiblePlace("Paterson, Passaic, New Jersey, United States")
        result = FlexiblePlace.compare_two_places(place1, place2)
        self.assertEqual(result, 100)

    def test_same_place_returns_100(self):
        """Test: Same place returns 100
        Input: FlexiblePlace("Belgium"), FlexiblePlace("Belgium")
        Output: 100
        """
        place1 = FlexiblePlace("Belgium")
        place2 = FlexiblePlace("Belgium")
        result = FlexiblePlace.compare_two_places(place1, place2)
        self.assertEqual(result, 100)

    def test_same_place_case_insensitive_returns_100(self):
        """Test: Place comparison should be case-insensitive
        Input: FlexiblePlace("belgium"), FlexiblePlace("Belgium")
        Output: 100
        """
        place1 = FlexiblePlace("belgium")
        place2 = FlexiblePlace("Belgium")
        result = FlexiblePlace.compare_two_places(place1, place2)
        self.assertEqual(result, 100)

    def test_specific_compared_with_less_specific_returns_100_case_1(self):
        """Test: Specific compared with less specific returns 100 (Case 1)
        Input: FlexiblePlace("Camden, New Jersey, United States"), FlexiblePlace("Camden, Camden, New Jersey, United States")
        Output: 100
        """
        place1 = FlexiblePlace("Camden, New Jersey, United States")
        place2 = FlexiblePlace("Camden, Camden, New Jersey, United States")
        result = FlexiblePlace.compare_two_places(place1, place2)
        self.assertEqual(result, 100)

    def test_specific_compared_with_less_specific_returns_100_case_2(self):
        """Test: Specific compared with less specific returns 100 (Case 2)
        Input: FlexiblePlace("No Croghan J*, New York, United States"), FlexiblePlace("New York, United States")
        Output: 100
        """
        place1 = FlexiblePlace("No Croghan J*, New York, United States")
        place2 = FlexiblePlace("New York, United States")
        result = FlexiblePlace.compare_two_places(place1, place2)
        self.assertEqual(result, 100)

    def test_specific_compared_with_less_specific_returns_100_case_3(self):
        """Test: Specific compared with less specific returns 100 (Case 3)
        Input: FlexiblePlace("New York, New York, United States"), FlexiblePlace("New York, United States")
        Output: 100
        """
        place1 = FlexiblePlace("New York, New York, United States")
        place2 = FlexiblePlace("New York, United States")
        result = FlexiblePlace.compare_two_places(place1, place2)
        self.assertEqual(result, 100)

    def test_whitespace_only_strings(self):
        """Test: Whitespace-only strings should be treated as null
        Input: FlexiblePlace("   "), FlexiblePlace("   ")
        """
        place1 = FlexiblePlace("   ")
        place2 = FlexiblePlace("   ")
        result = FlexiblePlace.compare_two_places(place1, place2)
        self.assertEqual(result, 100)


if __name__ == "__main__":
    unittest.main()
