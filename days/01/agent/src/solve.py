"""Solve AoC 2025 day 1 from rotations on stdin."""

import argparse
import re
import sys


def counts(lines):
    position = 50
    endpoints = crossings = 0
    for number, line in enumerate(lines, 1):
        command = line.strip()
        if not command:
            continue
        match = re.fullmatch(r"([LR])([0-9]+)", command)
        if not match:
            raise ValueError(f"Invalid rotation on line {number}")
        direction, distance = match[1], int(match[2])
        turns, remainder = divmod(distance, 100)
        # Each full turn reaches zero once, regardless of the start position.
        crossings += turns
        if direction == "R":
            crossings += position + remainder >= 100
            position = (position + remainder) % 100
        else:
            # Leaving zero is not a new visit to zero.
            crossings += 0 < position <= remainder
            position = (position - remainder) % 100
        endpoints += position == 0
    return endpoints, crossings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--part", type=int, required=True, choices=(1, 2))
    args = parser.parse_args()
    try:
        print(counts(sys.stdin)[args.part - 1])
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
