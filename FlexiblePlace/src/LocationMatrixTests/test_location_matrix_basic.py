import unittest
from FlexiblePlace.src.LocationMatrix import LocationMatrix
from FlexiblePlace.src.FlexiblePlace import FlexiblePlace


class TestLocationMatrixBasic(unittest.TestCase):
    def test_empty_initialization(self):
        """An empty list of places should produce an empty matrix."""
        lm = LocationMatrix([])
        self.assertEqual(lm.row_count, 0)
        self.assertEqual(lm.column_count, 0)
        self.assertEqual(str(lm), "")

    def test_single_row_initialization(self):
        """A single place should create one row with correct column count."""
        fp = FlexiblePlace("Belgium")
        lm = LocationMatrix([fp.get_location_components()])
        self.assertEqual(lm.row_count, 1)
        self.assertEqual(lm.column_count, len(fp.get_location_components()))
        # Verify matrix values correspond to the FlexiblePlace components
        for col, comp in enumerate(fp.get_location_components()):
            self.assertEqual(lm.matrix[0][col].value, comp)

    def test_resize_and_padding(self):
        """Rows shorter than the longest place should be padded to column_count."""
        # first row has 3 components, second row only 1
        places = [
            ["c_country", "c_state", "c_city"],
            ["single_country"]
        ]
        lm = LocationMatrix(places)
        self.assertEqual(lm.row_count, 2)
        self.assertEqual(lm.column_count, 3)
        # shorter row should have placeholder components in remaining columns (value == "")
        self.assertEqual(lm.matrix[1][0].value, "single_country")
        self.assertEqual(lm.matrix[1][1].value, "")
        self.assertEqual(lm.matrix[1][2].value, "")

    def test_example_str_output(self):
        """Verify the example output formatting from the prompt matches expected spacing."""
        places = [
            FlexiblePlace("Washington, United States"),
            FlexiblePlace("Walla Walla, Washingon"),
            FlexiblePlace("Walla Walla, Washingon, United States"),
        ]
        # Use get_location_components() because LocationMatrix expects list[list[str]]
        lm = LocationMatrix([p.get_location_components() for p in places])

        # Expected layout from the example in your prompt (lowercase values)
        expected = (
            "| united states | washington |             |\n"
            "|               | washington | walla walla |\n"
            "| united states | washington | walla walla |"
        )
        self.assertEqual(str(lm), expected)


if __name__ == "__main__":
    unittest.main()