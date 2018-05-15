from random import choice
from game.constants import Suits


class Player(object):
    def __init__(self, position, hand):
        self.position = position
        self.hand = sorted(hand)

    def set_hand(self, hand):
        self.hand = sorted(hand)

    def list_hand(self):
        return [cards.observation() for cards in self.hand]

    def count_honor_points(self):
        points = 0
        honor_limit = 10
        for card in self.hand:
            if card.value > honor_limit:
                points += card.value - honor_limit
        return points

    def play_card_random(self, suit):
        possible_cards = [cards for cards in self.hand if cards.suit in suit]
        return self.hand.pop(self.hand.index(choice(self.hand))) if len(possible_cards) == 0 else \
            self.hand.pop(self.hand.index(choice(possible_cards)))
