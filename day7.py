from aocd import get_data, submit
from collections import Counter

data = get_data(day=7, year=2023)
# data = '32T3K 765\nT55J5 684\nKK677 28\nKTJJT 220\nQQQJA 483'

bids = {cards: int(bid) for cards, bid in (h.split() for h in data.splitlines())}
hands = list(bids.keys())

def classify_hand(cards):
    card_counts = sorted(Counter(cards).values(), reverse=True)

    if card_counts == [5]:
        return 6  # Five of a kind
    elif card_counts == [4, 1]:
        return 5  # Four of a kind
    elif card_counts == [3, 2]:
        return 4  # Full house
    elif card_counts == [3, 1, 1]:
        return 3  # Three of a kind
    elif card_counts == [2, 2, 1]:
        return 2  # Two pair
    elif card_counts == [2, 1, 1, 1]:
        return 1  # One pair
    else:
        return 0  # High card

def sorting_key(cards):
    return classify_hand(cards), cards.translate(str.maketrans("TQKA", "AXYZ"))

print(f"Part 1 - Total winnings: {sum([rank * bids[cards] for (rank, cards) in enumerate(sorted(hands, key=sorting_key), 1)])}")

def sorting_key_joker(cards):
    best_hand = cards
    if cards.count("J") != 5:
        most_common_card, _ = Counter(cards.replace("J", "")).most_common(1)[0]
        best_hand = cards.replace("J", most_common_card)

    return classify_hand(best_hand), cards.translate(str.maketrans("TQKA", "AXYZ")).replace("J", "1")

print(f"Part 2 - Total winnings: {sum([rank * bids[cards] for (rank, cards) in enumerate(sorted(hands, key=sorting_key_joker), 1)])}")
