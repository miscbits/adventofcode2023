import functools


@functools.cache
def math_the_math(top, length):
    total = 0
    for i in range(length):
        total += top - i
    return total


@functools.cache
def calulate_load(beam: str):
    total = 0
    for i, c in enumerate(beam[::-1]):
        if c == "0":
            total += i + 1
    return total


class IcePuzzle:
    """docstring for IcePuzzle It looks very similar to yesterdays..."""

    def __init__(self, raw_input):
        self.raw_input = raw_input
        self.rows = []
        self.cols = []
        for row in raw_input.split("\n"):
            self.rows.append(row.replace("O", "0").replace(".", "1"))
            self.bin_rows = 0
        for c in self.rows[0]:
            self.cols.append("")
        for ri, r in enumerate(self.rows):
            for ci, c in enumerate(r):
                self.cols[ci] += c

    def max_north_load(self):
        total_max_load = 0
        for col in self.cols:
            barriers = col.split("#")
            top = len(col)
            for barrier in barriers:
                total_max_load += math_the_math(top, barrier.count("0"))
                top -= len(barrier) + 1  # essentially get the index of the next section
        return total_max_load

    def calculate_north_load(self):
        return sum([calulate_load(col) for col in self.cols])

    def tilt(self):
        for i, col in enumerate(self.cols):
            barriers = col.split("#")
            self.cols[i] = "#".join(["".join(sorted(barrier)) for barrier in barriers])

    def rotate_cw(self):
        self.rows = [col[::-1] for col in self.cols]
        self.cols = ["" for _ in self.cols]
        for ri, r in enumerate(self.rows):
            for ci, c in enumerate(r):
                self.cols[ci] += c

    def cycle(self):
        self.tilt()  # move north
        self.rotate_cw()
        self.tilt()  # move west
        self.rotate_cw()
        self.tilt()  # move south
        self.rotate_cw()
        self.tilt()  # move east
        self.rotate_cw()  # reorient_north

    def __str__(self):
        return "\n".join(self.rows).replace("0", "O").replace("1", ".")


def get_ice_slider(input_file: str) -> IcePuzzle:
    with open(input_file) as input_file:
        return IcePuzzle(input_file.read())


def part_1():
    ice_slider = get_ice_slider("../input.txt")
    print(ice_slider.max_north_load())


def part_2():
    ice_slider = get_ice_slider("../input.txt")
    for i in range(1000):
        ice_slider.cycle()
    print(ice_slider.calculate_north_load())


if __name__ == "__main__":
    part_2()
