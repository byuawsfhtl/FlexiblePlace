# import unittest
# from FlexiblePlace.src.FlexiblePlace import FlexiblePlace, combine_flexible_places


# class TestCombineFlexiblePlaces(unittest.TestCase):
#     """Test suite for FlexiblePlace.combine_flexible_places static method."""

#     def test_null_returns_null(self) -> None:
#         """Null returns null."""
#         places = []
#         result = combine_flexible_places(places)
#         self.assertIsNone(result)

#     def test_single_object_returns_same_object(self) -> None:
#         """Single object returns the same object."""
#         places = [FlexiblePlace("Belgium")]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "Belgium")

#     def test_duplicate_objects_return_same_object(self) -> None:
#         """
#         Duplicate objects return same object
#         ("Belgium" and "Belgium" returns "Belgium").
#         """
#         places = [FlexiblePlace("Belgium"), FlexiblePlace("Belgium")]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "Belgium")

#     def test_indecision_yields_longest_string(self) -> None:
#         """
#         Indecision yields longest string
#         ("Paris" and "Belgium" returns "Belgium").
#         """
#         places = [FlexiblePlace("Paris"), FlexiblePlace("Belgium")]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "Belgium")

#     def test_tie_yields_first(self) -> None:
#         """
#         Tie in string length yields first
#         ("Melgium" and "Belgium" returns "Melgium").
#         """
#         places = [FlexiblePlace("Melgium"), FlexiblePlace("Belgium")]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "Melgium")

#     def test_more_specific_replaces_less_specific_new_jersey(self) -> None:
#         """
#         More specific replaces less specific if same location and ignores outlier
#         ("Camden, New Jersey",
#          "Camden, Camden, New Jersey, United States", and
#          "reallylongcityname, reallylongcountyname, reallylongstatename, reallylongcountryname"
#          returns "Camden, Camden, New Jersey, United States").
#         """
#         places = [FlexiblePlace("Camden, New Jersey"), FlexiblePlace("Camden, Camden, New Jersey, United States"), FlexiblePlace("reallylongcityname, reallylongcountyname, reallylongstatename, reallylongcountryname")]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "Camden, Camden, New Jersey, United States")

#     def test_more_specific_replaces_less_specific_new_york(self) -> None:
#         """
#         More specific replaces less specific if same location and ignores outlier
#         ("New York, New York, United States",
#          "New York, United States", and
#          "reallylongcityname, reallylongstatename, UnitedStates"
#          returns "New York, New York, United States").
#         """
#         places = [
#             FlexiblePlace("New York, New York, United States"),
#             FlexiblePlace("New York, United States"),
#             FlexiblePlace("reallylongcityname, reallylongstatename, UnitedStates")
#         ]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "New York, New York, United States")

#     def test_combining_location_with_county_versus_not(self) -> None:
#         """
#         Combining location with county versus not with county
#         ("Lawrence, Massachusetts, United States",
#          "Lawrence, Essex, Massachusetts, United States"
#         returns "Lawrence, Essex, Massachusetts, United States").
#         """
#         places = [
#             FlexiblePlace("Lawrence, Massachusetts, United States"),
#             FlexiblePlace("Lawrence, Essex, Massachusetts, United States")
#         ]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "Lawrence, Essex, Massachusetts, United States")

#     def test_combining_location_with_county_to_make_more_specific_new_york(self) -> None:
#         """
#         Combining location with county versus not with county to create more specific location
#         ("Buffalo, New York, United States",
#          "Buffalo, Erie, New York"
#         returns "Buffalo, Erie, New York, United States").
#         """
#         places = [
#             FlexiblePlace("Buffalo, New York, United States"),
#             FlexiblePlace("Buffalo, Erie, New York")
#         ]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "Buffalo, Erie, New York, United States")

#     def test_combining_location_with_county_to_make_more_specific_illinois(self) -> None:
#         """
#         Combining location with county to create more specific location and ignores outlier
#         ("Springfield, Sangamon, Illinois",
#          "Springfield, Illinois, United States",
#          "reallylongcityname, Sangamon, Illinois, United States"
#         returns "Springfield, Sangamon, Illinois, United States").
#         """
#         places = [
#             FlexiblePlace("Springfield, Sangamon, Illinois"),
#             FlexiblePlace("Springfield, Illinois, United States"),
#             FlexiblePlace("reallylongcityname, Sangamon, Illinois, United States")
#         ]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "Springfield, Sangamon, Illinois, United States")

#     def test_correctly_matches_abbreviations_philadelphia(self) -> None:
#         """
#         Correctly matches abbreviations
#         ("Phila, Pennsylvania, United States",
#          "Philadelphia, Pennsylvania"
#         returns "Philadelphia, Pennsylvania, United States").
#         """
#         places = [
#             FlexiblePlace("Phila, Pennsylvania, United States"),
#             FlexiblePlace("Philadelphia, Pennsylvania")
#         ]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "Philadelphia, Pennsylvania, United States")

#     def test_correctly_matches_abbreviations_township(self) -> None:
#         """
#         Correctly matches abbreviations
#         ("Elder Twp, Pennsylvania, United States",
#          "Elder Township, Cambria, Pennsylvania"
#         returns "Elder Township, Cambria, Pennsylvania, United States").
#         """
#         places = [
#             FlexiblePlace("Elder Twp, Pennsylvania, United States"),
#             FlexiblePlace("Elder Township, Cambria, Pennsylvania")
#         ]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "Elder Township, Cambria, Pennsylvania, United States")

#     def test_correctly_matches_abbreviations_ignores_outliers(self) -> None:
#         """
#         Correctly matches abbreviations and ignores outliers
#         ("Elder Twp, Pennsylvania, United States",
#          "Elder Township, Cambria, Pennsylvania",
#          "reallylongcityname, Pennsylvania, United States"
#          returns "Elder Township, Cambria, Pennsylvania, United States").
#         """
#         places = [
#             FlexiblePlace("Elder Twp, Pennsylvania, United States"),
#             FlexiblePlace("Elder Township, Cambria, Pennsylvania"),
#             FlexiblePlace("reallylongcityname, Pennsylvania, United States")
#         ]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "Elder Township, Cambria, Pennsylvania, United States")

#     def test_correctly_matches_abbreviations_philadelphia_monthly_meeting(self) -> None:
#         """
#         Correctly matches abbreviations with more specific data
#         ("Phila, Pennsylvania, United States"),
#          "Philadelphia Monthly Meeting, Philadelphia, Philadelphia, Pennsylvania"
#          returns "Philadelphia Monthly Meeting, Philadelphia, Philadelphia, Pennsylvania, United States").
#         """
#         places = [
#             FlexiblePlace("Phila, Pennsylvania, United States"),
#             FlexiblePlace("Philadelphia Monthly Meeting, Philadelphia, Philadelphia, Pennsylvania")
#         ]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "Philadelphia Monthly Meeting, Philadelphia, Philadelphia, Pennsylvania, United States")

#     def test_combines_data_from_incomplete_but_matching_sources(self) -> None:
#         """
#         Combines data from incomplete, but matching, sources
#         ("Sugarloaf Township, Pennsylvania, United States",
#          "Luzerne, Pennsylvania",
#          "Sugarloaf Township, Luzerne, Pennsylvania"
#         returns "Sugarloaf Township, Luzerne, Pennsylvania, United States").
#         """
#         places = [
#             FlexiblePlace("Sugarloaf Township, Pennsylvania, United States"),
#             FlexiblePlace("Luzerne, Pennsylvania"),
#             FlexiblePlace("Sugarloaf Township, Luzerne, Pennsylvania")
#         ]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "Sugarloaf Township, Luzerne, Pennsylvania, United States")

#     def test_disambiguates_multiple_locations_paris_texas(self) -> None:
#         """
#         Matches coinsiding places and removes outlier
#         ("Paris, France",
#          "Paris, Texas",
#          "Texas, United States"
#          returns "Paris, Texas, United States").
#         """
#         places = [
#             FlexiblePlace("Paris, France"),
#             FlexiblePlace("Paris, Texas"),
#             FlexiblePlace("Texas, United States")
#         ]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "Paris, Texas, United States")

#     def test_disambiguates_multiple_locations_new_york(self) -> None:
#         """
#         Matches coinsiding places and removes outlier
#         ("New York, Iowa, United States",
#          "New York, United States",
#          "New York, New York, United States"
#          returns "New York, New York, United States").
#         """
#         places = [
#             FlexiblePlace("New York, Iowa, United States"),
#             FlexiblePlace("New York, United States"),
#             FlexiblePlace("New York, New York, United States")
#         ]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "New York, New York, United States")


#     def test_disambiguates_multiple_locations_walla_walla(self) -> None:
#         """
#         Matches coinsiding places and removes outlier
#         ("Washington, Utah",
#          "Walla Walla, Washington",
#          "Washington, United States"
#          returns "Walla Walla, Washington, United States").
#         """
#         places = [
#             FlexiblePlace("Washington, Utah"),
#             FlexiblePlace("Walla Walla, Washington"),
#             FlexiblePlace("Washington, United States")
#         ]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "Walla Walla, Washington, United States")

#     def test_works_with_large_input_washington(self) -> None:
#         """
#         Disambiguates multiple locations
#         ("United States",
#          "Belgium",
#          "Washington, Utah",
#          "Walla Walla, Washington",
#          "Washington, United States"
#          returns "Walla Walla, Washington, United States").
#         """
#         places = [
#             FlexiblePlace("United States"),
#             FlexiblePlace("Belgium"),
#             FlexiblePlace("Washington, Utah"),
#             FlexiblePlace("Walla Walla, Washington"),
#             FlexiblePlace("Washington, United States")
#         ]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "Walla Walla, Washington, United States")

#     def test_works_with_a_large_input_massachusetts(self) -> None:
#         """
#         Works with a ton of inputs at once
#         ("Massachusetts Bay Colony, British Colonial America",
#          "British Colonial America",
#          "Lincoln, Massachusetts Bay Colony",
#          "Bucksport, Lincoln, Massachusetts Bay Colony",
#          "Lincoln, Massachusetts Bay Colony, British Colonial America",
#          "reallysuperlongcityname, reallysuperlongcountyname, reallysuperlongstatename, reallysuperlongcountryname",
#          "Belgium"
#         returns "Bucksport, Lincoln, Massachusetts Bay Colony, British Colonial America").
#         """
#         places = [
#             FlexiblePlace("Massachusetts Bay Colony, British Colonial America"),
#             FlexiblePlace("British Colonial America"),
#             FlexiblePlace("Lincoln, Massachusetts Bay Colony"),
#             FlexiblePlace("Bucksport, Lincoln, Massachusetts Bay Colony"),
#             FlexiblePlace("Lincoln, Massachusetts Bay Colony, British Colonial America"),
#             FlexiblePlace("reallysuperlongcityname, reallysuperlongcountyname, reallysuperlongstatename, reallysuperlongcountryname"),
#             FlexiblePlace("Belgium")
#         ]
#         result = combine_flexible_places(places)
#         self.assertEqual(str(result), "Bucksport, Lincoln, Massachusetts Bay Colony, British Colonial America")


# if __name__ == "__main__":
#     unittest.main()
