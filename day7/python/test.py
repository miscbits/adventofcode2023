from camel_cards import part_1, part_2, Hand

with open("../test.txt") as input_file:
    camel_hands = [line.strip() for line in input_file.readlines()]
def test_part_1(camel_hands):
    expected = 6440
    actual = part_1(camel_hands)
    assert expected == actual

def test_parse_hand():
    # high card
    hand = Hand(cards='2684T', bet=825, joker_count=0)
    hand.calculate_quality()
    #          2               6               8               4               T
    expected = 1 * (10 ** 8) + 5 * (10 ** 6) + 7 * (10 ** 4) + 3 * (10 ** 2) + 9 * (10 ** 0)

    # one pair
    hand = Hand(cards='6685T', bet=825, joker_count=0)
    hand.calculate_quality()

    #          6               6               8               5               T
    expected = 5 * (10 ** 8) + 5 * (10 ** 6) + 7 * (10 ** 4) + 4 * (10 ** 2) + 9 * (10 ** 0) + 10**10
    assert expected == hand.quality

    # two pair
    hand = Hand(cards='55AJJ', bet=825, joker_count=0)
    hand.calculate_quality()

    #          5               5               A                J                J
    expected = 4 * (10 ** 8) + 4 * (10 ** 6) + 13 * (10 ** 4) + 10 * (10 ** 2) + 10 * (10 ** 0) + 10**11
    assert expected == hand.quality

    # three of a kind
    hand = Hand(cards='77A7J', bet=825, joker_count=0)
    hand.calculate_quality()

    #          7               7               A                7               J
    expected = 6 * (10 ** 8) + 6 * (10 ** 6) + 13 * (10 ** 4) + 6 * (10 ** 2) + 10 * (10 ** 0) + 10**12
    assert expected == hand.quality

    # full house
    hand = Hand(cards='55KKK', bet=825, joker_count=0)
    hand.calculate_quality()

    #          5               5               K                K                K
    expected = 4 * (10 ** 8) + 4 * (10 ** 6) + 12 * (10 ** 4) + 12 * (10 ** 2) + 12 * (10 ** 0) + 10**13
    assert expected == hand.quality

    # four of a kind
    hand = Hand(cards='5KKKK', bet=825, joker_count=0)
    hand.calculate_quality()

    #          5               K                K                K                K
    expected = 4 * (10 ** 8) + 12 * (10 ** 6) + 12 * (10 ** 4) + 12 * (10 ** 2) + 12 * (10 ** 0) + 10**14
    assert expected == hand.quality

    # five of a kind
    hand = Hand(cards='KKKKK', bet=825, joker_count=0)
    hand.calculate_quality()

    #          K                K                K                K                K
    expected = 12 * (10 ** 8) + 12 * (10 ** 6) + 12 * (10 ** 4) + 12 * (10 ** 2) + 12 * (10 ** 0) + 10**15
    assert expected == hand.quality

def test_parse_hand_joker():
    # zero jokers
    # high card
    hand = Hand(cards='2684T', bet=825, joker_count=0)
    hand.calculate_quality_jokers()
    #          2               6               8               4               T
    expected = 2 * (10 ** 8) + 6 * (10 ** 6) + 8 * (10 ** 4) + 4 * (10 ** 2) + 10 * (10 ** 0)

    # one pair
    hand = Hand(cards='6685T', bet=825, joker_count=0)
    hand.calculate_quality_jokers()

    #          6               6               8               5               T
    expected = 6 * (10 ** 8) + 6 * (10 ** 6) + 8 * (10 ** 4) + 5 * (10 ** 2) + 10 * (10 ** 0) + 10**10
    assert expected == hand.quality

    # two pair
    hand = Hand(cards='55AQQ', bet=825, joker_count=0)
    hand.calculate_quality_jokers()

    #          5               5               A                Q                Q
    expected = 5 * (10 ** 8) + 5 * (10 ** 6) + 13 * (10 ** 4) + 11 * (10 ** 2) + 11 * (10 ** 0) + 10**11
    assert expected == hand.quality

    # three of a kind
    hand = Hand(cards='77A7Q', bet=825, joker_count=0)
    hand.calculate_quality_jokers()

    #          7               7               A                7               Q
    expected = 7 * (10 ** 8) + 7 * (10 ** 6) + 13 * (10 ** 4) + 7 * (10 ** 2) + 11 * (10 ** 0) + 10**12
    assert expected == hand.quality

    # full house
    hand = Hand(cards='55KKK', bet=825, joker_count=0)
    hand.calculate_quality_jokers()

    #          5               5               K                K                K
    expected = 5 * (10 ** 8) + 5 * (10 ** 6) + 12 * (10 ** 4) + 12 * (10 ** 2) + 12 * (10 ** 0) + 10**13
    assert expected == hand.quality

    # four of a kind
    hand = Hand(cards='5KKKK', bet=825, joker_count=0)
    hand.calculate_quality_jokers()

    #          5               K                K                K                K
    expected = 5 * (10 ** 8) + 12 * (10 ** 6) + 12 * (10 ** 4) + 12 * (10 ** 2) + 12 * (10 ** 0) + 10**14
    assert expected == hand.quality

    # five of a kind
    hand = Hand(cards='KKKKK', bet=825, joker_count=0)
    hand.calculate_quality_jokers()

    #          K                K                K                K                K
    expected = 12 * (10 ** 8) + 12 * (10 ** 6) + 12 * (10 ** 4) + 12 * (10 ** 2) + 12 * (10 ** 0) + 10**15
    assert expected == hand.quality

    # one joker
    hand = Hand(cards='2QJ69', bet=825, joker_count=1)
    hand.calculate_quality_jokers()
    #          2               Q                J               6               9                two of a kind   
    expected = 2 * (10 ** 8) + 11 * (10 ** 6) + 1 * (10 ** 4) + 6 * (10 ** 2) + 9 * (10 ** 0) + 10 ** 10
    assert expected == hand.quality

    hand = Hand(cards='QQJ69', bet=825, joker_count=1)
    hand.calculate_quality_jokers()
    #          Q                Q                J               6               9               three of a kind   
    expected = 11 * (10 ** 8) + 11 * (10 ** 6) + 1 * (10 ** 4) + 6 * (10 ** 2) + 9 * (10 ** 0) + 10 ** 12
    assert expected == hand.quality

    hand = Hand(cards='QQJ66', bet=825, joker_count=1)
    hand.calculate_quality_jokers()
    #          Q                Q                J               6               6               full house   
    expected = 11 * (10 ** 8) + 11 * (10 ** 6) + 1 * (10 ** 4) + 6 * (10 ** 2) + 6 * (10 ** 0) + 10 ** 13
    assert expected == hand.quality

    hand = Hand(cards='QQJQ6', bet=825, joker_count=1)
    hand.calculate_quality_jokers()
    #          Q                Q                J               Q                6               four of a kind   
    expected = 11 * (10 ** 8) + 11 * (10 ** 6) + 1 * (10 ** 4) + 11 * (10 ** 2) + 6 * (10 ** 0) + 10 ** 14
    assert expected == hand.quality

    hand = Hand(cards='QQJQQ', bet=825, joker_count=1)
    hand.calculate_quality_jokers()
    #          Q                Q                J               Q                Q                five of a kind   
    expected = 11 * (10 ** 8) + 11 * (10 ** 6) + 1 * (10 ** 4) + 11 * (10 ** 2) + 11 * (10 ** 0) + 10 ** 15
    assert expected == hand.quality

    # two jokers
    hand = Hand(cards='JQJ67', bet=825, joker_count=2)
    hand.calculate_quality_jokers()
    #          J               Q                J               6               7               three of a kind   
    expected = 1 * (10 ** 8) + 11 * (10 ** 6) + 1 * (10 ** 4) + 6 * (10 ** 2) + 7 * (10 ** 0) + 10 ** 12
    assert expected == hand.quality

    hand = Hand(cards='JQJ66', bet=825, joker_count=2)
    hand.calculate_quality_jokers()
    #          J               Q                J               6               6               four of a kind   
    expected = 1 * (10 ** 8) + 11 * (10 ** 6) + 1 * (10 ** 4) + 6 * (10 ** 2) + 6 * (10 ** 0) + 10 ** 14
    assert expected == hand.quality

    hand = Hand(cards='J6J66', bet=825, joker_count=2)
    hand.calculate_quality_jokers()
    #          J               6               J               6               6               five of a kind   
    expected = 1 * (10 ** 8) + 6 * (10 ** 6) + 1 * (10 ** 4) + 6 * (10 ** 2) + 6 * (10 ** 0) + 10 ** 15
    assert expected == hand.quality

    # three jokers
    hand = Hand(cards='J4J2J', bet=825, joker_count=3)
    hand.calculate_quality_jokers()
    #          J               4               J               2               J               four of a kind   
    expected = 1 * (10 ** 8) + 4 * (10 ** 6) + 1 * (10 ** 4) + 2 * (10 ** 2) + 1 * (10 ** 0) + 10 ** 14
    assert expected == hand.quality

    hand = Hand(cards='J8J8J', bet=825, joker_count=3)
    hand.calculate_quality_jokers()
    #          J               8               J               8               J               five of a kind   
    expected = 1 * (10 ** 8) + 8 * (10 ** 6) + 1 * (10 ** 4) + 8 * (10 ** 2) + 1 * (10 ** 0) + 10 ** 15
    assert expected == hand.quality

    # 4 jokers
    hand = Hand(cards='J3JJJ', bet=825, joker_count=4)
    hand.calculate_quality_jokers()
    #          J               3               J               J               J               five of a kind   
    expected = 1 * (10 ** 8) + 3 * (10 ** 6) + 1 * (10 ** 4) + 1 * (10 ** 2) + 1 * (10 ** 0) + 10 ** 15
    assert expected == hand.quality

    # all jokers
    hand = Hand(cards='JJJJJ', bet=825, joker_count=1)
    hand.calculate_quality_jokers()
    #          J               J               J               J               J               five of a kind   
    expected = 1 * (10 ** 8) + 1 * (10 ** 6) + 1 * (10 ** 4) + 1 * (10 ** 2) + 1 * (10 ** 0) + 10 ** 15
    assert expected == hand.quality

def test_part_2(camel_hands):
    expected = 5905
    actual = part_2(camel_hands)
    assert expected == actual

test_part_1(camel_hands)
test_parse_hand_joker()
test_parse_hand()
test_part_2(camel_hands)