import unittest
from bowling_game import BowlingGame

class BowlingGameTests(unittest.TestCase):
    def setUp(self):
        self.g = BowlingGame()

    def roll_many(self, n, pins):
        for _ in range(n):
            self.g.roll(pins)

    def test_all_gutters(self):
        self.roll_many(20, 0)
        self.assertEqual(self.g.score(), 0)

    def test_all_ones(self):
        self.roll_many(20, 1)
        self.assertEqual(self.g.score(), 20)

    def test_single_spare_followed_by_three(self):
        self.g.roll(5); self.g.roll(5)  # spare
        self.g.roll(3)
        self.roll_many(17, 0)
        self.assertEqual(self.g.score(), 16)

    def test_single_strike_followed_by_three_and_four(self):
        self.g.roll(10)  # strike
        self.g.roll(3); self.g.roll(4)
        self.roll_many(16, 0)
        self.assertEqual(self.g.score(), 24)

    def test_perfect_game(self):
        self.roll_many(12, 10)
        self.assertEqual(self.g.score(), 300)

    def test_all_spares(self):
        self.roll_many(21, 5)
        self.assertEqual(self.g.score(), 150)

    def test_regular_game_no_marks(self):
        rolls = [3,4, 2,5, 1,6, 4,2, 8,1, 7,1, 5,3, 2,3, 4,3, 2,6]
        for p in rolls:
            self.g.roll(p)
        self.assertEqual(self.g.score(), 72)

    def test_invalid_roll_value(self):
        with self.assertRaises(ValueError):
            self.g.roll(11)
        with self.assertRaises(ValueError):
            self.g.roll(-1)
        with self.assertRaises(ValueError):
            self.g.roll(3.5)

if __name__ == "__main__":
    unittest.main()
