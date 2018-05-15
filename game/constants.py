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
