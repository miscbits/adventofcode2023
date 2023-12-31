from collections import deque
from dataclasses import dataclass
from enum import Enum
import enum
import copy


class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    WEST = (0, -1)
    EAST = (0, 1)


@dataclass
class Beam:
    x: int
    y: int
    direction: Direction

    def move(self):
        match self.direction.value:
            case a, b:
                self.x += a
                self.y += b
        return self

    def pos(self):
        return (self.x, self.y)


def parse_input(input_file):
    with open(input_file) as mirror_map_file:
        return {(x, y): c
                for x, line in enumerate(mirror_map_file.read().split("\n"))
                for y, c in enumerate(line)}


def calculate_heat(mirror_map, initial_beam):
    beams = deque()

    beams.append(initial_beam)

    heated_points = set()
    visited_points = set()
    while beams and (beam := beams.pop()):
        if beam.pos() not in mirror_map:
            continue
        if (beam.pos(), *beam.direction.value) in visited_points:
            continue
        visited_points.add((beam.pos(), *beam.direction.value))
        heated_points.add(beam.pos())

        match (mirror_map[beam.pos()], beam.direction):
            case ("|", Direction.EAST) | ("|", Direction.WEST):
                beams.append(Beam(beam.x, beam.y, Direction.NORTH).move())
                beams.append(Beam(beam.x, beam.y, Direction.SOUTH).move())
            case ("-", Direction.NORTH) | ("-", Direction.SOUTH):
                beams.append(Beam(beam.x, beam.y, Direction.EAST).move())
                beams.append(Beam(beam.x, beam.y, Direction.WEST).move())
            case "/", direction:
                match direction:
                    case(Direction.NORTH):
                        beams.append(
                            Beam(beam.x, beam.y, Direction.EAST).move())
                    case(Direction.SOUTH):
                        beams.append(
                            Beam(beam.x, beam.y, Direction.WEST).move())
                    case(Direction.EAST):
                        beams.append(
                            Beam(beam.x, beam.y, Direction.NORTH).move())
                    case(Direction.WEST):
                        beams.append(
                            Beam(beam.x, beam.y, Direction.SOUTH).move())
            case "\\", direction:
                match direction:
                    case(Direction.NORTH):
                        beams.append(
                            Beam(beam.x, beam.y, Direction.WEST).move())
                    case(Direction.SOUTH):
                        beams.append(
                            Beam(beam.x, beam.y, Direction.EAST).move())
                    case(Direction.EAST):
                        beams.append(
                            Beam(beam.x, beam.y, Direction.SOUTH).move())
                    case(Direction.WEST):
                        beams.append(
                            Beam(beam.x, beam.y, Direction.NORTH).move())
            case _:
                beams.append(beam.move())

    return len(heated_points)


def part1():
    mirror_map = parse_input("../input.txt")
    return calculate_heat(mirror_map, Beam(0, 0, Direction.EAST))


def part2():
    mirror_map = parse_input("../input.txt")
    size = max([x[0] for x in mirror_map.keys()])
    max_found = 0
    for i in range(0, size + 1):
        max_found = max(max_found, calculate_heat(
            mirror_map, Beam(i, 0, Direction.EAST)))

        max_found = max(max_found, calculate_heat(
            mirror_map, Beam(i, size, Direction.WEST)))

        max_found = max(max_found, calculate_heat(
            mirror_map, Beam(0, i, Direction.SOUTH)))

        max_found = max(max_found, calculate_heat(
            mirror_map, Beam(size, i, Direction.NORTH)))
    return max_found


if __name__ == '__main__':
    print(part1())
    print(part2())
