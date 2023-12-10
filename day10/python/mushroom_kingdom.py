from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Map:
    pipes: [[Pipe]]
    current_pos: (int, int) = (0, 0)

    def from_string(schema: str) -> Map:
        schema_lines = schema.split("\n")
        map = Map([])
        for line in schema_lines:
            map.pipes.append([Pipe.from_string(x) for x in line])
            if "S" in line:
                map.current_pos = (
                    schema.index(line) // (len(line)),
                    line.index("S"),
                )
        return map

    def move_up(self) -> Map:
        self.current_pos = (self.current_pos[0] - 1, self.current_pos[1])
        return self

    def move_down(self) -> Map:
        self.current_pos = (self.current_pos[0] + 1, self.current_pos[1])
        return self

    def move_left(self) -> Map:
        self.current_pos = (self.current_pos[0], self.current_pos[1] - 1)
        return self

    def move_right(self) -> Map:
        self.current_pos = (self.current_pos[0], self.current_pos[1] + 1)
        return self

    def get_pipe(self, pos: (int, int)) -> Pipe:
        if (
            pos[0] < 0
            or pos[1] < 0
            or pos[0] >= len(self.pipes)
            or pos[1] >= len(self.pipes[0])
        ):
            return Pipe()
        return self.pipes[pos[0]][pos[1]]

    def get_current_pipe(self):
        return self.get_pipe(self.current_pos)

    def get_top_pipe(self):
        return self.get_pipe((self.current_pos[0] - 1, self.current_pos[1]))

    def get_right_pipe(self):
        return self.get_pipe((self.current_pos[0], self.current_pos[1] + 1))

    def get_bottom_pipe(self):
        return self.get_pipe((self.current_pos[0] + 1, self.current_pos[1]))

    def get_left_pipe(self):
        return self.get_pipe((self.current_pos[0], self.current_pos[1] - 1))

    def can_move_up(self):
        if self.get_current_pipe().has_top and self.current_pos[0] > 0:
            return self.get_top_pipe().has_bottom

    def can_move_right(self):
        if self.get_current_pipe().has_right and self.current_pos[1] < len(
            self.pipes[0]
        ):
            return self.get_right_pipe().has_left

    def can_move_down(self):
        if self.get_current_pipe().has_bottom and self.current_pos[0] < len(self.pipes):
            return self.get_bottom_pipe().has_top

    def can_move_left(self):
        if self.get_current_pipe().has_left and self.current_pos[1] > 0:
            return self.get_left_pipe().has_right

    def current_space_is_start(self) -> bool:
        return self.get_pipe(self.current_pos()).is_start


@dataclass
class Pipe:
    has_left: bool = False
    has_right: bool = False
    has_top: bool = False
    has_bottom: bool = False
    is_start: bool = False

    def valid_pipe(self) -> bool:
        return (
            len(
                [
                    x
                    for x in [
                        self.has_left,
                        self.has_right,
                        self.has_top,
                        self.has_bottom,
                    ]
                    if x
                ]
            )
            == 2
            or self.is_start
        )

    @staticmethod
    def from_string(pipe_string: str) -> Pipe:
        match pipe_string:
            case "|":
                return Pipe(has_top=True, has_bottom=True)
            case "-":
                return Pipe(has_left=True, has_right=True)
            case "L":
                return Pipe(has_top=True, has_right=True)
            case "J":
                return Pipe(has_top=True, has_left=True)
            case "7":
                return Pipe(has_left=True, has_bottom=True)
            case "F":
                return Pipe(has_bottom=True, has_right=True)
            case "S":
                return Pipe(True, True, True, True, True)
        return Pipe()


def part_1(map: Map) -> int:
    map_length = len(get_loop_coords(map))
    return map_length // 2


def is_point_inside_loop(point, loop):
    x, y = point
    count = 0
    for i in range(len(loop)):
        x1, y1 = loop[i]
        x2, y2 = loop[(i + 1) % len(loop)]  # Wrap around for the last point
        if ((y1 <= y < y2) or (y2 <= y < y1)) and (x < max(x1, x2)):
            if y1 != y2:
                intersection = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                if x < intersection:
                    count += 1
            else:
                count += 1
    return count % 2 == 1


def get_loop_coords(map: Map) -> {int, int}:
    # move clockwise around loop
    loop_points: [(int, int)] = []
    if map.can_move_right():
        map.move_right()
        previous_move = "right"
    elif map.can_move_down():
        map.move_down()
        previous_move = "down"
    elif map.can_move_up():
        map.move_up()
        previous_move = "up"
    else:
        # start should have two possible moves
        raise Exception("invalid map")
    loop_points.append((map.current_pos[0], map.current_pos[1]))

    while not map.get_current_pipe().is_start:
        if map.can_move_right() and previous_move != "left":
            map.move_right()
            previous_move = "right"
        elif map.can_move_down() and previous_move != "up":
            map.move_down()
            previous_move = "down"
        elif map.can_move_left() and previous_move != "right":
            map.move_left()
            previous_move = "left"
        elif map.can_move_up() and previous_move != "down":
            map.move_up()
            previous_move = "up"
        else:
            raise Exception("dead end")
        loop_points.append((map.current_pos[0], map.current_pos[1]))

    return loop_points


def part_2(map: Map) -> int:
    loop_coords = get_loop_coords(map)

    potential_points_in_polygon = []

    for point_x in range(len(map.pipes)):
        for point_y in range(len(map.pipes[0])):
            potential_point = point_x, point_y
            if potential_point not in loop_coords:
                potential_points_in_polygon.append(potential_point)

    points_in_polygon_count = 0
    for point in potential_points_in_polygon:
        if is_point_inside_loop(point, loop_coords):
            points_in_polygon_count += 1
    return points_in_polygon_count


def test_moves():
    map = Map([[Pipe(has_bottom=True)], [Pipe(has_top=True)]], (0, 0))
    assert map.can_move_down()
    map = Map([[Pipe(has_bottom=True)], [Pipe(has_top=True)]], (1, 0))
    assert map.can_move_up()
    map = Map([[Pipe(has_right=True), Pipe(has_left=True)]], (0, 0))
    assert map.can_move_right()
    map = Map([[Pipe(has_right=True), Pipe(has_left=True)]], (0, 1))
    assert map.can_move_left()


if __name__ == "__main__":
    test_moves()
    with open("../input.txt") as input_file:
        map = Map.from_string(input_file.read())
    print(part_1(map))
    print(part_2(map))
