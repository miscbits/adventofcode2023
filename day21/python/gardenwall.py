from __future__ import annotations
from functools import cache
from dataclasses import dataclass, field
import itertools
from enum import Enum

Direction = Enum("Direction", ["UP", "DOWN","LEFT", "RIGHT"])

@dataclass
class Garden:
    starting_point: (int, int) = (-1,-1)
    blockers: [(int, int)] = field(default_factory=list)
    rows: [str] = field(default_factory=list)
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
def pos_move(pos, direction) -> (int, int):
    change = {
        Direction.UP: (-1,0),
        Direction.DOWN: (1,0),
        Direction.LEFT: (0,-1),
        Direction.RIGHT: (0,1),
    }[direction]

    return (pos[0] + change[0], pos[1] + change[1])

def part_1():
    with open('../input.txt') as input_file:
        garden = Garden.from_string(input_file.read())
    potentials = [garden.starting_point]


    @cache
    def expand(pos):
        directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        positions = (pos_move(p, d) for p, d in itertools.product([pos], directions))
        positions = (position for position in positions if position not in garden.blockers)
        # expanded = (position for position in (  if position not in garden.blockers and 0 <= position[0] < garden.col_len and 0<= position[1] < garden.row_len)
        return list(positions)
    
    for i in range(720):
        potentials = {position for position in itertools.chain(*[expand(p) for p in potentials])}

        print(i +1, len(potentials))

def find_coefficients(f1, f2, f3):
    f2 += -4*f1
    f3 += -9*f1
    f2 *= -.5
    f3 += 6 * f2
    f2 += -1.5*f3
    f1 += -1 * f3
    f1 += -1 * f2
    return (f1, f2, f3)

def part_2():
    with open('../input.txt') as input_file:
        garden = Garden.from_string(input_file.read())
    potentials = [garden.starting_point]


    @cache
    def expand(pos):
        directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        positions = (pos_move(p, d) for p, d in itertools.product([pos], directions))
        positions = (position for position in positions if position not in garden.blockers)
        # expanded = (position for position in (  if position not in garden.blockers and 0 <= position[0] < garden.col_len and 0<= position[1] < garden.row_len)
        return list(positions)

    odd_totals = []    
    for i in range((65 + 262 * 2) + 1):
        potentials = {position for position in itertools.chain(*[expand(p) for p in potentials])}
        if (i) % 262 == 65:
            odd_totals.append(len(potentials))
        print(i, len(potentials))

    a,b,c = find_coefficients(*odd_totals)

    steps = (26501365 - 65)/262

    total = a * steps**2 + b * steps + c

    print(total)

if __name__ == '__main__':
    part_2()