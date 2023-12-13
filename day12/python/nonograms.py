import functools


class HotSpringSlice:
    """representation of a row of HotSpring data"""

    def __init__(self, str_rep):
        self.str_rep = str_rep

        parts = str_rep.split(" ")
        self.map = parts[0]
        self.splits = [int(i) for i in parts[1].split(",")]

    def __str__(self) -> str:
        return self.str_rep

    def __len__(self) -> int:
        return len(self.map)

    def min_length(self):
        return sum(self.splits) + len(self.splits) - 1


@functools.cache
def gen_options(hot_spring_map) -> [str]:
    def gen(rem_len, rem_splits):
        if len(rem_splits) == 0:
            yield "." * rem_len
            return

        a = rem_splits[0]
        rest = rem_splits[1:]
        after = sum(rest) + len(rest)

        for before in range(rem_len - after - a + 1):
            cand = "." * before + "#" * a + "."
            for opt in gen(rem_len - a - before - 1, rest):
                yield cand + opt

    return list(gen(len(hot_spring_map), hot_spring_map.splits))


def compare_options(broken_map, options):
    for option in options:
        if all((o == s or s == "?") for o, s in zip(option, broken_map.map)):
            yield option


def count_matches2(pattern, splits):
    @functools.cache
    def gen(rem_pattern, rem_len, rem_splits):
        if len(rem_splits) == 0:
            if all(c in ".?" for c in rem_pattern):
                return 1
            return 0

        a = rem_splits[0]
        rest = rem_splits[1:]
        after = sum(rest) + len(rest)

        count = 0

        for before in range(rem_len - after - a + 1):
            cand = "." * before + "#" * a + "."
            if all(c0 == c1 or c0 == "?" for c0, c1 in zip(rem_pattern, cand)):
                rest_pattern = rem_pattern[len(cand) :]
                count += gen(rest_pattern, rem_len - a - before - 1, rest)

        return count

    return gen(pattern, len(pattern), tuple(splits))


def part_1():
    with open("../input.txt") as input_file:
        hot_spring_map = [HotSpringSlice(h) for h in input_file.read().split("\n")]

    num_of_options = 0
    for h in hot_spring_map:
        possibles = list(compare_options(h, gen_options(h)))
        num_of_options += len(possibles)
    print(num_of_options)


def part_2():
    with open("../input.txt") as input_file:
        hot_spring_map = [HotSpringSlice(h) for h in input_file.read().split("\n")]

    num_of_options = 0
    for h in hot_spring_map:
        possibles = count_matches2(
            "?".join([h.map, h.map, h.map, h.map, h.map]), h.splits * 5
        )
        num_of_options += possibles
    print(num_of_options)


if __name__ == "__main__":
    part_2()
