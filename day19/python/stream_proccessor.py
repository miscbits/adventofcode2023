from kafka import KafkaProducer
import json
from kafka.admin import KafkaAdminClient, NewTopic


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
    conditions = []
    for instruction in destinations[:-1]:
        condition, destination = instruction.split(":")
        conditions.append(condition)
        instructions.append(([c for c in conditions], destination))
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
    stream_routes, messages = parse_input("../test.txt")
    stream_routes = {route[0]: route[1] for route in stream_routes}

    simplified = simplify_map(dict(stream_routes))
    while simplified.keys() != stream_routes.keys():
        stream_routes = simplified
        simplified = simplify_map(simplified)

    admin_client = KafkaAdminClient(
        bootstrap_servers="localhost:9092", client_id="admin_client"
    )

    topic_list = [NewTopic(name="in", num_partitions=1, replication_factor=1)]
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda m: json.dumps(m).encode("ascii"),
    )

    for message in messages:
        producer.produce(message)


if __name__ == "__main__":
    part_1()
