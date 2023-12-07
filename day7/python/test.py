from camel_cards import part_1, part_2, Hand

with open("../test.txt") as input_file:
    camel_hands = [line.strip() for line in input_file.readlines()]
def test_part_1(camel_hands):
    expected = 6440
    actual = part_1(camel_hands)
    assert expected == actual

def test_parse_hand():
    # high card
    hand = Hand(cards='2684T', bet=825)
    hand.calculate_quality()
    expected = 0
    assert expected == hand.hand_type

    # one pair
    hand = Hand(cards='6685T', bet=825)
    hand.calculate_quality()

    expected = 1
    assert expected == hand.hand_type

    # two pair
    hand = Hand(cards='55AJJ', bet=825)
    hand.calculate_quality()

    expected = 2
    assert expected == hand.hand_type

    # three of a kind
    hand = Hand(cards='77A7J', bet=825)
    hand.calculate_quality()

    expected = 3
    assert expected == hand.hand_type

    # full house
    hand = Hand(cards='55KKK', bet=825)
    hand.calculate_quality()

    expected = 4
    assert expected == hand.hand_type

    # four of a kind
    hand = Hand(cards='5KKKK', bet=825)
    hand.calculate_quality()

    expected = 5
    assert expected == hand.hand_type

    # five of a kind
    hand = Hand(cards='KKKKK', bet=825)
    hand.calculate_quality()

    expected = 6
    assert expected == hand.hand_type

def test_parse_hand_joker():
    # one joker
    hand = Hand(cards='2QJ69', bet=825, jacks_are_wild=True)
    hand.calculate_quality()
    expected = 1
    assert expected == hand.hand_type

    hand = Hand(cards='QQJ69', bet=825, jacks_are_wild=True)
    hand.calculate_quality()
    expected = 3
    assert expected == hand.hand_type

    hand = Hand(cards='QQJ66', bet=825, jacks_are_wild=True)
    hand.calculate_quality()
    expected = 4
    assert expected == hand.hand_type

    hand = Hand(cards='QQJQ6', bet=825, jacks_are_wild=True)
    hand.calculate_quality()
    expected = 5
    assert expected == hand.hand_type

    hand = Hand(cards='QQJQQ', bet=825, jacks_are_wild=True)
    hand.calculate_quality()
    expected = 6
    assert expected == hand.hand_type

    # two jokers
    hand = Hand(cards='JQJ67', bet=825, jacks_are_wild=True)
    hand.calculate_quality()
    expected = 3
    assert expected == hand.hand_type

    hand = Hand(cards='JQJ66', bet=825, jacks_are_wild=True)
    hand.calculate_quality()
    expected = 5
    assert expected == hand.hand_type

    hand = Hand(cards='J6J66', bet=825, jacks_are_wild=True)
    hand.calculate_quality()
    expected = 6
    assert expected == hand.hand_type

    # three jokers
    hand = Hand(cards='J4J2J', bet=825, jacks_are_wild=True)
    hand.calculate_quality()
    expected = 5
    assert expected == hand.hand_type

    hand = Hand(cards='J8J8J', bet=825, jacks_are_wild=True)
    hand.calculate_quality()
    expected = 6
    assert expected == hand.hand_type

    # 4 jokers
    hand = Hand(cards='J3JJJ', bet=825, jacks_are_wild=True)
    hand.calculate_quality()
    expected = 6
    assert expected == hand.hand_type

    # all jokers
    hand = Hand(cards='JJJJJ', bet=825, jacks_are_wild=True)
    hand.calculate_quality()
    expected = 6
    assert expected == hand.hand_type

def test_part_2(camel_hands):
    expected = 5905
    actual = part_2(camel_hands)
    assert expected == actual

test_parse_hand()
test_parse_hand_joker()
test_part_1(camel_hands)
test_part_2(camel_hands)