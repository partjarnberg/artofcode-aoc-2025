"""Teaching example: count arrivals at zero without expanding every turn."""
import argparse
import re
import sys


def solve(text, part):
    position = 50
    answer = 0
    for number, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        if not re.fullmatch(r'[LR][0-9]+', line):
            raise ValueError(f'Invalid rotation on line {number}')
        direction, distance = line[0], int(line[1:])
        if part == 2:
            first_zero = (100 - position) if direction == 'R' else (position or 100)
            if distance >= first_zero:
                answer += 1 + (distance - first_zero) // 100
        position = (position + (distance if direction == 'R' else -distance)) % 100
        if part == 1 and position == 0:
            answer += 1
    return answer


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--part', type=int, choices=(1, 2), required=True)
    args = parser.parse_args()
    try:
        print(solve(sys.stdin.read(), args.part))
    except ValueError as error:
        print(error, file=sys.stderr)
        raise SystemExit(2)
