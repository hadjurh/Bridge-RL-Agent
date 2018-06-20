from game.game import Game, play_card_random
from game.constants import Positions
from utils.memory import write_file
import sys

# Options:
# --method
# --size_of_deck
# --fixed_deck
# --training_steps
# --testing_steps
# --plot
# --print


def main_generate_games(argv, write=True):
    it = int(argv[0])
    games_set_size = int(argv[1])
    observations = []
    actions = []
    scores = []

    for i in range(it):
        game = Game([Positions.North, Positions.South])  # Constrain: North or South is declarer
        # print("Declarer: ", game.contract.declarer, "---- HP: ", game.declarer_honor_points)

        while True:
            current_player = game.players[game.whose_turn_it_is_to_play.value]

            if game.whose_turn_it_is_to_play in [Positions.North, Positions.South]:
                observations.append(game.observation(Positions.South))

            basic_strategy = game.whose_turn_it_is_to_play in [Positions.West, Positions.East]
            current_card = play_card_random(current_player, game.dominant_suit, game, basic_strategy)

            if game.whose_turn_it_is_to_play in [Positions.North, Positions.South]:
                actions.append(current_card.observation())

            game.play_a_card(current_card)

            if game.number_of_played_cards % 4 == 0:
                game.trick_history.append(game.trick)
                game.whose_turn_it_is_to_play = game.get_winner()
                # print("Winner:", game.get_winner(), "\n")
                game.reset_trick()

            if game.done:
                scores.append(str([game.contract.level, game.scores["NS"], game.scores["EW"]]))
                break

        # Memory buffer
        if (i + 1) % games_set_size == 0 and write:
            write_file(i, games_set_size, observations, actions, scores)
            observations = []
            actions = []
            scores = []


if __name__ == '__main__':
    main_generate_games(sys.argv[1:], write=True)

# STEPS
# Initialize game parameters (decks, agent players, computer players)
# Learning
# knowledge = method(game, training_steps, mode='learning', knowledge=None)
# Testing
# score = method(game, testing_steps, mode='testing', knowledge=knowledge)
# Plot
