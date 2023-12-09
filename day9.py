from aocd import get_data, submit
import numpy as np
from numpy.polynomial.polynomial import Polynomial


# data = '0 3 6 9 12 15\n1 3 6 10 15 21\n10 13 16 21 30 45\n'
data = get_data(day=9, year=2023)

sequences = [list(map(int, line.split(" "))) for line in data.splitlines()]
poly_functions = [Polynomial.fit(np.arange(len(sequence)), sequence, deg=len(sequence)-1) for sequence in sequences]

next = [round(function(len(sequence))) for function, sequence in zip(poly_functions, sequences)]
previous = [round(function(-1)) for function, sequence in zip(poly_functions, sequences)]

print(f"Part 1 - Sum of extrapolated values: {sum(next)}")
print(f"Part 2 - Sum of extrapolated previous values: {sum(previous)}")

