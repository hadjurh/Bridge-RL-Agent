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
