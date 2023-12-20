from collections import deque


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


if __name__ == "__main__":
    part_1()
