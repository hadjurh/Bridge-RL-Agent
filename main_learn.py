import ast
import json
import sys
import glob
import datetime
import time
from brain.q_learning import QLearningTable


def extract_fulfilled_contracts(file):
    fulfilled_contracts = {}

    with open("database/" + file + ".score") as scores:
        for num, line in enumerate(scores, 1):
                line_list = ast.literal_eval(line)
                contract = line_list[0]
                score = line_list[1]
                if score >= contract:
                    fulfilled_contracts[num // 2] = [contract, score]

    return fulfilled_contracts


def extract_fulfilled_games(file):
    fulfilled_games = {}
    fulfilled_contracts = extract_fulfilled_contracts(file)
    length_of_one_game = 52

    fulfilled_games_range = []
    for contract in fulfilled_contracts.keys():
        fulfilled_games_range += list(range((contract - 1) * length_of_one_game + 1,
                                            contract * length_of_one_game + 1))

    state = []
    with open("database/" + file + ".game") as games:
        for num, line in enumerate(games, 1):
            if num in fulfilled_games_range:
                if len(line) in [2, 3]:
                    contract_index = (num - 1) // 52 + 1
                    game_id = [contract_index,
                               fulfilled_contracts[contract_index][0],
                               fulfilled_contracts[contract_index][1]]

                    action = int(line)
                    if str(game_id) in fulfilled_games.keys():
                        fulfilled_games[str(game_id)].append([state, action])
                    else:
                        fulfilled_games[str(game_id)] = [[state, action]]
                else:
                    state = ast.literal_eval(line)

    return fulfilled_games


if __name__ == '__main__':
    start = time.time()

    # RL agent initialization
    q_agent = QLearningTable()
    next_state = []

    # Find files
    path = sys.argv[1]
    files = glob.glob('database/*.game')

    for file in files:
        file_name_no_extension = file[9:-5]
        fulfilled_games_dict = extract_fulfilled_games(file_name_no_extension)

        for game_id in reversed(list(fulfilled_games_dict.keys())):
            game_id_list = ast.literal_eval(game_id)
            reward = (game_id_list[2] - game_id_list[1] + 1)
            for index, play in enumerate(reversed(fulfilled_games_dict[game_id])):
                action = play[1]
                current_state = play[0]

                q_agent.learn(current_state, action, next_state, reward)

                next_state = current_state

    with open('database/' + str(len(files)) + "_" +
              str(datetime.datetime.now())[0:10] + "_" +
              str(datetime.datetime.now())[11:19].replace(":", "-") + '.json', 'w') as file:
        file.write(json.dumps(q_agent.q_table))

    print(round(time.time() - start, 3), "sec.")
