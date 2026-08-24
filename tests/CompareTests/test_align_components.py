from FlexiblePlace.src.Compare import Compare
from unittest.mock import patch

class TestAlignComponents:
    def test_creates_LocationMatrix_object(self) -> None:
        """Tests that the align_locations uses the LocationMatrix to align locations"""
        with patch("FlexiblePlace.src.Compare.LocationMatrix") as mock_location_matrix:
            place_a = ["a", "b"]
            place_b = ["b", "c"]
            expected = [["a", "b", ""], ["", "b", "c"]]
            mock_location_matrix.return_value.get_locations.return_value = expected
            actual = Compare.align_components(place_a, place_b)
            mock_location_matrix.assert_called_once_with([place_a, place_b])
            assert expected == actual
