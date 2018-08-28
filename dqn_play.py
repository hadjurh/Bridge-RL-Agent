from game.game import Game, play_card_random
from game.constants import Positions
from game.cards import observation_to_card
import sys
import copy
import numpy as np
from brain.dqn import DQNAgent

path = sys.argv[1]

memory_agent = DQNAgent(state_size=5, action_size=52)
memory_agent.load(path)

nb_of_games = int(sys.argv[2])
nb_samples = int(sys.argv[3])

for i in range(nb_samples):
    agent_game_won = 0
    random_game_won = 0
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
                observation = game.observation(game.whose_turn_it_is_to_play)
                observation = observation[0] + [observation[1]]
                observation = np.reshape(observation, [1, memory_agent.state_size])

                current_card = observation_to_card(int(np.argmax(memory_agent.model.predict(observation))) + 1)

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

    print("Agent:", agent_game_won)
    print("Random:", random_game_won)
