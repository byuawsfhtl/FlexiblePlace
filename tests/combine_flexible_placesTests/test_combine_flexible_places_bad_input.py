from FlexiblePlace.src.FlexiblePlace import FlexiblePlace

combine_flexible_places = FlexiblePlace.combine_flexible_places

class TestCombineFlexiblePlacesBadInput:
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
        assert str(result) == "A, B, C, D, E"

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
        assert str(result) == "A, A, A, A"

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
        assert str(result) == "A, B, C"

    def test_void_input(self) -> None:
        """If data is different types of null, null is still returned"""
        places = [
            FlexiblePlace([]),
            FlexiblePlace(["",""]),
            FlexiblePlace(""),
            FlexiblePlace(" , ")
        ]
        result = combine_flexible_places(places)
        assert not result

    def test_bad_align(self) -> None:
        """Badly aligned data will create stange combination
        ("Orlando, Florida",
            "Florida, Utah, United States",
            returns "Orlando, Florida, Utah, United States")"""
        places = [
            FlexiblePlace("Orlando, Florida"),
            FlexiblePlace("Florida, Utah, United States")
        ]
        result = combine_flexible_places(places)
        assert str(result) == "Orlando, Florida, Utah, United States"

    def test_bad_align_by_auto_fill(self) -> None:
        """Badly aligned data (caused by autofill) will create stange combination
        ("Walla Walla, Washington",
         "Washington, United States",
         "Washington, Utah"
         returns "Walla Walla, Washington, Utah, United States")"""
        places = [
            FlexiblePlace("Walla Walla, Washington"),
            FlexiblePlace("Washington, United States"),
            FlexiblePlace("Washington, Utah")
        ]
        result = combine_flexible_places(places)
        assert str(result) == "Walla Walla, Washington, Utah, United States"


    def test_bad_order(self) -> None:
        """Badly ordered data still works
        ("A, B",
         "B, A",
         returns "A, B, A")"""
        places = [
            FlexiblePlace("A, B"),
            FlexiblePlace("B, A")
        ]
        result = combine_flexible_places(places)
        assert str(result) == "A, B, A"

    def test_misspelled_data(self) -> None:
            """Misspelled data is still combined correctly
            ("Walla Walla, Washingon",
             "Washington, Unided Sates",
             "United States"
             returns "Walla Walla, Washington, United States")"""
            places = [
                FlexiblePlace("Walla Walla, Washingon"),
                FlexiblePlace("Washington, Unided Sates"),
                FlexiblePlace("United States")
            ]
            result = combine_flexible_places(places)
            assert str(result) == "Walla Walla, Washington, United States"
