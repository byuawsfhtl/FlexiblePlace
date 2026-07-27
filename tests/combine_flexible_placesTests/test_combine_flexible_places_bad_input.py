import unittest
from FlexiblePlace.src.FlexiblePlace import FlexiblePlace, combine_flexible_places


class TestCombineFlexiblePlacesBadInput(unittest.TestCase):
    """Bad input tests for FlexiblePlace.combine_flexible_places static method"""

    def test_many_linked_components(self) -> None:
        """Checks if several layers of linked components causes problems.
        ("A,B,C",
         "A,B,D",
         "A,C",
         "B,D",
         "A,B,C,D",
         "A,D",
         "A,E",
         "C,D,E"
         returns "A,B,C,D,E")"""
        places = [
            FlexiblePlace("A, B, C"),
            FlexiblePlace("A, B, D"),
            FlexiblePlace("A, C"),
            FlexiblePlace("B, D"),
            FlexiblePlace("A, B, C, D"),
            FlexiblePlace("A, D"),
            FlexiblePlace("A, E"),
            FlexiblePlace("C, D, E")
        ]
        result = combine_flexible_places(places)
        self.assertEqual(str(result), "A, B, C, D, E")

    def test_identical_components(self) -> None:
            """Checks multiple identical components are handled correctly.
            ("A,A,A,A",
             "A,A,A",
             "A,A",
             "A",
             "A,B,C,D",
             returns "A,A,A,A")"""
            places = [
                FlexiblePlace("A, A, A, A"),
                FlexiblePlace("A, A, A"),
                FlexiblePlace("A, A"),
                FlexiblePlace("A"),
                FlexiblePlace("A, B, C, D"),
            ]
            result = combine_flexible_places(places)
            self.assertEqual(str(result), "A, A, A, A")

    def test_no_correlation(self) -> None:
            """If data does not correlate, first is returned
            ("A,B,C",
             "D,E,F",
             "H,I,J"
             returns "A,B,C")"""
            places = [
                FlexiblePlace("A, B, C"),
                FlexiblePlace("D, E, F"),
                FlexiblePlace("H, I, J"),
            ]
            result = combine_flexible_places(places)
            self.assertEqual(str(result), "A, B, C")

    def test_void_input(self) -> None:
                """If data is different types of null, null is still returned"""
                places = [
                    FlexiblePlace([]),
                    FlexiblePlace(["",""]),
                    FlexiblePlace("")
                ]
                result = combine_flexible_places(places)
                self.assertFalse(result)



if __name__ == "__main__":
    unittest.main()
