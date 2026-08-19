from FlexiblePlace.src.Compare import Compare
import pytest

class TestAdjustScores:
    def test_adjust_scores(self) -> None:
        """Tests that the scores are adjusted correctly"""
        scores_list = [10.0, 10.0, 10.0, 10.0]
        expected_list = [68.18019, 55.0, 36.36039, 10.0]
        Compare.adjust_scores(scores_list)
        for actual, expected in zip(scores_list, expected_list):
            assert pytest.approx(expected) == pytest.approx(actual)