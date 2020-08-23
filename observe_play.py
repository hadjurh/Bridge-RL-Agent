from game.game import Game, play_card_random
from game.constants import Positions
from game.cards import observation_to_card
import sys
import copy
import json
import glob

path = sys.argv[1]
files = glob.glob("database/" + path)

nb_of_games = int(sys.argv[2])
nb_samples = int(sys.argv[3])

play_by_play = open('performances/games_play_by_play.txt', 'a')
pbp = ""

for file in files:
    with open(file) as json_file:
        brain = json.load(json_file)

    known_states = brain.keys()

    for i in range(nb_samples):
        print(str(nb_of_games), "(" + str(i + 1) + ")", file=sys.stderr)

        for _ in range(nb_of_games):
            game = Game([Positions.North, Positions.South])
            game_copy = copy.deepcopy(game)

            while True:
                current_player = game.players[game.whose_turn_it_is_to_play.value]
                heuristic_strategy = game.whose_turn_it_is_to_play in [Positions.West, Positions.East]

                if heuristic_strategy:
                    current_card = play_card_random(current_player, game.dominant_suit, game, heuristic_strategy)
                else:
                    observation = str(game.observation(game.whose_turn_it_is_to_play))
                    if observation in known_states:
                        current_card = observation_to_card(int(max(brain[observation])))
                    else:
                        current_card = play_card_random(current_player, game.dominant_suit, game, heuristic_strategy)

                pbp += "\n" + str(game.whose_turn_it_is_to_play)[10:] + " played " + str(current_card) \
                       + "\n" + str([str(card) for card in game.players[game.whose_turn_it_is_to_play.value].hand])
                game.play_a_card(current_card)

                if game.number_of_played_cards % 4 == 0:
                    game.trick_history.append(game.trick)
                    game.whose_turn_it_is_to_play = game.get_winner()
                    # print("Winner:", game.get_winner(), "\n")
                    game.reset_trick()
                    pbp += "\n"

                if game.done:
                    if game.scores["NS"] >= game.contract.level:
                        pbp += "\nAgent won\n\n"
                    else:
                        pbp += "\nAgent lost\n\n"

                    play_by_play.write(pbp)
                    pbp = ""
                    break

            while True:
                current_player = game_copy.players[game_copy.whose_turn_it_is_to_play.value]
                heuristic_strategy = game_copy.whose_turn_it_is_to_play in [Positions.West, Positions.East]

                current_card = play_card_random(current_player, game_copy.dominant_suit, game_copy, heuristic_strategy)
                game_copy.play_a_card(current_card)

                if game_copy.number_of_played_cards % 4 == 0:
                    game_copy.trick_history.append(game_copy.trick)
                    game_copy.whose_turn_it_is_to_play = game_copy.get_winner()
                    # print("Winner:", game_copy.get_winner(), "\n")
                    game_copy.reset_trick()

                if game_copy.done:
                    break

        play_by_play.close()
