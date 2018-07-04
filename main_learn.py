import ast
import json
import sys
import glob
import datetime
import time
from brain.q_learning import QLearningTable


if __name__ == '__main__':
    start = time.time()
    total_number_of_games = 0

    # Find files
    path = sys.argv[1]
    files = glob.glob("database/" + path)
    memory = None

    # Check for memory
    if len(sys.argv) == 3:
        name_of_memory_file = glob.glob("database/" + sys.argv[2])[0]
        print("Learning with memory: " + name_of_memory_file)
        with open(name_of_memory_file) as memory_file:
            memory = json.load(memory_file)

        index_of_underscores = [i for i, ltr in enumerate(name_of_memory_file) if ltr == "_"]
        total_number_of_games = int(name_of_memory_file[9:index_of_underscores[0]])

    # RL agent initialization
    q_agent = QLearningTable(memory=memory)
    next_state = []

    for file in files:
        print("Current file: " + file)
        file_name_no_extension = file[9:-5]

        index_of_underscores = [i for i, ltr in enumerate(file_name_no_extension) if ltr == "_"]
        total_number_of_games += int(file_name_no_extension[index_of_underscores[1] + 1:index_of_underscores[2]])
        print("Current total number of games", total_number_of_games)

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

    with open('database/' + str(total_number_of_games) + "_" +
              str(datetime.datetime.now())[0:10] + "_" +
              str(datetime.datetime.now())[11:19].replace(":", "-") + '.json', 'w') as file:
        file.write(json.dumps(q_agent.q_table))

    print(round(time.time() - start, 3), "sec.")
