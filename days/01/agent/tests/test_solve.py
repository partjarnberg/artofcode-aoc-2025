"""Independent simulation and our own test data; no personal AoC input."""

import importlib.util
from pathlib import Path
import random
import subprocess
import sys
import unittest

SOLVER = Path(__file__).resolve().parents[1] / "src" / "solve.py"
spec = importlib.util.spec_from_file_location("day01", SOLVER)
day01 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(day01)


def simulate(commands):
    position = 50
    endpoints = crossings = 0
    for command in commands:
        step = 1 if command[0] == "R" else -1
        for _ in range(int(command[1:])):
            position = (position + step) % 100
            crossings += position == 0
        endpoints += position == 0
    return endpoints, crossings


class RotationTests(unittest.TestCase):
    def test_multiple_turns(self):
        self.assertEqual(day01.counts(["R250", "L200", "R1", "L1"]), (3, 6))

    def test_leaving_zero(self):
        self.assertEqual(day01.counts(["L50", "L1", "R1"]), (2, 2))

    def test_zero_distance_and_full_turns(self):
        self.assertEqual(day01.counts(["R50", "L0", "L100", "R100"]), (4, 3))

    def test_large_rotations(self):
        for direction in "LR":
            self.assertEqual(day01.counts([direction + "1000000000000"]), (0, 10000000000))

    def test_empty_and_crlf(self):
        self.assertEqual(day01.counts([]), (0, 0))
        self.assertEqual(day01.counts(["\r\n", " L50\r\n"]), (1, 1))

    def test_every_position_near_turn_boundaries(self):
        for position in range(100):
            for direction in "LR":
                for amount in (0, 1, 49, 50, 99, 100, 101, 199, 200, 201):
                    commands = [f"R{(position - 50) % 100}", f"{direction}{amount}"]
                    self.assertEqual(day01.counts(commands), simulate(commands), commands)

    def test_random_sequences(self):
        rng = random.Random(202501)
        for _ in range(200):
            commands = [f"{rng.choice('LR')}{rng.randrange(601)}" for _ in range(20)]
            self.assertEqual(day01.counts(commands), simulate(commands))

    def test_invalid_input(self):
        for command in ("X3", "R-1", "Ltwo", "R3 trailing", "R", "R１"):
            with self.subTest(command=command), self.assertRaisesRegex(ValueError, "line 2"):
                day01.counts(["R1", command])

    def test_cli(self):
        for part, expected in ((1, "3\n"), (2, "6\n")):
            result = subprocess.run([sys.executable, str(SOLVER), "--part", str(part)],
                input="R250\nL200\nR1\nL1\n", text=True, capture_output=True)
            self.assertEqual((result.returncode, result.stdout, result.stderr), (0, expected, ""))

    def test_cli_errors(self):
        result = subprocess.run([sys.executable, str(SOLVER), "--part", "1"],
            input="R-1\n", text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("Invalid rotation on line 1", result.stderr)


if __name__ == "__main__":
    unittest.main()
