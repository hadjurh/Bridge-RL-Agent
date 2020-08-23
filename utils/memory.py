import sys
import datetime
import os


def write_file(step, set_size, observation_list, action_list, score_list, unique_id):
    print("Step: " + str(step), file=sys.stderr)

    now = datetime.datetime.now()
    time_str = str(now)[0:10] + "_" + str(now)[11:23].replace(":", "-").replace(".", "-")

    if not os.path.exists('database'):
        os.makedirs('database')

    file_game = open("database/no_trump_" + str(set_size) + "_" +
                     time_str + "_" + unique_id +
                     ".game", "w")
    file_score = open("database/no_trump_" + str(set_size) + "_" +
                      time_str + "_" + unique_id +
                      ".score", "w")

    file_game.write(''.join((str(observation) + "\n" + str(action) + "\n")
                            for observation, action in zip(observation_list, action_list)))
    file_score.write(''.join((str(score) + "\n")
                             for score in score_list))
