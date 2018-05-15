from game.game import Game
from game.constants import Positions
import sys

# Options:
# --method
# --size_of_deck
# --fixed_deck
# --training_steps
# --testing_steps
# --plot
# --print


def main_generate_games(argv):
    it = int(argv[0])

    file = open("no_trump" + str(it) + ".game", "w")
    observations = []
    actions = []

    for i in range(it):
        if i % 100000 == 0 and i != 0:
            print("Step:" + str(i))
            file.write(''.join((str(observation) + "\n" + str(action) + "\n")
                               for observation, action in zip(observations, actions)))
            observations = []
            actions = []

        game = Game()
        # print("Declarer: ", game.contract.declarer, "---- HP: ", game.declarer_honor_points, "\n")

        while True:
            current_player = game.players[game.whose_turn_it_is_to_play.value]
            current_card = current_player.play_card_random(game.dominant_suit)

            if game.whose_turn_it_is_to_play in [Positions.North, Positions.South]:
                observations.append(game.observation(Positions.South))
                actions.append(current_card.observation())

            game.play_a_card(current_card)

            if game.number_of_played_cards % 4 == 0:
                game.trick_history.append(game.trick)
                game.whose_turn_it_is_to_play = game.get_winner()
                # print("Winner:", game.get_winner(), "\n")
                game.reset_trick()

            if game.done:
                # print(game.scores, "\n")
                break


if __name__ == '__main__':
    main_generate_games(sys.argv[1:])

# STEPS
# Initialize game parameters (decks, agent players, computer players)
# Learning
# knowledge = method(game, training_steps, mode='learning', knowledge=None)
# Testing
# score = method(game, testing_steps, mode='testing', knowledge=knowledge)
# Plot
