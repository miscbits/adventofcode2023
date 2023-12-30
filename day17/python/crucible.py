from dataclasses import dataclass, field
from heapq import heappush, heappop


@dataclass(frozen=True)
class CityBlock:
    x: int
    y: int
    heat: int


@dataclass(order=True)
class PrioritizedItem:
    heatloss: int
    dx: int = field(compare=False)
    dy: int = field(compare=False)
    item: CityBlock = field(compare=False)


@dataclass
class Crucible:
    matrix: dict[tuple[int, int], CityBlock]
    min_move: int = 1
    max_move: int = 3

    def in_matrix_limit(self, x, y):
        return (x, y) in self.matrix

    def max_x_y(self):
        return max(self.matrix.keys())


def parse_input_file(file_path, min_move=1, max_move=3) -> Crucible:
    with open(file_path, "r") as f:
        file = f.read()

    matrix = {}
    for ri, row in enumerate(file.split("\n")):
        for ci, c in enumerate(list(row)):
            matrix[ri, ci] = CityBlock(ri, ci, int(c))
    return Crucible(matrix, min_move, max_move)


def calculate_heat_loss(min_move, max_move) -> int:
    crucible = parse_input_file('../input.txt', min_move, max_move)

    destination = crucible.max_x_y()
    searched = set()
    heap = [PrioritizedItem(0, 0, 0, crucible.matrix[(0, 0)])]

    while node := heappop(heap):
        heatloss = node.heatloss
        dx = node.dx
        dy = node.dy
        block = node.item
        x, y = block.x, block.y

        if (block.x, block.y) == destination:
            return heatloss
        if (x, y, dx, dy) in searched:
            continue
        searched.add((x, y, dx, dy))

        for tx, ty in {(1, 0), (0, 1), (-1, 0), (0, -1)}-{(dx, dy), (-dx, -dy)}:
            a, b, h = x, y, heatloss
            for i in range(1, crucible.max_move + 1):
                a, b = a+tx, b+ty
                if not crucible.in_matrix_limit(a, b):
                    continue
                h += crucible.matrix[a, b].heat
                if i >= crucible.min_move:
                    heappush(heap, PrioritizedItem(
                        h, tx, ty, crucible.matrix[a, b]))
    return -1


def part1():
    return calculate_heat_loss(1, 3)


def part2():
    return calculate_heat_loss(4, 10)


if __name__ == "__main__":
    print(part1())
    print(part2())
