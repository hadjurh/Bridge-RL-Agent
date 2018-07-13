import ast
import json
import sys
import os
import glob
import datetime
import time
from brain.q_learning import QLearningTable

if __name__ == '__main__':
    start = time.time()

    # Find files
    path = sys.argv[1]
    files = glob.glob("database/" + path)

    number_of_games = 0

    unique_id = sys.argv[2]

    # RL agent initialization
    q_agent = QLearningTable()

    for file in files:
        print("Current file: " + file, file=sys.stderr)
        file_name_no_extension = file[9:-5]

        index_of_underscores = [i for i, ltr in enumerate(file_name_no_extension) if ltr == "_"]
        number_of_games += int(file_name_no_extension[index_of_underscores[1] + 1:index_of_underscores[2]])

        rewards = []
        with open("database/" + file_name_no_extension + ".score") as scores:
            for line in scores:
                score_list = ast.literal_eval(line)
                rewards.append(score_list[1] - score_list[0] + 1)

        with open(file) as games:
            for num, line in enumerate(games, 1):
                if (num - 1) % 48 == 0 or (num - 2) % 48 == 0:
                    if num > 2 and not num % 2 == 0:
                        q_agent.learn(current_state, action, [], rewards[(num - 1) // 48])
                    if len(line) in [2, 3]:
                        action = int(line)
                    else:
                        current_state = ast.literal_eval(line)
                else:
                    if len(line) in [2, 3]:
                        action = int(line)
                    else:
                        next_state = ast.literal_eval(line)
                        q_agent.learn(current_state, action, next_state, rewards[(num - 1) // 48])
                        current_state = next_state

        q_agent.learn(current_state, action, [], rewards[-1])

        os.remove(str(file))
        os.remove("database/" + file_name_no_extension + ".score")

        with open('database/learn_' + str(number_of_games) + "_" +
                  str(datetime.datetime.now())[0:10] + "_" +
                  str(datetime.datetime.now())[11:23].replace(":", "-").replace(".", "-") + "_" +
                  unique_id + '.json', 'w') as file_learn:
            file_learn.write(json.dumps(q_agent.q_table))

        print(round(time.time() - start, 3), "sec.", file=sys.stderr)
