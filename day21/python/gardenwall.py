from __future__ import annotations
from dataclasses import dataclass, field
from functools import cache
import itertools
from enum import Enum

Direction = Enum("Direction", ["UP", "DOWN", "LEFT", "RIGHT"])


@dataclass
class Garden:
    starting_point: tuple[int, int] = (-1, -1)
    blockers: list[tuple[int, int]] = field(default_factory=list)
    rows: list[str] = field(default_factory=list)
    row_len: int = 0
    col_len: int = 0

    @staticmethod
    def from_string(schema: str) -> Garden:
        garden = Garden()
        garden.starting_point = (-1, -1)
        for ri, line in enumerate(schema.split("\n")):
            garden.rows.append(line)
            for ci, c in enumerate(line):
                if c == "#":
                    garden.blockers.append((ci, ri))
                if c == "S":
                    garden.starting_point = (ci, ri)
        garden.col_len = ri + 1
        garden.row_len = ci + 1

        return garden


@cache
def pos_move(pos, direction) -> tuple[int, int]:
    change = {
        Direction.UP: (-1, 0),
        Direction.DOWN: (1, 0),
        Direction.LEFT: (0, -1),
        Direction.RIGHT: (0, 1),
    }[direction]

    return (pos[0] + change[0], pos[1] + change[1])


def part_1():
    with open('../input.txt') as input_file:
        garden = Garden.from_string(input_file.read())
    potentials = [garden.starting_point]

    @cache
    def expand(pos):
        directions = [Direction.UP, Direction.DOWN,
                      Direction.LEFT, Direction.RIGHT]
        positions = (pos_move(p, d)
                     for p, d in itertools.product([pos], directions))
        positions = (
            position for position in positions
            if position not in garden.blockers
        )
        return list(positions)

    for i in range(64):
        potentials = {position for position in itertools.chain(
            *[expand(p) for p in potentials])}

        print(i + 1, len(potentials))


def find_coefficients(x, y, z):
    y += -4*x
    z += -9*x
    y *= -0.5
    z += 6*y
    y += -1.5*z
    x += -1 * z
    x += -1 * y
    return (x, y, z)


def part_2():
    with open('../input.txt') as input_file:
        garden = Garden.from_string(input_file.read())
    potentials = [garden.starting_point]

    @cache
    def expand(pos):
        directions = [Direction.UP, Direction.DOWN,
                      Direction.LEFT, Direction.RIGHT]
        positions = (pos_move(pos, d) for d in directions)
        positions = (position for position in positions if (
            position[0] % garden.col_len, position[1] % garden.row_len)
            not in garden.blockers)
        return list(positions)

    odd_totals = []
    for i in range(1, 5000):
        potentials = {position for position in itertools.chain(
            *[expand(p) for p in potentials])}
        if (i) % 262 == 0:
            odd_totals.append(len(potentials))
            if len(odd_totals) == 3:
                break
        print(i+1, len(potentials))

    print(odd_totals)
    a, b, c = find_coefficients(*odd_totals)
    print(a, b, c)

    steps = (26501365)/262
    total = a * steps**2 + b * steps + c
    print(total)


if __name__ == '__main__':
    part_2()
