
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


compare_places = FlexiblePlace.compare_places

class TestCompareTwoPlacesCloseMatch:
    """Test for low scoring matches for FlexiblePlace.compare_places static method."""

    def test_different_countries(self) -> None:
        """Different countries (but otherwise agreeing info) should return 80 or higher."""
        place1 = FlexiblePlace("Richmond, Victoria, Australia")
        place2 = FlexiblePlace("Richmond, Victoria, Canada")
        result = compare_places(place1, place2)
        assert result >= 80

    def test_major_misspelled(self) -> None:
        """Same place but with major misspelled components should return 80 or higher."""
        place1 = FlexiblePlace("Walla Walla, Washington, United States")
        place2 = FlexiblePlace("Wahla Wahla, Worshingn, Yuneyded Stayts")
        result = compare_places(place1, place2)
        assert result >= 80    

    def test_minor_misspelled(self) -> None:
        """Same place but with minor misspelled components should return 90 or higher."""
        place1 = FlexiblePlace("Walla Walla, Washington, United States")
        place2 = FlexiblePlace("Wala Wala, Washingon, United Sates")
        result = compare_places(place1, place2)
        assert result >= 90
