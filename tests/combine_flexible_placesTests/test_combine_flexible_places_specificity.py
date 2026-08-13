from FlexiblePlace.src.FlexiblePlace import FlexiblePlace

combine_flexible_places = FlexiblePlace.combine_flexible_places

class TestCombineFlexiblePlacesSpecificity:
    """Specificity tests for FlexiblePlace.combine_flexible_places static method, to rigorously test combination algorithm"""

    def test_merge_partial_into_completed_location(self) -> None:
        """
        More specific replaces less specific if same location and ignores outlier
        ("New York, New York, United States",
         "New York, United States",
         "reallylongcityname, reallylongstatename, UnitedStates"
         returns "New York, New York, United States").
        """
        places = [
            FlexiblePlace("New York, New York, United States"),
            FlexiblePlace("New York, United States"),
            FlexiblePlace("reallylongcityname, reallylongstatename, UnitedStates")
        ]
        result = combine_flexible_places(places)
        assert str(result) == "New York, New York, United States"

    def test_combining_location_with_county_versus_not(self) -> None:
        """
        Combining location with county versus not with county
        ("Lawrence, Massachusetts, United States",
         "Lawrence, Essex, Massachusetts, United States"
        returns "Lawrence, Essex, Massachusetts, United States").
        """
        places = [
            FlexiblePlace("Lawrence, Massachusetts, United States"),
            FlexiblePlace("Lawrence, Essex, Massachusetts, United States")
        ]
        result = combine_flexible_places(places)
        assert str(result) == "Lawrence, Essex, Massachusetts, United States"

    def test_combine_two_partials_to_create_complete_location(self) -> None:
        """
        Combines the info of two imprecise locations, to create a more precise location. Ignores outlier
        ("Springfield, Sangamon, Illinois",
         "Springfield, Illinois, United States",
         "reallylongcityname, Sangamon, reallylongstatename, United States"
        returns "Springfield, Sangamon, Illinois, United States").
        """
        places = [
            FlexiblePlace("Springfield, Sangamon, Illinois"),
            FlexiblePlace("Springfield, Illinois, United States"),
            FlexiblePlace("reallylongcityname, Sangamon, Illinois, United States")
        ]
        result = combine_flexible_places(places)
        assert str(result) == "Springfield, Sangamon, Illinois, United States"

    def test_combine_three_partials_to_create_completed_location(self) -> None:
        """
        Correctly combines the info of three imprecise locations
        ("Sugarloaf Township, Pennsylvania, United States",
         "Luzerne, Pennsylvania",
         "Sugarloaf Township, Luzerne, Pennsylvania"
        returns "Sugarloaf Township, Luzerne, Pennsylvania, United States").
        """
        places = [
            FlexiblePlace("Sugarloaf Township, Pennsylvania, United States"),
            FlexiblePlace("Luzerne, Pennsylvania"),
            FlexiblePlace("Sugarloaf Township, Luzerne, Pennsylvania")
        ]
        result = combine_flexible_places(places)
        assert str(result) == "Sugarloaf Township, Luzerne, Pennsylvania, United States"

    def test_identifies_correct_city(self) -> None:
        """
        Intelligently determines which city is correct without a plurarlity
        ("badcity, badstate, badcountry",
         "Walla Walla, Washington",
         "Washington, United States",
         "College Place, Washington, badcountry",
         "United States"
         returns "Walla Walla, Washington, United States").
        """
        places = [
            FlexiblePlace("badcity, badstate, badcountry"),
            FlexiblePlace("Walla Walla, Washington", auto_fill = False),
            FlexiblePlace("Washington, United States"),
            FlexiblePlace("College Place, Washington, badcountry"),
            FlexiblePlace("United States")
        ]
        result = combine_flexible_places(places)
        assert str(result) == "Walla Walla, Washington, United States"

    def test_identifies_correct_state(self) -> None:
        """
        Correctly removes California as an outlier
        ("Orange, California",
         "Orange, Florida, U.S.A.",
         "Orlando, Orange, Florida"
         returns "Orlando, Orange, Florida, U.S.A.").
        """
        places = [
            FlexiblePlace("Orange, California", auto_fill = False),
            FlexiblePlace("Orange, Florida, U.S.A."),
            FlexiblePlace("Orlando, Orange, Florida", auto_fill = False)
        ]
        result = combine_flexible_places(places)
        assert str(result) == "Orlando, Orange, Florida, U.S.A."

    def test_identifies_correct_country(self) -> None:
        """
        Intelligently determines correct country without a plurality
        ("Paris, France",
         "Paris, Texas",
         "Texas, USA"
         returns "Paris, Texas, Usa").
        """
        places = [
            FlexiblePlace("Paris, France"),
            FlexiblePlace("Paris, Texas", auto_fill = False),
            FlexiblePlace("Texas, USA")
        ]
        result = combine_flexible_places(places)
        assert str(result) == "Paris, Texas, Usa"

    def test_duplicate_city_and_state_name(self) -> None:
        """
        Doesn't get confused by duplicate city and state names
        ("New York, incorrectstate, United States",
         "New York, United States",
         "New York, New York, United States"
         returns "New York, New York, United States").
        """
        places = [
            FlexiblePlace("New York, incorrectstate, United States"),
            FlexiblePlace("New York, United States"),
            FlexiblePlace("New York, New York, United States")
        ]
        result = combine_flexible_places(places)
        assert str(result) == "New York, New York, United States"

    def test_tie_break_by_string_length(self) -> None:
        """
        Chooses 'United States' as the country because it is the longer string
        ("Washington, D.C.",
         "Walla Walla, Washington",
         "Washington, United States"
         returns "Walla Walla, Washington, United States").
        """
        places = [
            FlexiblePlace("Washington, D.C."),
            FlexiblePlace("Walla Walla, Washington"),
            FlexiblePlace("Washington, United States")
        ]
        result = combine_flexible_places(places)
        assert str(result) == "Walla Walla, Washington, United States"

    def test_shrinks_combined_place_if_needed(self) -> None:
        """
        Combined place can be less specific than a given location if no consensus is found
        ("badcity, Washington, incorrectcountry",
         "incorrectcity, Washington, badcountry",
         "Washington, United States",
         "Washington, United States",
         returns "Washington, United States").
        """
        places = [
            FlexiblePlace("badcity, Washington, incorrectcountry"),
            FlexiblePlace("incorrectcity, Washington, badcountry"),
            FlexiblePlace("Washington, United States"),
            FlexiblePlace("Washington, United States")
        ]
        result = combine_flexible_places(places)
        assert str(result) == "Washington, United States"

    def test_works_with_large_input(self) -> None:
        """Can handle large input without trouble"""
        places = [FlexiblePlace("Walla Walla, Washington, United States")]
        for i in range(100):
            places.append(FlexiblePlace("Walla Walla"))
            places.append(FlexiblePlace("Washington"))
            places.append(FlexiblePlace("United States"))
        result = combine_flexible_places(places)
        assert str(result) == "Walla Walla, Washington, United States"

    def test_works_with_complex_input(self) -> None:
        """
        Properly combines several locations of varying specificity and excludes outliers
        ("Massachusetts Bay Colony, British Colonial America",
         "British Colonial America",
         "Lincoln, Massachusetts Bay Colony",
         "Bucksport, Lincoln, Massachusetts Bay Colony",
         "Lincoln, Massachusetts Bay Colony, British Colonial America",
         "reallysuperlongcityname, reallysuperlongcountyname, reallysuperlongstatename, reallysuperlongcountryname",
         "Belgium"
        returns "Bucksport, Lincoln, Massachusetts Bay Colony, British Colonial America").
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
        result = combine_flexible_places(places)
        assert str(result) == "Bucksport, Lincoln, Massachusetts Bay Colony, British Colonial America"
