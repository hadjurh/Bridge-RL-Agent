from game.game import Game, play_card_random
from game.constants import Positions
from game.cards import observation_to_card
import sys
import copy
import json
import glob
import os

path = sys.argv[1]
files = glob.glob("database-" + path)

nb_of_games = int(sys.argv[2])
nb_samples = int(sys.argv[3])

for file in files:
    print(file)
    with open(file) as json_file:
        brain = json.load(json_file)

    known_states = brain.keys()

    for i in range(nb_samples):
        agent_game_won = 0
        random_game_won = 0
        recognized_states = []
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
                        current_card = None

                        # Dominant suit cards both in player's hand and brain
                        # --> The one with highest score
                        brain_player_intersect_dominant = {obs: score for obs, score in brain[observation].items() if
                                                           observation_to_card(int(obs)).suit in game.dominant_suit
                                                           and observation_to_card(int(obs)) in current_player.hand}
                        brain_player_intersect = {obs: score for obs, score in brain[observation].items() if
                                                  observation_to_card(int(obs)) in current_player.hand}

                        if brain_player_intersect_dominant:
                            recognized_states.append(observation)
                            current_card = current_player.play_card(observation_to_card(
                                int(max(brain_player_intersect_dominant, key=brain_player_intersect_dominant.get))))

                        # Dominant suit cards only in player's hand
                        # --> Random
                        elif [card for card in current_player.hand if card.suit in game.dominant_suit]:
                            current_card = play_card_random(current_player, game.dominant_suit,
                                                            game, heuristic_strategy)

                        # No dominant cards in player's hand and other cards known in brain
                        # --> The one with the highest score
                        elif brain_player_intersect:
                            recognized_states.append(observation)
                            current_card = current_player.play_card(observation_to_card(
                                int(max(brain_player_intersect, key=brain_player_intersect.get))))

                        # No dominant cards in player's hand and no other cards known in brain
                        # --> Random
                        elif not [card for card in current_player.hand if card.suit in game.dominant_suit] and \
                                not brain_player_intersect:
                            current_card = play_card_random(current_player, game.dominant_suit, game,
                                                            heuristic_strategy)
                    else:
                        current_card = play_card_random(current_player, game.dominant_suit, game, heuristic_strategy)

                assert current_card is not None
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

        index_of_underscores = [i for i, ltr in enumerate(file) if ltr == "_"]
        number_of_games_learned = int(file[index_of_underscores[0] + 1:index_of_underscores[1]])

        if not os.path.exists('performances'):
            os.makedirs('performances')

        if not os.path.isfile('performances/performances.csv'):
            perf = open('performances/performances.csv', 'a')
            perf.write("Number of learned games" + " ; " +
                       "Number of tested games" + " ; " +
                       "Agent won" + " ; " +
                       "Random won" + " ; " +
                       "Recognized states" + " ; " +
                       "Total states")
            perf.close()

        perf = open('performances/performances.csv', 'a')
        perf.write("\n" + str(number_of_games_learned) + " ; " +
                   str(nb_of_games) + " ; " +
                   str(agent_game_won) + " ; " +
                   str(random_game_won) + " ; " +
                   str(recognized_states.__len__()) + " ; " +
                   str(nb_of_games * 24))
        perf.close()
