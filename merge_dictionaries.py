import json
import sys
import glob
import copy
import datetime

if __name__ == '__main__':
    path = sys.argv[1]
    files = glob.glob("database/" + path)

    files = [f for f in files if f[9:15] != "merged"]

    merged_dictionary = {}

    update_count = 0

    for file in files:
        print("Currently proccessing " + file)
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
                            update_count += 1

                            if type(merged_dictionary[key][sub_key]) is float:
                                average = (current_dictionary[key][sub_key] + merged_dictionary[key][sub_key]) / 2
                                nb_terms = 2

                            elif type(merged_dictionary[key][sub_key]) is list:
                                nb_terms = merged_dictionary[key][sub_key][1]
                                average = (current_dictionary[key][sub_key] / nb_terms +
                                           merged_dictionary[key][sub_key][0] /
                                           ((nb_terms + 1) / nb_terms))
                                nb_terms += 1

                            merged_dictionary[key][sub_key] = [average, nb_terms]
                        else:
                            merged_dictionary[key][sub_key] = current_dictionary[key][sub_key]
                else:
                    merged_dictionary[key] = current_dictionary[key]

    print(update_count)
    with open('database/merged_' + str(datetime.datetime.now())[0:10] + "_" +
              str(datetime.datetime.now())[11:19].replace(":", "-") + '.json', 'w') as file:
        file.write(json.dumps(merged_dictionary))
