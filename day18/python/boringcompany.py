# -*- coding: utf-8 -*-

from dataclasses import dataclass

directions = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (1, 0),
    "0": (0, 1),
    "2": (0, -1),
    "3": (-1, 0),
    "1": (1, 0),
}


@dataclass(order=True)
class Segment:
    vector_origin: (int, int)
    vector_end: (int, int)
    color_code: str


def calc_area(shape):
    area = 0.0
    for segment in shape:
        area += vec_product(segment.vector_end, segment.vector_origin)
    return abs(area) / 2.0


def vec_product(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]


def picks_theorem(area, boundary_points):
    return (2 * area - boundary_points + 2) / 2


def part_1():
    with open("../input.txt") as input_file:
        lines = [line.split(" ") for line in input_file.read().split("\n")]
    current_position = (0, 0)
    shape = []
    boundary_points = 0
    for line in lines:
        end_position = (
            current_position[0] + directions[line[0]][0] * int(line[1]),
            current_position[1] + directions[line[0]][1] * int(line[1]),
        )
        segment = Segment(current_position, end_position, line[2][1:-1])
        shape.append(segment)
        boundary_points += abs(segment.vector_origin[1] - segment.vector_end[1])
        boundary_points += abs(segment.vector_origin[0] - segment.vector_end[0])
        current_position = end_position
    area = calc_area(shape)
    print(picks_theorem(area, boundary_points) + boundary_points)


def part_2():
    with open("../input.txt") as input_file:
        lines = [line.split(" ") for line in input_file.read().split("\n")]
    current_position = (0, 0)
    shape = []
    boundary_points = 0
    for line in lines:
        color_code = line[2][2:-1]
        direction = directions[color_code[-1]]
        distance = int(f"0x{color_code[:5]}", 16)
        end_position = (
            current_position[0] + direction[0] * distance,
            current_position[1] + direction[1] * distance,
        )
        segment = Segment(current_position, end_position, line[2][1:-1])
        shape.append(segment)
        boundary_points += abs(segment.vector_origin[1] - segment.vector_end[1])
        boundary_points += abs(segment.vector_origin[0] - segment.vector_end[0])
        current_position = end_position
    area = calc_area(shape)
    print(picks_theorem(area, boundary_points) + boundary_points)


def point_in_boundary(point, shape):
    for segment in shape:
        v1, v2 = segment.vector_origin, segment.vector_end
        x1, x2 = min(v1[0], v2[0]), max(v1[0], v2[0])
        y1, y2 = min(v1[0], v2[0]), max(v1[0], v2[0])
        if x1 <= point[0] <= x2 and y1 <= point[1] <= y2:
            return True
    return False


def add_points(p1, p2):
    return (p1[0] + p2[0]), (p1[1] + p2[1])


def get_point_from_shape(coord, shape):
    if 0 <= coord[0] < len(shape) and 0 <= coord[1] < len(shape[0]):
        return shape[coord[0]][coord[1]]
    return " "


def get_point_type(coord, boundary_points):
    directions = [
        add_points(coord, (0, 1)),  # right
        add_points(coord, (0, -1)),  # left
        add_points(coord, (-1, 0)),  # up
        add_points(coord, (1, 0)),  # down
    ]
    # possible_shapes = ["┌", "┐", "└", "┘", "─", "│"]
    above, below, left, right = (
        get_point_from_shape(directions[2], boundary_points),
        get_point_from_shape(directions[3], boundary_points),
        get_point_from_shape(directions[1], boundary_points),
        get_point_from_shape(directions[0], boundary_points),
    )

    if above == "*" and below == "*":
        return "|"
    if right == "*" and left == "*":
        return "-"
    if right == "*" and below == "*":
        return "F"
    if left == "*" and below == "*":
        return "7"
    if above == "*" and right == "*":
        return "L"
    if above == "*" and left == "*":
        return "J"
    return "*"


def visualize_part_1():
    with open("../input.txt") as input_file:
        lines = [line.split(" ") for line in input_file.read().split("\n")]
    corners = [(0, 0)]
    boundary_points = set()
    for line in lines:
        end_position = (
            corners[-1][0] + directions[line[0]][0] * int(line[1]),
            corners[-1][1] + directions[line[0]][1] * int(line[1]),
        )
        x1, x2 = (
            min(corners[-1][0], end_position[0]),
            max(corners[-1][0], end_position[0]),
        )
        y1, y2 = (
            min(corners[-1][1], end_position[1]),
            max(corners[-1][1], end_position[1]),
        )
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                boundary_points.add((x, y))
        corners.append(end_position)
    min_x = min([s[0] for s in corners])
    max_x = max([s[0] for s in corners])
    min_y = min([s[1] for s in corners])
    max_y = max([s[1] for s in corners])

    boundaries_as_astericks = []
    for x in range(min_x, max_x + 1):
        line = []
        for y in range(min_y, max_y + 1):
            if (x, y) in boundary_points:
                line.append("*")
            else:
                line.append(" ")
        boundaries_as_astericks.append(line)

    boundaries_as_pipes = [
        [" " for _ in range(len(boundaries_as_astericks[0]))]
        for _ in range(len(boundaries_as_astericks))
    ]
    for x in range(len(boundaries_as_astericks)):
        for y in range(len(boundaries_as_astericks[0])):
            point_char = get_point_from_shape((x, y), boundaries_as_astericks)
            if point_char == "*":
                boundaries_as_pipes[x][y] = get_point_type(
                    (x, y), boundaries_as_astericks
                )

    positive_inverse = {"F": "J", "L": "7"}
    for line in boundaries_as_pipes:
        fill = False
        ignore = False
        ignore_char = ""
        for i, c in enumerate(line[:-1]):
            if ignore:
                if c in "FJ7L":
                    ignore = False
                    if c == positive_inverse.get(ignore_char, "0"):
                        fill = not fill
            if c in "FJ7L":
                ignore = True
                ignore_char = c
                fill = not fill
                continue
            if c == "-":
                line[i] = ignore_char
                continue
            if c in "|FJ7L":
                fill = not fill
                continue
            elif fill:
                line[i] = "#"

    with open("output.txt", "w") as output_file:
        for line in boundaries_as_pipes:
            output_file.write("".join(line) + "\n")


if __name__ == "__main__":
    visualize_part_1()
