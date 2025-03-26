import unittest
from utils import normalize_support

class TestUtils(unittest.TestCase):
    def test_normalize_support(self):
        support = {"A": 30, "B": 70}
        normalize_support(support)
        self.assertAlmostEqual(support["A"], 30.0)
        self.assertAlmostEqual(support["B"], 70.0)

    def test_normalize_support_zero_total(self):
        support = {"A": 0, "B": 0}
        normalize_support(support)
        self.assertAlmostEqual(support["A"], 50.0)
        self.assertAlmostEqual(support["B"], 50.0)

if __name__ == "__main__":
    unittest.main()
