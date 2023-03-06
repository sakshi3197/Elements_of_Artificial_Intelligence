# SeekTruth.py : Classify text objects into two categories
#
# PLEASE PUT YOUR NAMES AND USER IDs HERE
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
import math

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!
    occurences_dict = {}

    def remove_punc(string):
        punc_list = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
        for punc_marks in string:
            if punc_marks in punc_list:
                string = string.replace(punc_marks, "")
        return string

    for k in range(len(train_data["objects"])):
        sentence = train_data["objects"][k]
        cleaned = sentence.strip().lower().split()
        cleaned_p = [remove_punc(k) for k in cleaned]
        for individual_word in cleaned_p:
            if individual_word not in occurences_dict:
                occurences_dict[individual_word] = {}

            if train_data["labels"][k] == "truthful":
                if 'truthful' not in occurences_dict[individual_word]:
                    occurences_dict[individual_word]['truthful'] = 0
                occurences_dict[individual_word]["truthful"] = occurences_dict[individual_word]["truthful"] + 1
            else:
                if 'deceptive' not in occurences_dict[individual_word]:
                    occurences_dict[individual_word]['deceptive'] = 0
                occurences_dict[individual_word]["deceptive"] = occurences_dict[individual_word]["deceptive"] + 1

    final_list = []
    for k in range(len(test_data['objects'])):
        sentence = test_data['objects'][k]
        cleaned_t = sentence.strip().lower().split()
        cleaned_pt = [remove_punc(k) for k in cleaned_t]
        truth_decep_ratio = 1
        for individual_word in cleaned_pt:
            if individual_word not in occurences_dict:
                continue
            else:
                if 'truthful' not in occurences_dict[individual_word] or 'deceptive' not in occurences_dict[individual_word]:
                    continue
                else:
                    truth_decep_ratio = truth_decep_ratio * (occurences_dict[individual_word]['truthful'] / occurences_dict[individual_word]['deceptive'])
        if (truth_decep_ratio > 1):
            final_list.append('truthful')
        else:
            final_list.append('deceptive')

    return final_list

    #return [test_data["classes"][0]] * len(test_data["objects"])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
