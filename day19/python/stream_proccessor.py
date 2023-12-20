from collections import deque
from dataclasses import dataclass, replace


def parse_message(message_input):
    message = {}
    for param in message_input[1:-1].split(","):
        k, v = param.split("=")
        message[k] = int(v)
    return message


def test_condition(message, condition_input):
    condition_key = condition_input[0]
    condition_operator = condition_input[1]
    condition_val = int(condition_input[2:])
    match condition_operator:
        case "<":
            return message[condition_key] < condition_val
        case ">":
            return message[condition_key] > condition_val
        case "=":
            return message[condition_key] == condition_val
    return False


def parse_direction(direction_input):
    # qbl{m<1574:A,R}
    stream_name, destinations = direction_input[:-1].split("{")
    destinations = destinations.split(",")
    instructions = []
    for instruction in destinations[:-1]:
        condition, destination = instruction.split(":")
        instructions.append((condition, destination))
    instructions.append(("default", destinations[-1]))
    return (stream_name, instructions)


def parse_input(input_file_path):
    with open(input_file_path) as input_file:
        directions, messages = input_file.read().split("\n\n")
    stream_routes = [parse_direction(direction) for direction in directions.split("\n")]
    messages = [parse_message(message) for message in messages.split("\n")]

    return stream_routes, messages


def is_unidirection(stream_route_rules):
    directions = set([d[1] for d in stream_route_rules])
    return len(directions) == 1


def simplify_map(stream_routes):
    unidirection_map = {}
    for stream, rules in stream_routes.items():
        if is_unidirection(rules):
            unidirection_map[stream] = rules[-1][-1]

    for stream in unidirection_map.keys():
        del stream_routes[stream]

    for stream, rules in stream_routes.items():
        for i in range(len(rules)):
            stream_routes[stream][i] = (
                rules[i][0],
                unidirection_map.get(rules[i][1], rules[i][1]),
            )

    return stream_routes


def part_1():
    stream_routes, messages = parse_input("../input.txt")
    stream_routes = {route[0]: route[1] for route in stream_routes}

    simplified = simplify_map(dict(stream_routes))
    while simplified.keys() != stream_routes.keys():
        stream_routes = simplified
        simplified = simplify_map(simplified)

    topics = {r: deque() for r in stream_routes}

    for message in messages:
        topics["in"].append(message)

    accepted_queue = deque()

    topics_to_process_next = deque()
    topics_to_process_next.append("in")

    while list(topics_to_process_next):
        topic = topics_to_process_next.popleft()  # FIFO processing
        print("processing", topic)
        next_topics = set()
        while list(topics[topic]):
            q_item = topics[topic].pop()
            routes = stream_routes[topic]
            for rules, destination in routes:
                if rules == "default" or test_condition(q_item, rules):
                    if destination == "A":
                        accepted_queue.append(q_item)
                    elif destination == "R":
                        pass  # message is
                    else:
                        next_topics.add(destination)
                        topics[destination].append(q_item)
                    break
        for nt in next_topics:
            topics_to_process_next.append(nt)

    total = 0
    for item in accepted_queue:
        total += item["x"] + item["m"] + item["a"] + item["s"]

    print(total)


@dataclass
class Possibility:
    destination: str = "in"
    min_x: int = 0
    max_x: int = 4000
    min_m: int = 0
    max_m: int = 4000
    min_a: int = 0
    max_a: int = 4000
    min_s: int = 0
    max_s: int = 4000

    def is_valid(self):
        return (
            self.min_x <= self.max_x
            and self.min_m <= self.max_m
            and self.min_a <= self.max_a
            and self.min_s <= self.max_s
        )

    def get_prop(self, prop: str):
        match prop:
            case "min_x":
                return self.min_x
            case "max_x":
                return self.max_x
            case "min_m":
                return self.min_m
            case "max_m":
                return self.max_m
            case "min_a":
                return self.min_a
            case "max_a":
                return self.max_a
            case "min_s":
                return self.min_s
            case "max_s":
                return self.max_s

    def set_prop(self, prop: str, val: int):
        match prop:
            case "min_x":
                self.min_x = val
            case "max_x":
                self.max_x = val
            case "min_m":
                self.min_m = val
            case "max_m":
                self.max_m = val
            case "min_a":
                self.min_a = val
            case "max_a":
                self.max_a = val
            case "min_s":
                self.min_s = val
            case "max_s":
                self.max_s = val


def eval_possibilities(possibility, routes):
    new_possibilities = []
    eval_possib = replace(possibility)
    for rule, destination in routes:
        new_possib = replace(eval_possib)
        new_possib.destination = destination
        match rule[1]:
            case "=":
                rule_val = int(rule[2:])
                new_possib.set_prop("max_" + rule[0], rule_val)
                new_possib.set_prop("min_" + rule[0], rule_val)
                eval_possib.set_prop(
                    "max_" + rule[0],
                    max(rule_val - 1, eval_possib.get_prop("max_" + rule[0])),
                )
                eval_possib.set_prop(
                    "min_" + rule[0],
                    min(rule_val + 1, eval_possib.get_prop("min_" + rule[0])),
                )
            case ">":
                rule_val = int(rule[2:])
                new_possib.set_prop("min_" + rule[0], rule_val + 1)
                eval_possib.set_prop(
                    "max_" + rule[0],
                    min(eval_possib.get_prop("max_" + rule[0]), rule_val),
                )
            case "<":
                rule_val = int(rule[2:])
                new_possib.set_prop("max_" + rule[0], rule_val - 1)
                eval_possib.set_prop(
                    "min_" + rule[0],
                    max(eval_possib.get_prop("min_" + rule[0]), rule_val),
                )
        if destination != "R":
            new_possibilities.append(new_possib)
        if not eval_possib.is_valid():
            break
    print(new_possibilities)
    return new_possibilities


def part_2():
    stream_routes, messages = parse_input("../test.txt")
    stream_routes = {route[0]: route[1] for route in stream_routes}

    simplified = simplify_map(dict(stream_routes))
    while simplified.keys() != stream_routes.keys():
        stream_routes = simplified
        simplified = simplify_map(simplified)

    possibilities = deque()
    possibilities.append(Possibility())
    accepted_possibilities = []
    while possibilities:
        possibility = possibilities.pop()
        if possibility.destination == "A":
            accepted_possibilities.append(possibility)
        else:
            for p in eval_possibilities(
                possibility, stream_routes[possibility.destination]
            ):
                possibilities.append(p)
    print(accepted_possibilities)

    count = 0

    for possibility in accepted_possibilities:
        count += (
            (possibility.max_x - possibility.min_x)
            * (possibility.max_m - possibility.min_m)
            * (possibility.max_a - possibility.min_a)
            * (possibility.max_s - possibility.min_s)
        )
    print(accepted_possibilities)
    print(count)


if __name__ == "__main__":
    part_2()
