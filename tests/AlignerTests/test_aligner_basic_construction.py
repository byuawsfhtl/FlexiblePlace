from FlexiblePlace.src.Aligner import Aligner

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
runner.add_method(Aligner.__str__, "Aligner.__str__", executor=lambda d: str(d))
runner.add_method(Aligner.__bool__, "Aligner.__bool__", executor=lambda d: bool(d))
runner.add_method(Aligner.get_locations, "Aligner.get_locations", executor=lambda d: d.get_locations())



class TestAlignerBasicContstruction:
    """Tests that Aligner objects are initialized with the correct size."""
    def test_empty_initialization(self) -> None:
        """An empty list of places should produce an empty matrix."""
        aligner = Aligner([])
        assert aligner.row_count == 0
        assert aligner.column_count == 0
        assert str(aligner) == ""    

    def test_single_row_initialization(self) -> None:
        """A single place should create one row with correct column count."""
        fp = FlexiblePlace("Belgium")
        aligner = Aligner([fp.get_location()])
        assert aligner.row_count == 1
        assert aligner.column_count == len(fp.get_location())
        # Verify matrix values correspond to the FlexiblePlace components
        for col, comp in enumerate(fp.get_location()):
            assert aligner.matrix[0][col].value == comp

    def test_resize_and_padding(self) -> None:
        """Rows shorter than the longest place should be padded to column_count."""
        places = [
            ["c_country", "c_state", "c_city"],
            ["single_country"]
        ]
        aligner = Aligner(places)
        assert aligner.row_count == 2
        assert aligner.column_count == 3
        
    def test_example_str_output(self) -> None:
        """Verify the example output formatting from the prompt matches expected spacing."""
        places = [
            FlexiblePlace("Washington, United States", auto_fill=False),
            FlexiblePlace("Walla Walla, Washingon", auto_fill=False),
            FlexiblePlace("Walla Walla, Wasington, United Sates", auto_fill=False),
        ]
        aligner = Aligner([p.location for p in places])
        expected = (
            "| walla walla | wasington  | united sates  |\n"
            "|             | washington | united states |\n"
            "| walla walla | washingon  |               |"
        )
        assert str(aligner) == expected

    def test_get_locations(self) -> None:
        """Tests that the get_locations method works"""
        places = [
            FlexiblePlace("Washington, United States", auto_fill=False),
            FlexiblePlace("Walla Walla, Washingon", auto_fill=False),
            FlexiblePlace("Walla Walla, Wasington, United Sates", auto_fill=False),
        ]
        aligner = Aligner([p.get_location() for p in places])
        expected = [
            ["walla walla", "wasington", "united sates"],
            ["", "washington", "united states"],
            ["walla walla", "washingon", ""]
        ]
        assert aligner.get_locations() == expected