from itertools import pairwise


def predictnext(diffs):
    val = 0
    while(any(diffs)):
        val += diffs[-1]

        diffs = [val2 - val1 for val1, val2 in pairwise(diffs)]
    return val

def predictprevious(diffs):
    starts = []
    while(any(diffs)):
        starts.insert(0, diffs[0])

        diffs = [val2 - val1 for val1, val2 in pairwise(diffs)]

    val = 0
    for i in starts:
        val = i - val
    return val

def part_1(input_file_path="../test.txt"):
    with open(input_file_path) as measurements_file:
        measurements = [[int(i) for i in line.split(" ")] for line in measurements_file.read().split("\n")]

    total = 0
    for current_series in measurements:
        total += predictnext(current_series)
    return total

def part_2(input_file_path="../test.txt"):
    with open(input_file_path) as measurements_file:
        measurements = [[int(i) for i in line.split(" ")] for line in measurements_file.read().split("\n")]

    total = 0
    for current_series in measurements:
        total += predictprevious(current_series)
    return total

if __name__ == '__main__':
    print(part_1("../input.txt"))
    print(part_2("../input.txt"))
