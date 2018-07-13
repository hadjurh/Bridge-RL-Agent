from game.constants import Suits, values


class Card(object):
    def __init__(self, suit, value):
        """
        :param suit: [Clubs = 0, Diamonds = 1, Hearts = 2, Spades = 3]
        :param value: 2..14
        """
        self.suit = suit
        self.value = value

    def __str__(self):
        return str(self.value) + str(self.suit)[6]

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

    def __gt__(self, other):
        if self.value == other.value:
            return self.suit.value > other.suit.value
        return self.value > other.value

    def __lt__(self, other):
        return not (self > other or self == other)

    # How the cards in actions and states are represented
    def observation(self):
        return (self.value - 1) + self.suit.value * 13

    def close_cards(self):
        close_cards = {}
        for distance in range(1, 13):
            close_cards[distance] = []
            if self.value - distance >= 2:
                close_cards[distance].append(Card(self.suit, self.value - distance))
            if self.value + distance <= 14:
                close_cards[distance].append(Card(self.suit, self.value + distance))
        return close_cards


def observation_to_card(observation):
    """
    Transform an observation into a Card
    :param observation
    :return: Associated Card
    """
    suit = Suits((observation - 1) // 13)
    value = observation % 13 if observation % 13 != 0 else 13

    return Card(suit, value + 1)


if __name__ == '__main__':
    c = Card(Suits.Clubs, 5)
    close_c = c.close_cards()
    print(close_c)

    for s in Suits:
        for v in values:
            print(Card(s, v))
            assert Card(s, v) == observation_to_card(Card(s, v).observation())

    assert Card(Suits.Clubs, 2) < Card(Suits.Clubs, 3)
    assert not Card(Suits.Clubs, 3) < Card(Suits.Clubs, 2)
    assert not Card(Suits.Clubs, 2) > Card(Suits.Clubs, 3)
    assert Card(Suits.Clubs, 3) > Card(Suits.Clubs, 2)
    assert not Card(Suits.Diamonds, 2) == Card(Suits.Diamonds, 3)
    assert not Card(Suits.Diamonds, 2) == Card(Suits.Clubs, 2)
    assert not Card(Suits.Diamonds, 2) == Card(Suits.Clubs, 3)
    assert Card(Suits.Diamonds, 2) == Card(Suits.Diamonds, 2)

    print("Tests passed")
