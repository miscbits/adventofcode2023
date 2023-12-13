import functools


def is_power_of_2(num: int) -> bool:
    num = abs(num)
    if num == 0:
        return False
    while num != 1:
        if num % 2 != 0:
            return False
        num = num // 2
    return True


@functools.cache
def get_bin_rep(schema: str) -> int:
    total = 0
    for i, c in enumerate(schema):
        if c == "#":
            total += 1 << (len(schema) - i - 1)
    return total


def _fuzzy_find_reflection_index(schema: [str]) -> int:
    reverse_schema = schema[::-1]
    for i in range(len(schema) // 2):
        bin_reps = (
            get_bin_rep("".join(schema[0 : i + 1])),
            get_bin_rep("".join(schema[i + 1 : (i + 1) * 2][::-1])),
        )
        if is_power_of_2(bin_reps[0] ^ bin_reps[1]):
            return i + 1

        bin_reps = (
            get_bin_rep("".join(reverse_schema[0 : i + 1])),
            get_bin_rep("".join(reverse_schema[i + 1 : (i + 1) * 2][::-1])),
        )
        if is_power_of_2(bin_reps[0] ^ bin_reps[1]):
            return len(schema) - (i + 1)
    # no reflection found
    return 0


def _find_reflection_index(schema: [str]) -> int:
    reverse_schema = schema[::-1]
    for i in range(len(schema) // 2):
        bin_reps = (
            get_bin_rep("".join(schema[0 : i + 1])),
            get_bin_rep("".join(schema[i + 1 : (i + 1) * 2][::-1])),
        )
        if bin_reps[0] == bin_reps[1]:
            return i + 1

        bin_reps = (
            get_bin_rep("".join(reverse_schema[0 : i + 1])),
            get_bin_rep("".join(reverse_schema[i + 1 : (i + 1) * 2][::-1])),
        )
        if bin_reps[0] == bin_reps[1]:
            return len(schema) - (i + 1)
    # no reflection found
    return 0


class MirrorPool:
    """docstring for MirrorPool"""

    def __init__(self, raw_input):
        self.raw_input = raw_input
        self.rows = []
        self.cols = []
        for row in raw_input.split("\n"):
            self.rows.append(row)
            self.bin_rows = 0
        for c in self.rows[0]:
            self.cols.append("")
        for ri, r in enumerate(self.rows):
            for ci, c in enumerate(r):
                self.cols[ci] += c

    def find_reflection_value(self) -> int:
        return (_find_reflection_index(self.rows) * 100) + _find_reflection_index(
            self.cols
        )

    def fuzzy_find_reflection_value(self) -> int:
        return (
            _fuzzy_find_reflection_index(self.rows) * 100
        ) + _fuzzy_find_reflection_index(self.cols)


def get_reflections(input_file: str) -> [MirrorPool]:
    with open(input_file) as input_file:
        for schema in input_file.read().split("\n\n"):
            yield MirrorPool(schema)


def part_1():
    total = 0
    for pool in get_reflections("../test.txt"):
        reflection_value = pool.find_reflection_value()
        total += reflection_value

    print(total)


def part_2():
    total = 0
    for pool in get_reflections("../input.txt"):
        reflection_value = pool.fuzzy_find_reflection_value()
        if reflection_value == 0:
            print(pool.raw_input)
        total += reflection_value

    print(total)


part_2()
