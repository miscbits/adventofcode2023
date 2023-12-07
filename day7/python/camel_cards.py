from dataclasses import dataclass
from dataclasses import field

SHARED_VAL_MAP = {
    '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, 'T': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13,
}

SHARED_VAL_MAP_JOKERS = {
    'J': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'Q': 11, 'K': 12, 'A': 13,
}

TIE_BREAK_MAP_JOKER = {
    'J': 'a', '2': 'b', '3': 'c', '4': 'd', '5': 'e', '6': 'f', '7': 'g', '8': 'h', '9': 'i', 'T': 'j', 'Q': 'k', 'K': 'l', 'A': 'm',
}

TIE_BREAK_MAP = {
    '2': 'a', '3': 'b', '4': 'c', '5': 'd', '6': 'e', '7': 'f', '8': 'g', '9': 'h', 'T': 'i', 'J': 'j', 'Q': 'k', 'K': 'l', 'A': 'm',
}

FIVE_OF_A_KIND = 10**15
FOUR_OF_A_KIND = 10**14
FULL_HOUSE = 10**13
THREE_OF_A_KIND = 10**12
TWO_PAIR = 10**11
ONE_PAIR = 10**10

TYPE_FIVE_OF_A_KIND = 6
TYPE_FOUR_OF_A_KIND = 5
TYPE_FULL_HOUSE = 4
TYPE_THREE_OF_A_KIND = 3
TYPE_TWO_PAIR = 2
TYPE_ONE_PAIR = 1

@dataclass(order=True, kw_only=True)
class Hand:
    hand_type: int = 0
    tie_break: str = ""
    quality: int = 0
    cards: str
    bet: int
    joker_count: int = 0

    def calculate_quality(self):
        self.quality = 0
        card_counter = {}
        for i, card in enumerate(self.cards):
            self.quality += SHARED_VAL_MAP[card] * (10 ** ((len(self.cards) - i - 1) * 2)) # [0, 2, 4, 6, 8]
            self.tie_break += TIE_BREAK_MAP[card]
            card_counter[card] = card_counter.get(card, 0) + 1
        card_types, card_vals = card_counter.keys(), card_counter.values()
        # 5 of a kind
        if len(card_types) == 1:
            self.quality += FIVE_OF_A_KIND
            self.hand_type=TYPE_FIVE_OF_A_KIND
            return self
        if len(card_types) == 2:
            # 4 of a kind
            if 4 in card_vals:
                self.quality += FOUR_OF_A_KIND
                self.hand_type=TYPE_FOUR_OF_A_KIND
            # full house
            elif 3 in card_vals:
                self.quality += FULL_HOUSE
                self.hand_type=TYPE_FULL_HOUSE
                return self
        # 3 of a kind. can't be a full house because previous check
        if 3 in card_vals:
            self.quality += THREE_OF_A_KIND
            self.hand_type=TYPE_THREE_OF_A_KIND
        #  two pair
        elif list(card_vals).count(2) == 2:
            self.quality += TWO_PAIR
            self.hand_type=TYPE_TWO_PAIR
        # one pair
        elif 2 in card_vals:
            self.quality += ONE_PAIR
            self.hand_type=TYPE_ONE_PAIR
        return self

    def calculate_quality_jokers(self):
        self.quality = 0
        card_counter = {}
        for i, card in enumerate(self.cards):
            self.quality += SHARED_VAL_MAP_JOKERS[card] * (10 ** ((len(self.cards) - i - 1) * 2)) # [0, 2, 4, 6, 8]
            self.tie_break += TIE_BREAK_MAP_JOKER[card]
            if card == 'J':
                continue
            card_counter[card] = card_counter.get(card, 0) + 1
        card_types, card_vals = card_counter.keys(), card_counter.values()
        # one or zero card types is always five of a kind
        # this covers all cases like [4], [3], [2], [1] so we wont have to check for that with any other combination of hands + jokers
        # this also is always true if joker count is 4 or 5
        if len(card_types) <= 1:
            self.quality += FIVE_OF_A_KIND
            self.hand_type = TYPE_FIVE_OF_A_KIND
            return self
        if self.joker_count <= 0:
            if len(card_types) == 2:
                # 4 of a kind
                if 4 in card_vals:
                    self.quality += FOUR_OF_A_KIND
                    self.hand_type = TYPE_FOUR_OF_A_KIND
                # full house
                elif 3 in card_vals:
                    self.quality += FULL_HOUSE
                    self.hand_type = TYPE_FULL_HOUSE
                    return self
            # 3 of a kind. can't be a full house because previous check
            if 3 in card_vals:
                self.quality += THREE_OF_A_KIND
                self.hand_type = TYPE_THREE_OF_A_KIND
            #  two pair
            elif list(card_vals).count(2) == 2:
                self.quality += TWO_PAIR
                self.hand_type = TYPE_TWO_PAIR
            # one pair
            elif 2 in card_vals:
                self.quality += ONE_PAIR
                self.hand_type = TYPE_ONE_PAIR
            return self
        # card vals sums to 4
        elif self.joker_count == 1:
            # implies [3, 1]
            if 3 in card_vals:
                self.quality += FOUR_OF_A_KIND
                self.hand_type = TYPE_FOUR_OF_A_KIND
            # [2, 1, 1] or [2, 2] possible here
            elif 2 in card_vals:
                # implies [2, 2]
                if len(card_vals) == 2:
                    self.quality += FULL_HOUSE
                    self.hand_type = TYPE_FULL_HOUSE
                # implies [2, 1, 1]
                else:
                    self.quality += THREE_OF_A_KIND
                    self.hand_type = TYPE_THREE_OF_A_KIND
            # [1,1,1,1] is the only option left
            else:
                self.quality += ONE_PAIR
                self.hand_type = TYPE_ONE_PAIR
        # card vals sum to 3
        elif self.joker_count == 2:
            # implies [2, 1]
            if 2 in card_vals:
                self.quality += FOUR_OF_A_KIND
                self.hand_type = TYPE_FOUR_OF_A_KIND
            # [1, 1, 1] is the only option left
            else:
                self.quality += THREE_OF_A_KIND
                self.hand_type = TYPE_THREE_OF_A_KIND
        # card vals sum to 2 and we know its not [2] so it must be [1,1]
        elif self.joker_count == 3:
            self.quality += FOUR_OF_A_KIND
            self.hand_type = TYPE_FOUR_OF_A_KIND
        return self

def part_1(camel_hands: list[str]) -> int:
    parsed_hands: list[Hand] = [
        Hand(cards=parts[0], bet=int(parts[1]), joker_count=parts[0].count('J')).calculate_quality()
        for hand in camel_hands if (parts := hand.split(" "))
    ]

    parsed_hands.sort()
    total_score = 0
    for place, hand in enumerate(parsed_hands):
        total_score += hand.bet * (place + 1)
    return total_score

def part_2(camel_hands: list[str]) -> int:
    parsed_hands: list[Hand] = [
        Hand(cards=parts[0], bet=int(parts[1]), joker_count=parts[0].count('J')).calculate_quality_jokers()
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
