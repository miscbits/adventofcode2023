import itertools


class Cosmos:
    """Object represent rows and columns of cosmos data"""

    def __init__(self, raw_input):
        super(Cosmos, self).__init__()
        self.raw_input = raw_input

        self.rows = []
        self.cols = []
        self.blank_rows = []
        self.blank_cols = []
        self.points = []
        for row in raw_input.split("\n"):
            self.rows.append(row)
        for c in self.rows[0]:
            self.cols.append("")
        for ri, r in enumerate(self.rows):
            for ci, c in enumerate(r):
                self.cols[ci] += c
                if c == "#":
                    self.points.append((ri, ci))
            if "#" not in r:
                self.blank_rows.append(ri)
        for ci, c in enumerate(self.cols):
            if "#" not in c:
                self.blank_cols.append(ci)

    def __str__(self):
        return (
            "rows:\n"
            + "\n".join(self.rows)
            + "\n"
            + "cols:\n"
            + "\n".join(self.cols)
            + "\n"
            + "blank_rows: "
            + ",".join([str(x) for x in self.blank_rows])
            + "\nblank_cols: "
            + ",".join([str(x) for x in self.blank_cols])
            + "\npoints: "
            + ",".join([str(x) for x in self.points])
        )

    def space_between_points(self, point_a, point_b, modifier=2):
        distance_x = abs(point_a[0] - point_b[0])
        distance_y = abs(point_a[1] - point_b[1])

        for x in range(min(point_a[0], point_b[0]), max(point_a[0], point_b[0])):
            if x in self.blank_rows:
                distance_x += modifier - 1

        for y in range(min(point_a[1], point_b[1]), max(point_a[1], point_b[1])):
            if y in self.blank_cols:
                distance_y += modifier - 1

        return distance_x + distance_y


def part_1():
    with open("../input.txt") as input_file:
        cosmos_data = input_file.read()
    cosmos = Cosmos(cosmos_data)

    # print(cosmos)

    total = 0
    for pair in itertools.combinations(cosmos.points, 2):
        total += cosmos.space_between_points(pair[0], pair[1])
    print(total)


def part_2():
    with open("../input.txt") as input_file:
        cosmos_data = input_file.read()
    cosmos = Cosmos(cosmos_data)

    # print(cosmos)

    total = 0
    for pair in itertools.combinations(cosmos.points, 2):
        total += cosmos.space_between_points(pair[0], pair[1], 1000000)
    print(total)


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
