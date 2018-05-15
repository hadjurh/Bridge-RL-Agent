from game.cards import Card
from game.constants import Suits, Positions, values
from game.player import Player
from game.contract import Contract
from random import shuffle


class Game(object):
    def __init__(self):
        """
        Set the game up ready to start
        """
        self.players = [Player(position, []) for position in Positions]
        self.deck = [Card(suit, value) for suit in Suits for value in values]
        self.number_of_played_cards = 0
        self.contract = Contract()
        self.trick = {position: None for position in Positions}
        self.trick_history = []
        self.declarer_honor_points = 0
        self.scores = {"NS": 0, "EW": 0}
        self.done = False
        self.dominant_suit = Suits

        while self.contract.declarer is None:
            self.deal()
            self.set_contract()
        self.whose_turn_it_is_to_play = Positions((self.contract.declarer.value + 1) % 4)

    def deal(self):
        shuffle(self.deck)
        cards_number_per_player = len(self.deck) // 4
        for p in range(len(self.players)):
            self.players[p].set_hand(self.deck[p * cards_number_per_player:(p + 1) * cards_number_per_player])

    def set_contract(self):
        n_honor_points = self.players[0].count_honor_points()
        s_honor_points = self.players[2].count_honor_points()
        ns_honor_points = n_honor_points + s_honor_points

        e_honor_points = self.players[1].count_honor_points()
        w_honor_points = self.players[3].count_honor_points()
        ew_honor_points = e_honor_points + w_honor_points

        if ns_honor_points > ew_honor_points:
            self.contract.declarer = Positions.North if n_honor_points >= s_honor_points else Positions.South
            self.declarer_honor_points = ns_honor_points
        elif ns_honor_points < ew_honor_points:
            self.contract.declarer = Positions.East if e_honor_points >= w_honor_points else Positions.West
            self.declarer_honor_points = ew_honor_points

    def get_winner(self):
        # card_values = [card.value for card in self.trick.values()]
        # number_of_max = card_values.count(max(card_values))
        trick_with_cards_that_count = \
            {k: self.trick[k] for k in self.trick.keys() if self.trick[k].suit in self.dominant_suit}
        # if number_of_max > 1:
        #     print("Start: ", Positions((self.whose_turn_it_is_to_play.value + 1) % 4))
        #     print(self.dominant_suit)
        #     print([str(pos) + " " + str(card) for card, pos in zip(self.trick.values(), self.trick.keys())])
        #     print("Winner: ", max(trick_with_cards_that_count, key=trick_with_cards_that_count.get), "\n")
        return max(trick_with_cards_that_count, key=trick_with_cards_that_count.get)

    def play_a_card(self, card):
        position = self.whose_turn_it_is_to_play
        self.trick[position] = card
        self.number_of_played_cards += 1

        if self.number_of_played_cards % 4 == 1:
            self.dominant_suit = [card.suit]

        if self.number_of_played_cards % 4 == 0:
            winner_position = self.get_winner()
            if winner_position == Positions.North or winner_position == Positions.South:
                self.scores["NS"] += 1
            else:
                self.scores["EW"] += 1
        self.whose_turn_it_is_to_play = Positions((self.whose_turn_it_is_to_play.value + 1) % 4)
        self.done = self.number_of_played_cards == len(self.deck)

    def reset_trick(self):
        self.trick = {position: None for position in Positions}

    def trick_to_list(self):
        return [cards.observation() if cards is not None else 0 for cards in self.trick.values()]

    def trick_history_to_list(self):
        return [[cards.observation() for cards in tricks.values()] for tricks in self.trick_history]

    def observation(self, position):
        return [self.players[position.value].list_hand(),
                self.players[(position.value + 2) % 4].list_hand(),
                self.trick_to_list(),
                self.trick_history_to_list()]


if __name__ == '__main__':
    game = Game()
    pass
