from FlexiblePlace.src.FlexiblePlace import FlexiblePlace

class TestBasicFlexiblePlaceInitialization:
    """Test suite for basic FlexiblePlace initialization functionality."""
    
    def test_location_in_string(self):
        """Test FlexiblePlace initialization with a comma-separated string."""
        fp = FlexiblePlace("Walla Walla, Washington, United States")
        assert str(fp) == "Walla Walla, Washington, United States"

    def test_location_in_list(self):
        """Test FlexiblePlace initialization with a list of location components."""
        fp = FlexiblePlace(["Walla Walla", "Washington", "United States"])
        assert str(fp) == "Walla Walla, Washington, United States"

    def test_str_format(self):
        """Test string formatting and case normalization."""
        fp = FlexiblePlace("walla walla, waShiNGton, u.s.a.")
        assert str(fp) == "Walla Walla, Washington, U.S.A."

    def test_repr_format(self):
        """Test repr formatting with and without a place_description parameter."""
        fp1 = FlexiblePlace("Walla Walla, Washington, United States")
        assert repr(fp1) == ""
        fp2 = FlexiblePlace("Walla Walla, Washington, United States", "24")
        assert repr(fp2) == "24"

    def test_auto_fill(self):
        """Test automatic country field population."""
        fp = FlexiblePlace("Walla Walla, Washington")
        assert str(fp) == "Walla Walla, Washington, United States"
