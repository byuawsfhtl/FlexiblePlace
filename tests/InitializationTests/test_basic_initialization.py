
from pathlib import Path
from pyscripttestutils import PyScriptTestRunner
from FlexiblePlace.src.FlexiblePlace import FlexiblePlace

runner = PyScriptTestRunner(
    Path(__file__).resolve().parents[2] / "FlexiblePlaceTS" / "dist" / "test_bridge.js",
    deserializer=lambda d: FlexiblePlace(d["location"], d.get("placeDescription", ""), auto_fill=False),
)

runner.add_method(FlexiblePlace.__str__, "FlexiblePlace.toString", executor=lambda d: str(d))
runner.add_method(FlexiblePlace.__repr__, "FlexiblePlace.__repr__", executor=lambda d: repr(d))
runner.add_method(FlexiblePlace.__eq__, "FlexiblePlace.__eq__", executor=lambda d: d[0] == d[1])
runner.add_method(FlexiblePlace.__bool__, "FlexiblePlace.__bool__", executor=lambda d: bool(d))
runner.add_method(FlexiblePlace.get_location, "FlexiblePlace.get_location", executor=lambda d: d.get_location())
runner.add_method(FlexiblePlace.compare, "FlexiblePlace.compare", executor=lambda d: d[0].compare(d[1]))
runner.add_method(FlexiblePlace.compare_places, "FlexiblePlace.compare_places", executor=lambda d: FlexiblePlace.compare_places(d[0], d[1]))
runner.add_method(FlexiblePlace.combine_flexible_places, "FlexiblePlace.combine_flexible_places", executor=lambda d: FlexiblePlace.combine_flexible_places(d[0]))


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
