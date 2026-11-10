"""AI-produced example: both counters in one pass, constant work per rotation."""
import argparse
import re
import sys


def counts(text):
    position, endpoints, crossings = 50, 0, 0
    for line in text.splitlines():
        command = line.strip()
        if not command:
            continue
        match = re.fullmatch(r'([LR])([0-9]+)', command)
        if not match:
            raise ValueError('Invalid rotation')
        direction, amount = match[1], int(match[2])
        if direction == 'R':
            crossings += (position + amount) // 100
            position = (position + amount) % 100
        else:
            crossings += (amount + (100 - position) % 100) // 100
            position = (position - amount) % 100
        endpoints += position == 0
    return endpoints, crossings


def solve(text, part):
    return counts(text)[part - 1]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--part', type=int, choices=(1, 2), required=True)
    args = parser.parse_args()
    try:
        print(solve(sys.stdin.read(), args.part))
    except ValueError as error:
        print(error, file=sys.stderr)
        raise SystemExit(2)
