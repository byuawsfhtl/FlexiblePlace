
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


combine_flexible_places = FlexiblePlace.combine_flexible_places


class TestCombineFlexiblePlacesBasic:
    """Basic tests for FlexiblePlace.combine_flexible_places static method"""

    def test_null_returns_null(self) -> None:
        """Null returns null."""
        places = []
        result = combine_flexible_places(places)
        assert not result

    def test_single_object_returns_same_object(self) -> None:
        """Single object returns the same object."""
        places = [FlexiblePlace("Belgium")]
        result = combine_flexible_places(places)
        assert str(result) == "Belgium"

    def test_duplicate_objects_return_same_object(self) -> None:
        """Duplicate objects return same object
        ("Belgium" and "Belgium" returns "Belgium")."""
        places = [FlexiblePlace("Belgium"), FlexiblePlace("Belgium")]
        result = combine_flexible_places(places)
        assert str(result) == "Belgium"

    def test_indecision_yields_longest_string(self) -> None:
        """Indecision yields longest string
        ("Paris" and "Belgium" returns "Belgium")."""
        places = [FlexiblePlace("Paris"), FlexiblePlace("Belgium")]
        result = combine_flexible_places(places)
        assert str(result) == "Belgium"

    def test_tie_yields_first(self) -> None:
        """Tie in string length yields first
        ("Egypt" and "Japan" returns "Egypt")."""
        places = [FlexiblePlace("Egypt"), FlexiblePlace("Japan")]
        result = combine_flexible_places(places)
        assert str(result) == "Egypt"