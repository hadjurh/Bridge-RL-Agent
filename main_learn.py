import ast
import json
import sys
import glob
import datetime
import time
from brain.q_learning import QLearningTable


if __name__ == '__main__':
    start = time.time()

    # RL agent initialization
    q_agent = QLearningTable()
    next_state = []

    # Find files
    path = sys.argv[1]
    files = glob.glob("database/" + path)

    for file in files:
        print(file)
	file_name_no_extension = file[9:-5]

        rewards = []
        with open("database/" + file_name_no_extension + ".score") as scores:
            for line in scores:
                score_list = ast.literal_eval(line)
                rewards.append(score_list[1] - score_list[0] + 1)

        with open(file) as games:
            for num, line in enumerate(games, 1):
                if len(line) in [2, 3]:
                    action = int(line)
                    q_agent.learn(current_state, action, next_state, rewards[(num - 1) // 48])
                    next_state = current_state
                else:
                    current_state = ast.literal_eval(line)

    with open('database/' + str(len(files)) + "_" +
              str(datetime.datetime.now())[0:10] + "_" +
              str(datetime.datetime.now())[11:19].replace(":", "-") + '.json', 'w') as file:
        file.write(json.dumps(q_agent.q_table))

    print(round(time.time() - start, 3), "sec.")
