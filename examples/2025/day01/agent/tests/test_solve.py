import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from solve import solve


def reference(rotations):
    position, stops, passes = 50, 0, 0
    for direction, distance in rotations:
        for _ in range(distance):
            position = (position + (1 if direction == 'R' else -1)) % 100
            passes += position == 0
        stops += position == 0
    return stops, passes


class DayOneTests(unittest.TestCase):
    def test_own_small_example(self):
        text = 'R250\nL200\nR1\nL1\n'
        self.assertEqual(solve(text, 1), 3)
        self.assertEqual(solve(text, 2), 6)

    def test_leaving_zero_does_not_count_as_a_new_visit(self):
        self.assertEqual(solve('L50\nL1\nR1', 2), 2)

    def test_empty_and_crlf(self):
        self.assertEqual(solve('', 2), 0)
        self.assertEqual(solve('R50\r\n\r\nL100\r\n', 2), 2)

    def test_large_rotation_uses_constant_work(self):
        self.assertEqual(solve('R1000000000', 2), 10000000)

    def test_against_independent_click_by_click_simulation(self):
        randomizer = random.Random(202501)
        for _ in range(150):
            rotations = [(randomizer.choice('LR'), randomizer.randrange(400)) for _ in range(15)]
            text = '\n'.join(direction + str(distance) for direction, distance in rotations)
            expected = reference(rotations)
            self.assertEqual((solve(text, 1), solve(text, 2)), expected)

    def test_bad_commands_fail(self):
        for text in ['X3', 'R-1', 'Ltwo', 'R3 trailing']:
            with self.assertRaises(ValueError):
                solve(text, 1)


if __name__ == '__main__':
    unittest.main()
