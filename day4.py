from aocd import get_data, submit
import re


# data = "Card 1: 41 48 83 86 17 | 83 86 6 31 17 9 48 53\nCard 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\nCard 3: 1 21 53 59 44 | 69 82 63 72 16 21 14 1\nCard 4: 41 92 73 84 69 | 59 84 76 51 58 5 54 83\nCard 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\nCard 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"
data = get_data(day=4, year=2023)

def card_from_string(row):
    card = {}
    card["winningNumbers"] = [int(number) for number in row.split(':')[1].strip().split("|")[0].strip().split(" ") if number != ""]
    card["myNumbers"] = [int(number) for number in row.split(':')[1].strip().split("|")[1].strip().split(" ") if number != ""]
    return card


def number_of_matching_winning_numbers(card):
    return len(set(card["winningNumbers"]).intersection(card["myNumbers"]))

def number_of_points(card):
    matches = number_of_matching_winning_numbers(card)
    if matches == 0:
        return 0
    else:
        return 2 ** (matches - 1)


cards = [card_from_string(row.strip()) for row in data.split("\n")]

print(f"Part 1: Points in total: {sum([number_of_points(card) for card in cards])}")

number_of_cards = [1 for x in range(len(cards))]

for idx, card in enumerate(cards):
    matches = number_of_matching_winning_numbers(card)
    for c in range(matches):
        if(idx+c+1 >= len(number_of_cards)):
            break;
        number_of_cards[idx + c + 1] = number_of_cards[idx + c + 1] + number_of_cards[idx]

print(f"Part 2: Total number of cards: {sum(number_of_cards)}")
