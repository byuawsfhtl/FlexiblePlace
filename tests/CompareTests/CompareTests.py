from FlexiblePlace.src.Compare import Compare
from unittest.mock import patch
import pytest

class TestAlignComponents:
    def test_creates_LocationMatrix_object(self) -> None:
        """Tests that the align_locations uses the LocationMatrix to align locations.
        
        The align functionality is already rigorously tested in the LocationMatrix tests, so this test
        only checks that the align_components method utilizes the LocationMatrix to align components"""
        with patch("FlexiblePlace.src.Compare.LocationMatrix") as mock_location_matrix:
            place_a = ["a", "b"]
            place_b = ["b", "c"]
            expected = [["a", "b", ""], ["", "b", "c"]]
            mock_location_matrix.return_value.get_locations.return_value = expected
            actual = Compare.align_components(place_a, place_b)
            mock_location_matrix.assert_called_once_with([place_a, place_b])
            assert expected == actual

class TestCompareEachComponent:
    @staticmethod
    def mock_ratio(place_a, place_b) -> float:
        """A mock of the fuzz.ratio method that hard codes outputs for specific inputs."""
        if place_a == "walla walla" and place_b == "walla walla":
            return 100.0
        elif place_a == "united states" and place_b == "usa":
            return 30.0
        else:
            return 0
        
    def test_compare_each_location(self) -> None:
        """Tests that the method correctly pairs up and compares the components"""
        with patch("FlexiblePlace.src.Compare.fuzz") as mock_fuzz:
            mock_fuzz.ratio = TestCompareEachComponent.mock_ratio
            place_a = ["walla walla", "washington", "united states"]
            place_b = ["walla walla", "wrongstate", "usa"]
            expected = [100.0, 0.0, 30.0]
            assert Compare.compare_each_component([place_a, place_b]) == expected

class TestAdjustScores:
    """Tests that the scores are adjusted correctly, assuming that first score represents the most specific component (e.g. city)"""
    def test_scores_all_zero(self) -> None:
        """Tests that the scores adjust correctly when all are 0"""
        scores_list = [0.0, 0.0, 0.0, 0.0]
        expected_list = [64.64466, 50.0, 29.28932, 0.0]
        Compare.adjust_scores(scores_list)
        for actual, expected in zip(scores_list, expected_list):
            assert pytest.approx(expected) == pytest.approx(actual)

    def test_scores_all_ten(self) -> None:
        """Tests that the scores adjust correctly when all are 10"""
        scores_list = [10.0, 10.0, 10.0, 10.0]
        expected_list = [68.18019, 55.0, 36.36039, 10.0]
        Compare.adjust_scores(scores_list)
        for actual, expected in zip(scores_list, expected_list):
            assert pytest.approx(expected) == pytest.approx(actual)

    def test_scores_all_fifty(self) -> None:
        """Tests that the scores adjust correctly when all are 50"""
        scores_list = [50.0, 50.0, 50.0, 50.0]
        expected_list = [82.32233, 75.0, 64.64466, 50.0]
        Compare.adjust_scores(scores_list)
        for actual, expected in zip(scores_list, expected_list):
            assert pytest.approx(expected) == pytest.approx(actual)

    def test_scores_all_hundred(self) -> None:
        """Tests that the scores adjust correctly when all are 100"""
        scores_list = [100.0, 100.0, 100.0, 100.0]
        expected_list = [100.0, 100.0, 100.0, 100.0]
        Compare.adjust_scores(scores_list)
        for actual, expected in zip(scores_list, expected_list):
            assert pytest.approx(expected) == pytest.approx(actual)

    def test_scores_mix(self) -> None:
        """Tests that the scores adjust correctly when there are mixed scores"""
        scores_list = [0.0, 30.0, 50.0, 65.0]
        expected_list = [64.64466, 65.0, 64.64466, 65.0]
        Compare.adjust_scores(scores_list)
        for actual, expected in zip(scores_list, expected_list):
            assert pytest.approx(expected) == pytest.approx(actual)