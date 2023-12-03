class Schematic():
    """docstring for Schematic"""
    def __init__(self, schematic_lines):
        self.schematic_lines = schematic_lines

    def dimmensions(self) -> tuple[int, int]:
        return (len(self.schematic_lines), len(self.schematic_lines[-1]))

    def expand_coordinates(self, coords: tuple[int, int], length: int) -> list[tuple[int, int]]:
        return [(coords[0], y) for y in range(coords[1], coords[1]+length)]

    def find_num_coordinates(self, search_cooridanrtes: tuple[int, int]) -> tuple[tuple[int, int], int]:
        x, y = search_cooridanrtes
        if not self.schematic_lines[x][y].isdigit():
            return ((-1, -1), -1)

        search_index = y-1
        while(search_index >= 0 and self.schematic_lines[x][search_index].isdigit()):
            search_index -= 1
        search_index += 1
        left_digit = (x, search_index)

        length = 0
        while(search_index < self.dimmensions()[1] and self.schematic_lines[x][search_index].isdigit()):
            length+=1
            search_index+=1

        return (left_digit, length)

    def find_num_len(self, search_cooridanrtes: tuple[int, int]) -> int:
        x, y = search_cooridanrtes
        if not self.schematic_lines[x][y].isdigit():
            return -1

        length = 0
        search_index = y
        while(search_index < self.dimmensions()[1] and self.schematic_lines[x][search_index].isdigit()):
            length+=1
            search_index+=1

        return length

    def extract_num(self, left_digit: tuple[int, int], length: int) -> int:
        x,y = left_digit
        return int(self.schematic_lines[x][y:y+length])

    def coords_contain_special_char(self, coords: list[tuple[int, int]]) -> bool:
        for coord in coords:
            if self.contains_special(coord):
                return True
        return False

    def contains_special(self, coord: tuple[int, int]) -> bool:
        x, y = coord
        if self.schematic_lines[x][y] == '.':
            return False
        return True

    def gear_ratio(self, coord: tuple[int, int]) -> int:
        x,y = coord
        found_nums = []
        searched_coords = []
        if self.schematic_lines[x][y] != '*':
            return 0

        surroundings = calcate_surroundings(coord, 1)
        for surrounding in surroundings:
            if surrounding in searched_coords:
                continue
            if self.schematic_lines[surrounding[0]][surrounding[1]].isdigit():
                num_coord = self.find_num_coordinates(surrounding)
                for x in self.expand_coordinates(num_coord[0], num_coord[1]):
                    searched_coords.append(x)
                found_nums.append(self.extract_num(num_coord[0], num_coord[1]))
            if len(found_nums) > 2:
                return 0
        if len(found_nums) == 2:
            return found_nums[0] * found_nums[1]
        return 0

def load_schematic(file_path: str) -> Schematic:
    with open(file_path, 'r') as file:
        return Schematic(file.readlines())

def part_1():
    schematic = load_schematic('../input.txt')

    line_index = 0
    engine_parts = []
    for line_index in range(len(schematic.schematic_lines)):
        line = schematic.schematic_lines[line_index]
        char_index = 0
        while char_index < len(line):
            if line[char_index].isdigit():
                left_digit = (line_index,char_index)
                length = schematic.find_num_len(left_digit)
                surroundings = calcate_surroundings(left_digit, length)
                if schematic.coords_contain_special_char(surroundings):
                    engine_parts.append(schematic.extract_num(left_digit, length))
                char_index+=length
                continue
            char_index+=1
    print(sum(engine_parts))


def main():
    test_calculate_surroundings()
    test_schematic_special_character_detector()
    test_is_gear()

    schematic = load_schematic('../input.txt')

    gear_ratio_sums = 0
    dimmensions = schematic.dimmensions()
    for x in range(dimmensions[0]):
        for y in range(dimmensions[1]):
            if schematic.schematic_lines[x][y] == '*':
                gear_ratio_sums+=schematic.gear_ratio((x,y))
    print(gear_ratio_sums)


def calcate_surroundings(left_digit: tuple[int, int], length: int) -> list[tuple[int, int]]:
    x,y = left_digit
    return [
        (x+1,row) for row in range(y, y+length)
    ] + [
        (x-1,row) for row in range(y, y+length)
    ] + [
        (x,y-1), (x,y+length), (x-1,y-1), (x+1,y+length), (x-1, y+length), (x+1, y-1)
    ]


def test_calculate_surroundings():
    surroundings = calcate_surroundings((1,1), 1)
    assert  set(surroundings).issubset(set([
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 2),
        (2, 0), (2, 1), (2, 2),
    ]))

def test_schematic_special_character_detector():
    schematic = Schematic([
        '...', '.1.', '...'
    ])
    surroundings = calcate_surroundings((1,1), 1)
    assert not schematic.coords_contain_special_char(surroundings)

    schematic = Schematic([
        '*..', '.1.', '...'
    ])
    surroundings = calcate_surroundings((1,1), 1)
    assert schematic.coords_contain_special_char(surroundings)

    schematic = Schematic([
        '.*.', '*1.', '...'
    ])
    surroundings = calcate_surroundings((1,1), 1)
    assert schematic.coords_contain_special_char(surroundings)

    schematic = Schematic([
        '..*', '.1*', '...'
    ])
    surroundings = calcate_surroundings((1,1), 1)
    assert schematic.coords_contain_special_char(surroundings)

    schematic = Schematic([
        '...', '.1.', '*..'
    ])
    surroundings = calcate_surroundings((1,1), 1)
    assert schematic.coords_contain_special_char(surroundings)

    schematic = Schematic([
        '...', '.1.', '.*.'
    ])
    surroundings = calcate_surroundings((1,1), 1)
    assert schematic.coords_contain_special_char(surroundings)

    schematic = Schematic([
        '...', '.1.', '..*'
    ])
    surroundings = calcate_surroundings((1,1), 1)
    assert schematic.coords_contain_special_char(surroundings)

def test_is_gear():
    schamtic = Schematic(['...813..',
        '.....*..',
        '...476..',])

    assert schamtic.gear_ratio((1,5)) == 813*476



if __name__ == '__main__':
    main()