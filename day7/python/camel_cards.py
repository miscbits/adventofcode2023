from __future__ import annotations
from dataclasses import dataclass

TIE_BREAK_MAP_JOKER = {
    'J': 'a', '2': 'b', '3': 'c', '4': 'd', '5': 'e', '6': 'f', '7': 'g', '8': 'h', '9': 'i', 'T': 'j', 'Q': 'k', 'K': 'l', 'A': 'm',
}

TIE_BREAK_MAP = {
    '2': 'a', '3': 'b', '4': 'c', '5': 'd', '6': 'e', '7': 'f', '8': 'g', '9': 'h', 'T': 'i', 'J': 'j', 'Q': 'k', 'K': 'l', 'A': 'm',
}

FIVE_OF_A_KIND = 6
FOUR_OF_A_KIND = 5
FULL_HOUSE = 4
THREE_OF_A_KIND = 3
TWO_PAIR = 2
ONE_PAIR = 1

@dataclass(order=True, kw_only=True)
class Hand:
    hand_type: int = 0
    tie_break: str = ""
    cards: str
    bet: int
    jacks_are_wild: bool = False

    def calculate_tie_break(self) -> Hand:
        self.tie_break = "".join([TIE_BREAK_MAP_JOKER[card] if self.jacks_are_wild else TIE_BREAK_MAP[card] for card in self.cards])
        return self

    def calculate_quality(self) -> Hand:
        card_counter = {}
        for card in self.cards:
            if self.jacks_are_wild and card == 'J':
                continue
            card_counter[card] = card_counter.get(card, 0) + 1
        card_vals = list(card_counter.values())
        card_vals.sort(reverse=True)

        # five of a kind
        if card_vals in [[5], [4], [3], [2], [1], []]:
            self.hand_type = FIVE_OF_A_KIND
        # four of a kind
        elif card_vals in [[4,1], [3,1], [2,1], [1,1]]:
            self.hand_type = FOUR_OF_A_KIND
        # full house
        elif card_vals in [[3,2], [2,2]]:
            self.hand_type = FULL_HOUSE
        # thee of a kind
        elif card_vals in [[3,1,1], [2,1,1], [1,1,1]]:
            self.hand_type = THREE_OF_A_KIND
        # two pair
        elif card_vals in [[2,2,1]]:
            self.hand_type = TWO_PAIR
        # pair
        elif card_vals in [[2,1,1,1], [1,1,1,1]]:
            self.hand_type = ONE_PAIR

        return self

def part_1(camel_hands: list[str]) -> int:
    parsed_hands: list[Hand] = [
        Hand(cards=parts[0], bet=int(parts[1])).calculate_quality().calculate_tie_break()
        for hand in camel_hands if (parts := hand.split(" "))
    ]

    parsed_hands.sort()
    total_score = 0
    for place, hand in enumerate(parsed_hands):
        total_score += hand.bet * (place + 1)
    return total_score

def part_2(camel_hands: list[str]) -> int:
    parsed_hands: list[Hand] = [
        Hand(cards=parts[0], bet=int(parts[1]), jacks_are_wild=True).calculate_quality().calculate_tie_break()
        for hand in camel_hands if (parts := hand.split(" "))
    ]

    parsed_hands.sort()
    total_score = 0
    for place, hand in enumerate(parsed_hands):
        total_score += hand.bet * (place + 1)
    return total_score


if __name__ == "__main__":
    with open("../input.txt") as input_file:
        camel_hands = [line.strip() for line in input_file.readlines()]
    p1_answer = part_1(camel_hands)
    p2_answer = part_2(camel_hands)

    print(p1_answer)
    print(p2_answer)
