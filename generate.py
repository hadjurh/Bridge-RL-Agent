from game.game import Game, play_card_random
from game.constants import Positions
from utils.memory import write_file
import sys


def main_generate_games(argv, write=True):
    it = int(argv[0])
    games_set_size = int(argv[1])
    unique_id = argv[2]
    observations = []
    actions = []
    scores = []

    succeed_loops = 0
    while succeed_loops <= it - 1:
        game = Game([Positions.North, Positions.South])  # Constrain: North or South is declarer
        # print("Declarer: ", game.contract.declarer, "---- HP: ", game.declarer_honor_points)

        while True:
            current_player = game.players[game.whose_turn_it_is_to_play.value]

            if game.whose_turn_it_is_to_play in [Positions.North, Positions.South]:
                observations.append(game.observation(game.whose_turn_it_is_to_play))

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
                # Only save positive games
                if game.scores["NS"] >= game.contract.level:
                    succeed_loops += 1
                    scores.append(str([game.contract.level, game.scores["NS"], game.scores["EW"]]))
                    observations = observations[:-2]
                    actions = actions[:-2]
                else:
                    observations = observations[:-26]
                    actions = actions[:-26]
                break

        # Memory buffer
        if succeed_loops % games_set_size == 0 and write and not scores == []:
            write_file(succeed_loops, games_set_size, observations, actions, scores, unique_id)
            observations = []
            actions = []
            scores = []


if __name__ == '__main__':
    main_generate_games(sys.argv[1:], write=True)

