import json
import sys
import glob
import copy
import datetime
from random import shuffle

if __name__ == '__main__':
    total_number_of_games = 0

    path = sys.argv[1]
    files = glob.glob("database-" + path)
    files = [f for f in files if f[9:15] != "merged"]
    shuffle(files)

    unique_id = sys.argv[2]

    merged_dictionary = {}

    # TODO gaussian process: well defined distance functions

    for index, file in enumerate(files):
        print("Currently proccessing " + file, file=sys.stderr)

        index_of_underscores = [i for i, ltr in enumerate(file) if ltr == "_"]
        total_number_of_games += int(file[index_of_underscores[0] + 1:index_of_underscores[1]])

        with open(file) as json_file:
            current_dictionary = json.load(json_file)

        if merged_dictionary is {}:
            merged_dictionary = copy.deepcopy(current_dictionary)
        else:
            current_dict_keys = current_dictionary.keys()
            merged_dict_keys = merged_dictionary.keys()

            for key in current_dict_keys:
                if key in merged_dictionary.keys():
                    for sub_key in current_dictionary[key].keys():
                        if sub_key in merged_dictionary[key].keys():
                            merged_dictionary[key][sub_key] = max(current_dictionary[key][sub_key],
                                                                  merged_dictionary[key][sub_key])
                        else:
                            merged_dictionary[key][sub_key] = current_dictionary[key][sub_key]
                else:
                    merged_dictionary[key] = current_dictionary[key]

        with open('database-' + sys.argv[1][:sys.argv[1].find('/')] + '/merged_' +
                  str(total_number_of_games) + "_" +
                  str(datetime.datetime.now())[0:10] + "_" +
                  str(datetime.datetime.now())[11:19].replace(":", "-") + "_" +
                  unique_id + '.json', 'w') as file:
            file.write(json.dumps(merged_dictionary))
