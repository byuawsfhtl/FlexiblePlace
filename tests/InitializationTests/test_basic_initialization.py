from FlexiblePlace.src.FlexiblePlace import FlexiblePlace

class TestBasicFlexiblePlaceInitialization:
    """
    Test suite for basic FlexiblePlace initialization functionality.
    
    Tests various initialization methods including string input, list input,
    string formatting, repr formatting, and automatic country fill.
    """
    
    def test_location_in_string(self):
        """
        Test FlexiblePlace initialization with a comma-separated string.
        
        Verifies that a location string in the format "City, State, Country"
        is properly initialized and returned as a formatted string.
        """
        fp = FlexiblePlace("Walla Walla, Washington, United States")
        assert str(fp) == "Walla Walla, Washington, United States"

    def test_location_in_list(self):
        """
        Test FlexiblePlace initialization with a list of location components.
        
        Verifies that a location provided as a list ["City", "State", "Country"]
        is properly initialized and formatted as a comma-separated string.
        """
        fp = FlexiblePlace(["Walla Walla", "Washington", "United States"])
        assert str(fp) == "Walla Walla, Washington, United States"

    def test_str_format(self):
        """
        Test string formatting and case normalization.
        
        Verifies that location strings are properly title-cased and that
        abbreviations like "u.s.a." are correctly formatted to "U.S.A."
        """
        fp = FlexiblePlace("walla walla, waShiNGton, u.s.a.")
        assert str(fp) == "Walla Walla, Washington, U.S.A."

    def test_repr_format(self):
        """
        Test repr formatting with and without an ID parameter.
        
        Verifies that repr returns an empty string when no ID is provided,
        and returns the ID string when one is provided during initialization.
        """
        fp1 = FlexiblePlace("Walla Walla, Washington, United States")
        assert repr(fp1) == ""
        fp2 = FlexiblePlace("Walla Walla, Washington, United States", "24")
        assert repr(fp2) == "24"

    def test_auto_fill(self):
        """
        Test automatic country field population.
        
        Verifies that when a location is provided with only city and state,
        the country is automatically populated based on the state information.
        """
        fp = FlexiblePlace("Walla Walla, Washington")
        assert str(fp) == "Walla Walla, Washington, United States"
