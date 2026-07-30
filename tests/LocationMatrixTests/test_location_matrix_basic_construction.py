import pytest
from FlexiblePlace.src.LocationMatrix import LocationMatrix
from FlexiblePlace.src.FlexiblePlace import FlexiblePlace


class TestLocationMatrixBasicContstruction:
    """Tests that LocationMatrix objects are initialized with the correct size."""
    def test_empty_initialization(self) -> None:
        """An empty list of places should produce an empty matrix."""
        lm = LocationMatrix([])
        assert lm.row_count == 0
        assert lm.column_count == 0
        assert str(lm) == ""

    def test_single_row_initialization(self) -> None:
        """A single place should create one row with correct column count."""
        fp = FlexiblePlace("Belgium")
        lm = LocationMatrix([fp.get_location_components()])
        assert lm.row_count == 1
        assert lm.column_count == len(fp.get_location_components())
        # Verify matrix values correspond to the FlexiblePlace components
        for col, comp in enumerate(fp.get_location_components()):
            assert lm.matrix[0][col].value == comp

    def test_resize_and_padding(self) -> None:
        """Rows shorter than the longest place should be padded to column_count."""
        places = [
            ["c_country", "c_state", "c_city"],
            ["single_country"]
        ]
        lm = LocationMatrix(places)
        assert lm.row_count == 2
        assert lm.column_count == 3
        assert lm.matrix[1][0].value == "single_country"
        assert lm.matrix[1][1].value == ""
        assert lm.matrix[1][2].value == ""

    def test_example_str_output(self) -> None:
        """Verify the example output formatting from the prompt matches expected spacing."""
        places = [
            FlexiblePlace("Washington, United States", auto_fill=False),
            FlexiblePlace("Walla Walla, Washingon", auto_fill=False),
            FlexiblePlace("Walla Walla, Wasington, United Sates", auto_fill=False),
        ]
        lm = LocationMatrix([p.get_location_components() for p in places])
        expected = (
            "| united sates  | wasington  | walla walla |\n"
            "| united states | washington |             |\n"
            "|               | washingon  | walla walla |"
        )
        assert str(lm) == expected
