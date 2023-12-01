str_rep_nums = {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
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

def get_min_max_value(line):
    min_found, max_found = False, False
    for i in range(len(line)):
        for str_rep_num in str_rep_nums.keys():
            if line[i:].startswith(str_rep_num):
                if not min_found:
                    min_found = str_rep_num
                max_found = str_rep_num
                break
    return (min_found, max_found)

def num_mapper(str_rep_num):
    return str_rep_nums[str_rep_num]


def callibrator_parser(line):
    min_value, max_value = get_min_max_value(line)
    min_value = num_mapper(min_value)
    max_value = num_mapper(max_value)
    return min_value * 10 + max_value


def main():
    with open("input.txt", "r") as input_file:
        callibration_data = input_file.readlines()

    print(sum([callibrator_parser(line) for line in callibration_data]))


if __name__ == "__main__":
    main()
