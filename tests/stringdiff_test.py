from unittest import TestCase
from enia_translator import stringdiff


class ScoreTest(TestCase):

    def test_match_equal(self):
        self.assertEqual(stringdiff.score('asdf', 'asdf'), 1)

    def test_mismatch_cases(self):
        self.assertEqual(stringdiff.score('asdf', 'ASDF'), 0)

    def test_match_equal_ignoring_case(self):
        self.assertEqual(
            stringdiff.score('asdf', 'ASDF', case_sensitive=False),
            1,
        )

    def test_score_kitten_sitting(self):
        self.assertEqual(stringdiff.score('kitten', 'sitting'), 4/7)

    def test_score_weekdays(self):
        self.assertEqual(stringdiff.score('Saturday', 'Sunday'), 5/8)
