def callibrator_parser_ints(line):
    numbers = [x for x in line if x in "0123456789"]
    return int(numbers[0] + numbers[-1])


def getEarlyIndex(line):
    min_indexes = {
        x: line.index(x)
        for x in [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
        ]
        if x in line
    }
    min_index = len(line)
    min_value = "0"
    for k, v in min_indexes.items():
        if v <= min_index:
            min_index = v
            min_value = k
    return min_value


def getLatestIndex(line):
    search_vals = [
        "1"[::-1],
        "2"[::-1],
        "3"[::-1],
        "4"[::-1],
        "5"[::-1],
        "6"[::-1],
        "7"[::-1],
        "8"[::-1],
        "9"[::-1],
        "one"[::-1],
        "two"[::-1],
        "three"[::-1],
        "four"[::-1],
        "five"[::-1],
        "six"[::-1],
        "seven"[::-1],
        "eight"[::-1],
        "nine"[::-1],
    ]
    min_indexes = {x: line[::-1].index(x) for x in search_vals if x in line[::-1]}
    min_index = len(line)
    min_value = "0"
    for k, v in min_indexes.items():
        if v <= min_index:
            min_index = v
            min_value = k
    return min_value[::-1]


def num_mapper(str_rep_num):
    num_map = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    if str_rep_num in "0123456789":
        return int(str_rep_num)
    return num_map[str_rep_num]


def callibrator_parser_strings(line):
    min_value = num_mapper(getEarlyIndex(line))
    max_value = num_mapper(getLatestIndex(line))
    return min_value * 10 + max_value


def main():
    with open("input.txt", "r") as input_file:
        callibration_data = input_file.readlines()
    # print(sum([callibrator_parser_ints(line) for line in callibration_data]))
    print(sum([callibrator_parser_strings(line) for line in callibration_data]))


if __name__ == "__main__":
    main()
