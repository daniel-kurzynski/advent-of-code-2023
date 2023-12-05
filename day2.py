from aocd import get_data, submit
import numpy as np

# data = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\nGame 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\nGame 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\nGame 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\nGame 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
data = get_data(day=2, year=2023)

cubes = {"red": 12, "green": 13, "blue": 14}


def is_game_possible(game):
    for round in game["rounds"]:
        for cube in cubes:
            if cube in round and cubes[cube] < round[cube]:
                return False
    return True

def game_from_string(row):
    game = {}
    game["id"] = int(row.split(":")[0].split(" ")[1])
    game["rounds"] = []
    rounds = row.split(":")[1].split(";")
    for round in rounds:
        game["rounds"].append(cubes_from_string(round))
    return game

def cubes_from_string(round):
    cubes = {}
    for cube in round.split(","):
        color = cube.split(" ")[2]
        number = int(cube.split(" ")[1])
        cubes[color] = number
    return cubes


games = [game_from_string(row) for row in data.split("\n")]
possible_games = [game["id"] for game in games if is_game_possible(game)]
print(f"Part 1: Sum of possible games is: {sum(possible_games)}")

def powers(rounds):
    max_cubes = {"red": 0, "green": 0, "blue": 0}
    for round in rounds:
        for cube in round:
            max_cubes[cube] = max(max_cubes[cube], round[cube])
    return np.prod(list(max_cubes.values()))

print(sum([powers(game["rounds"]) for game in games]))

print([x for x in cubes])
