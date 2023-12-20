from dataclasses import dataclass, field
from enum import Enum
from math import lcm
from collections import deque

ModuleType = Enum("Module", ["FLIP_FLOP", "CONJUCTION", "BROADCASTER"])
PulseType = Enum("Pulse", ["LOW", "HIGH"])


@dataclass
class FlipFlopModule:
    name: str
    destinations: []
    on: bool = False

    def receive_pulse(self, pulse: PulseType, receieved_from: str):
        if pulse == PulseType.LOW:
            self.on = not self.on
            if self.on:
                return PulseType.HIGH
            return PulseType.LOW
        return None


@dataclass
class ConjuctionModule:
    name: str
    destinations: []
    previous_pulses: {str: PulseType} = field(default_factory=dict)

    def receive_pulse(self, pulse: PulseType, receieved_from: str):
        self.previous_pulses[receieved_from] = pulse
        if all([v == PulseType.HIGH for v in self.previous_pulses.values()]):
            return PulseType.LOW
        return PulseType.HIGH


@dataclass
class BroadCaster:
    name: str
    destinations: []


def module_factory(module_schema):
    module_name, destinations = module_schema.split(" -> ")
    destinations = destinations.replace(" ", "").split(",")

    match module_schema[0]:
        case "%":
            return FlipFlopModule(module_name[1:], destinations)
        case "&":
            return ConjuctionModule(module_name[1:], destinations)
        case "b":
            return BroadCaster(module_name, destinations)


def parse_input(input_file_path):
    with open(input_file_path) as input_file:
        data = input_file.read().split("\n")
    modules = {}
    for module_input in data:
        module = module_factory(module_input)
        if type(module) == BroadCaster:
            broadcaster = module
        else:
            modules[module.name] = module

    return broadcaster, modules


@dataclass
class Signal:
    sender: str
    destination: str
    pulse: PulseType


def part_1():
    broadcaster, modules = parse_input("../input.txt")
    for module in modules.values():
        for destination in module.destinations:
            if (
                modules.get(destination)
                and type(modules[destination]) == ConjuctionModule
            ):
                modules[destination].previous_pulses[module.name] = PulseType.LOW

    signals = deque()
    count_low_pulse = 0
    count_high_pulses = 0
    for i in range(1000):
        count_low_pulse += 1
        for destination in broadcaster.destinations:
            signals.append(Signal(broadcaster.name, destination, PulseType.LOW))
        while signals:
            signal = signals.popleft()  # FIFO

            if signal.pulse == PulseType.LOW:
                count_low_pulse += 1
            else:
                count_high_pulses += 1
            if not modules.get(signal.destination):
                continue
            response = modules[signal.destination].receive_pulse(
                signal.pulse, signal.sender
            )
            if response:
                for dest in modules[signal.destination].destinations:
                    signals.append(
                        Signal(modules[signal.destination].name, dest, response)
                    )

    print(count_low_pulse, count_high_pulses)
    print(count_low_pulse * count_high_pulses)


def part_2():
    broadcaster, modules = parse_input("../input.txt")
    for module in modules.values():
        for destination in module.destinations:
            if (
                modules.get(destination)
                and type(modules[destination]) == ConjuctionModule
            ):
                modules[destination].previous_pulses[module.name] = PulseType.LOW
        if "rx" in module.destinations:
            module_that_outputs_to_rx = module
    cycles = {d: 0 for d in module_that_outputs_to_rx.previous_pulses.keys()}

    signals = deque()
    button_presses = 0
    while not all(list(cycles.values())):
        button_presses += 1
        for destination in broadcaster.destinations:
            signals.append(Signal(broadcaster.name, destination, PulseType.LOW))
        while signals:
            signal = signals.popleft()  # FIFO
            if signal.destination == "rx" and signal.pulse == PulseType.LOW:
                return button_presses
            if not modules.get(signal.destination):
                continue
            response = modules[signal.destination].receive_pulse(
                signal.pulse, signal.sender
            )
            if response:
                for dest in modules[signal.destination].destinations:
                    signals.append(
                        Signal(modules[signal.destination].name, dest, response)
                    )
            if (
                signal.destination == module_that_outputs_to_rx.name
                and signal.pulse == PulseType.HIGH
                and cycles.get(signal.sender) == 0
            ):
                cycles[signal.sender] = button_presses
    print(lcm(*cycles.values()))


if __name__ == "__main__":
    part_1()
    part_2()
