def test_part_1():
    scores = part_1("../test.txt")
    assert scores == 13


def test_part_2():
    scores = part_2("../test.txt")
    assert scores == 30


def part_1(input_file_path: str) -> int:
    scratch_cards = read_scratcher_data(input_file_path)
    return sum([calculate_points_naiive(card) for card in scratch_cards.values()])


def part_2(input_file_path: str) -> int:
    scratch_cards = read_scratcher_data(input_file_path)
    num_of_cards = {k: 1 for k in scratch_cards.keys()}
    points = 0
    for k, v in scratch_cards.items():
        num_of_wins = calculate_points_total(v)
        for i in range(k, k + num_of_wins):
            num_of_cards[i + 1] += num_of_cards[k]
        points += num_of_cards[k]
    return points


def parse_line(line: str) -> (int, list[int], list[int]):
    line_parts = line.split(":")
    game_id = int(line_parts[0].lower().replace("card", "").strip())

    numbers = [
        [int(x) for x in y.strip().split(" ") if x.isnumeric()]
        for y in line_parts[1].split("|")
    ]
    return (game_id, numbers[0], numbers[1])


def read_scratcher_data(input_file_path: str) -> {int: (list[int], list[int])}:
    with open(input_file_path, "r") as file:
        return {
            parse_line(line)[0]: (parse_line(line)[1], parse_line(line)[2])
            for line in file
        }


def calculate_points_naiive(card: (list[int], list[int])) -> int:
    winning_nums = [w for w in card[0] if w in card[1]]
    if len(winning_nums) == 0:
        return 0
    return 2 ** (len(winning_nums) - 1)


def calculate_points_total(card: (list[int], list[int])) -> int:
    return len([w for w in card[0] if w in card[1]])


def main():
    test_part_1()
    test_part_2()
    print(part_1("../input.txt"))
    print(part_2("../input.txt"))


if __name__ == "__main__":
    main()
