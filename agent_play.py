from game.game import Game, play_card_random
from game.constants import Positions
from game.cards import observation_to_card
import sys
import copy
import json
import glob

path = sys.argv[1]
file = glob.glob("database/" + path)[0]

nb_of_games = int(sys.argv[2])
agent_game_won = 0
random_game_won = 0
recognized_states = []

with open(file) as json_file:
    brain = json.load(json_file)

known_states = brain.keys()

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
                recognized_states.append(observation)
            else:
                current_card = play_card_random(current_player, game.dominant_suit, game, heuristic_strategy)

        game.play_a_card(current_card)

        if game.number_of_played_cards % 4 == 0:
            game.trick_history.append(game.trick)
            game.whose_turn_it_is_to_play = game.get_winner()
            # print("Winner:", game.get_winner(), "\n")
            game.reset_trick()

        if game.done:
            # Only save positive games
            if game.scores["NS"] >= game.contract.level:
                agent_game_won += 1
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
            # Only save positive game_copys
            if game_copy.scores["NS"] >= game_copy.contract.level:
                random_game_won += 1
            break

summary = list()
summary.append("The agent won " + str(agent_game_won) + " games out of " + str(nb_of_games) + ".")
summary.append("Random strategy won " + str(random_game_won) + " games out of " + str(nb_of_games) + ".")
summary.append("\nThe agent recognized " + str(recognized_states.__len__()) + " games out of " + str(nb_of_games * 24) + ":")
for state in recognized_states:
    summary.append(state)

summary.append("\nThe agent won " + str(agent_game_won) + " games out of " + str(nb_of_games) + ".")
summary.append("Random strategy won " + str(random_game_won) + " games out of " + str(nb_of_games) + ".")
summary.append("\nThe agent recognized " + str(recognized_states.__len__()) + " games out of " + str(nb_of_games * 24) + ".")

summary_file = open("database/summary.txt", "w")
summary_file.write(''.join((str(string) + "\n") for string in summary))