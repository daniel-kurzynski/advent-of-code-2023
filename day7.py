from aocd import get_data, submit
from collections import Counter

data = get_data(day=7, year=2023)
# data = '32T3K 765\nT55J5 684\nKK677 28\nKTJJT 220\nQQQJA 483'

bids = {cards: int(bid) for cards, bid in (h.split() for h in data.splitlines())}
hands = list(bids.keys())

def sorting_key(cards):
    return sorted(Counter(cards).values(), reverse=True), cards.translate(str.maketrans("TQKA", "AXYZ"))

print(f"Part 1 - Total winnings: {sum([rank * bids[cards] for (rank, cards) in enumerate(sorted(hands, key=sorting_key), 1)])}")

def sorting_key_joker(cards):
    best_hand = cards
    if 0 < cards.count("J") < 5:
        most_common_card, _ = Counter(cards.replace("J", "")).most_common(1)[0]
        best_hand = cards.replace("J", most_common_card)

    return sorted(Counter(best_hand).values(), reverse=True), cards.translate(str.maketrans("TQKA", "AXYZ")).replace("J", "1")

print(f"Part 2 - Total winnings: {sum([rank * bids[cards] for (rank, cards) in enumerate(sorted(hands, key=sorting_key_joker), 1)])}")
