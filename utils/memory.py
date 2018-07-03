import sys
import datetime


def write_file(step, set_size, observation_list, action_list, score_list):
    print("Step: " + str(step), file=sys.stderr)

    file_game = open("database/no_trump_" + str(set_size) + "_" +
                     str(datetime.datetime.now())[0:10] + "_" +
                     str(datetime.datetime.now())[11:19].replace(":", "-") +
                     ".game", "w")
    file_score = open("database/no_trump_" + str(set_size) + "_" +
                      str(datetime.datetime.now())[0:10] + "_" +
                      str(datetime.datetime.now())[11:19].replace(":", "-") +
                      ".score", "w")
    file_game.write(''.join((str(observation) + "\n" + str(action) + "\n")
                            for observation, action in zip(observation_list, action_list)))
    file_score.write(''.join((str(score) + "\n")
                             for score in score_list))
