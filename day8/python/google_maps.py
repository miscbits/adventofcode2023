# this is a surprise tool I think I should have used
# class Node(object):
#   """Individual Node for binary tree"""
#   def __init__(self, label):
#       self.left = None
#       self.right = None
#       self.label = label

from math import gcd

def part_1():
    with open("../input.txt") as test_file:
        directions = {}
        lines = test_file.read().splitlines()
        moves = lines[0].replace("R", "1").replace("L", "0")
        for line in lines[2:]:
            directions[line[0:3]] = (line[7:10], line[12:15])

    location = "AAA"
    number_of_moves = 1
    wraparound = len(moves)
    current_move = moves[0]

    while directions[location][int(current_move)] != "ZZZ":
        location = directions[location][int(current_move)]
        current_move = moves[number_of_moves % wraparound]
        number_of_moves += 1
    print(number_of_moves)    

def part_2():
    with open("../input.txt") as test_file:
        directions = {}
        lines = test_file.read().splitlines()
        moves = lines[0].replace("R", "1").replace("L", "0")
        for line in lines[2:]:
            directions[line[0:3]] = (line[7:10], line[12:15])

    spots = [x for x in directions.keys() if x[2] == "A"]
    min_moves_from_spot_to_z = {}
    for spot in spots:
        location = spot
        number_of_moves = 1
        wraparound = len(moves)
        current_move = moves[0]

        while directions[location][int(current_move)][2] != "Z":
            location = directions[location][int(current_move)]
            current_move = moves[number_of_moves % wraparound]
            number_of_moves += 1
        min_moves_from_spot_to_z[spot] = number_of_moves

    lcm = 1
    for i in min_moves_from_spot_to_z.values():
        lcm = lcm*i//gcd(lcm, i)

    print(lcm)

part_1()
part_2()