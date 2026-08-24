from FlexiblePlace.src.Compare import Compare
import pytest

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