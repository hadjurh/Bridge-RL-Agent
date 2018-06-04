from enum import Enum


class Positions(Enum):
    North = 0
    East = 1
    South = 2
    West = 3


values = list(range(2, 15))


class Suits(Enum):
    Clubs = 0
    Diamonds = 1
    Hearts = 2
    Spades = 3


nt_points = {
    21: 7,
    22: 7,
    23: 8,
    24: 8,
    25: 9,
    26: 9,
    27: 10,
    28: 10,
    29: 11,
    30: 11,
    31: 11,
    32: 11,
    33: 12,
    34: 12,
    35: 12,
    36: 12,
    37: 13,
    38: 13,
    39: 13,
    40: 13
}

trump_points = {
    21: 7,
    22: 8,
    23: 9,
    24: 9,
    25: 10,
    26: 10,
    27: 11,
    28: 11,
    29: 11,
    30: 11,
    31: 12,
    32: 12,
    33: 12,
    34: 12,
    35: 12,
    36: 12,
    37: 13,
    38: 13,
    39: 13,
    40: 13
}
