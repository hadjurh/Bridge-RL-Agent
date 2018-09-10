from game.cards import Card, observation_to_card
from game.constants import Suits, Positions, values, nt_points
from game.player import Player
from game.contract import Contract
from random import shuffle, choice


class Game(object):
    def __init__(self, possible_declarers):
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

        while self.contract.declarer is None or self.contract.declarer not in possible_declarers:
            self.deal()
            self.set_contract()
        self.whose_turn_it_is_to_play = Positions((self.contract.declarer.value + 1) % 4)
        self.contract.level = nt_points[self.declarer_honor_points]

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
            {k: self.trick[k] for k in self.trick.keys()
             if type(self.trick[k]) == Card and self.trick[k].suit in self.dominant_suit}
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
        return [self.trick_to_list(),
                simplify_trick_history(self.trick_history_to_list())]


# The cards to keep explicitly on observations
important_cards = [Card(Suits.Clubs, 12), Card(Suits.Clubs, 13), Card(Suits.Clubs, 14),
                   Card(Suits.Diamonds, 12), Card(Suits.Diamonds, 13), Card(Suits.Diamonds, 14),
                   Card(Suits.Hearts, 12), Card(Suits.Hearts, 13), Card(Suits.Hearts, 14),
                   Card(Suits.Spades, 12), Card(Suits.Spades, 13), Card(Suits.Spades, 14)]
important_cards_number = [card.observation() for card in important_cards]


def simplify_hand(hand):
    filtered_cards = [card_number for card_number in hand if card_number in important_cards_number]
    number_of_other_cards = len(hand) - len(filtered_cards)
    return filtered_cards + [-number_of_other_cards]


def simplify_trick_history(trick_history):
    bytes_array = [1 if card_number in [cards for trick in trick_history for cards in trick]
                   else 0 for card_number in important_cards_number]
    return sum(i * 2 ** (len(bytes_array) - index) for index, i in enumerate(bytes_array))


def play_card_random(player, suit, current_game, basic_strategy=False):
    possible_cards = [cards for cards in player.hand if cards.suit in suit]
    if len(possible_cards) == 0:
        return player.hand.pop(player.hand.index(choice(player.hand)))
    if not basic_strategy:
        return player.hand.pop(player.hand.index(choice(possible_cards)))
    else:
        play_number = current_game.number_of_played_cards % 4

        # Last one to play in the trick and NS is currently winning
        if play_number == 3 and current_game.get_winner() in [Positions.North, Positions.South]:
            # It is possible to win, select the smallest card that wins the trick
            if current_game.trick[current_game.get_winner()] < max(possible_cards):
                selected_cards = [cards for cards in possible_cards
                                  if cards > current_game.trick[current_game.get_winner()]]
            else:
                selected_cards = [min(possible_cards)]

            return player.hand.pop(player.hand.index(choice(selected_cards)))

        elif play_number == 3 and not current_game.get_winner() in [Positions.North, Positions.South]:
            return player.hand.pop(player.hand.index(min(possible_cards)))

        # Not the first nor the last to play in the trick
        elif play_number in [1, 2]:
            already_seen_important_cards = [observation_to_card(cards)
                                            for trick_list in current_game.trick_history_to_list()
                                            for cards in trick_list
                                            if observation_to_card(cards).suit in current_game.dominant_suit]
            strongest_possible_card = max(possible_cards)
            if current_game.trick[current_game.get_winner()] < strongest_possible_card:
                if current_game.get_winner() in [Positions.North, Positions.South]:
                    if strongest_possible_card.value < 14:  # Not an ace
                        already_seen_better_cards = [cards for cards in already_seen_important_cards
                                                     if cards > strongest_possible_card]
                        if list(range(strongest_possible_card.value + 1, 15)) == \
                                [cards.value for cards in already_seen_better_cards]:
                            return player.hand.pop(player.hand.index(strongest_possible_card))
                        else:
                            return player.hand.pop(player.hand.index(choice(possible_cards)))
                    else:
                        return player.hand.pop(player.hand.index(max(possible_cards)))
                else:
                    return player.hand.pop(player.hand.index(choice(possible_cards)))  # TODO choose finesse often
            else:
                return player.hand.pop(player.hand.index(min(possible_cards)))
        else:
            return player.hand.pop(player.hand.index(choice(possible_cards)))


if __name__ == '__main__':
    game = Game([Positions.North, Positions.South])
    pass
