from FlexiblePlace.src.FlexiblePlace import FlexiblePlace

class TestBasicFlexiblePlaceInitialization:
    def test_location_in_string(self):
        fp = FlexiblePlace("Walla Walla, Washington, United States")
        assert str(fp) == "Walla Walla, Washington, United States"

    def test_location_in_list(self):
        fp = FlexiblePlace(["Walla Walla", "Washington", "United States"])
        assert str(fp) == "Walla Walla, Washington, United States"

    def test_str_format(self):
        fp = FlexiblePlace("walla walla, waShiNGton, u.s.a.")
        assert str(fp) == "Walla Walla, Washington, U.S.A."

    def test_repr_format(self):
        fp1 = FlexiblePlace("Walla Walla, Washington, United States")
        assert repr(fp1) == ""
        fp2 = FlexiblePlace("Walla Walla, Washington, United States", "24")
        assert repr(fp2) == "24"

    def test_auto_fill(self):
        fp = FlexiblePlace("Walla Walla, Washington")
        assert str(fp) == "Walla Walla, Washington, United States"
