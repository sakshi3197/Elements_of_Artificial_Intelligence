#!/usr/bin/python
#
# Perform optical individual_alphabet recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
#
# Authors: (insert names here)
# Sakshi Sandeep Sitoot : ssitoot
# Dwarakamai Mannemuddu : dwamanne
# Poojitha Mathi : pmathi
#
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import math
import re

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25
NEGLIGIBLE_VALUE = 0.000000001
ONEFOURTH = 1/4
THREEFOURTH = 3 /4
T = 512

def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    #print(im.size)
    #print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[m, n] < 1 else ' ' for m in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for n in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[m]: letter_images[m] for m in range(0, len(TRAIN_LETTERS) ) }

#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

train_letters_size = len(train_letters)
test_letters_size = len(test_letters)
## Below is just some sample code to show you how the functions above work.
# You can delete this and put your own code here!


# Each training letter is now stored as a list of characters, where black
#  dots are represented by *'s and white dots are spaces. For example,
#  here's what "a" looks like:

#print("\n".join([ r for r in train_letters['a'] ]))

# Same with test letters. Here's what the third single_alphabet of the test data
#  looks like:
#print("\n".join([ r for r in test_letters[2] ]))



# The final two lines of your output should look something like this:
#print("Simple: " + "Sample s1mple resu1t")
#print("   HMM: " + "Sample simple result")

def get_initial_transitional_probabilities(train_txt_fname):
    calculated_initial_probability = {}
    calculated_transitional_probability = {}
    with open(train_txt_fname,'r') as train_txt_fname_opened_file:
        for individual_row in train_txt_fname_opened_file:
            combined_alphabets = list(re.sub(r'[^\w\s]',r' ',' '.join([single_alphabet for single_alphabet in individual_row.split()][0::2])))
            if combined_alphabets:
                if combined_alphabets[0] in calculated_initial_probability.keys():
                    calculated_initial_probability[combined_alphabets[0]] = calculated_initial_probability[combined_alphabets[0]] + 1
                else:
                    calculated_initial_probability[combined_alphabets[0]] = 1
                for position_of_individual_alphabet in range(1,len(combined_alphabets)):
                    if combined_alphabets[position_of_individual_alphabet-1] in calculated_transitional_probability.keys():
                        if combined_alphabets[position_of_individual_alphabet] in calculated_transitional_probability[combined_alphabets[position_of_individual_alphabet-1]].keys():
                            calculated_transitional_probability[combined_alphabets[position_of_individual_alphabet-1]][combined_alphabets[position_of_individual_alphabet]] = calculated_transitional_probability[combined_alphabets[position_of_individual_alphabet-1]][combined_alphabets[position_of_individual_alphabet]] + 1
                        else:
                            calculated_transitional_probability[combined_alphabets[position_of_individual_alphabet-1]][combined_alphabets[position_of_individual_alphabet]] = 1
                    else:
                        calculated_transitional_probability[combined_alphabets[position_of_individual_alphabet-1]] = {combined_alphabets[position_of_individual_alphabet] : 1}
            sum_of_initial_probability = sum(calculated_initial_probability.values())
        for individual_probability in calculated_initial_probability.keys():
            calculated_initial_probability[individual_probability] = calculated_initial_probability[individual_probability]/sum_of_initial_probability
        for a in calculated_transitional_probability:
            transitional_probability_sum = sum(calculated_transitional_probability[a].values())
            for b in calculated_transitional_probability[a]:
                calculated_transitional_probability[a][b] = calculated_transitional_probability[a][b]/transitional_probability_sum

    return (calculated_initial_probability, calculated_transitional_probability)


def get_emission_probability(train_letters, test_letters):
    calculated_emission_probability = {}
    alphabet_bl_test = 0
    alphabet_bl_train = 0
    for position in range(0,test_letters_size):
        calculated_emission_probability[position] =  {}
        for single_alphabet in train_letters:
            alphabet_bl = 0
            alphabet_wh = 0
            number_of_identical_bl = 0
            number_of_identical_wt = 0
            for individual_alphabet in train_letters[single_alphabet]:
                if individual_alphabet == '*':
                    alphabet_bl_train = alphabet_bl_train + 1
            for position_of_alphabet in range(len(test_letters[position])):
                if test_letters[position][position_of_alphabet] == '*':
                    alphabet_bl_test = alphabet_bl_test + 1
                for m in range(0,len(test_letters[position][position_of_alphabet])):
                    if (test_letters[position][position_of_alphabet][m] == train_letters[single_alphabet][position_of_alphabet][m]):
                        if (train_letters[single_alphabet][position_of_alphabet][m] == '*'):
                            alphabet_bl = alphabet_bl + 1
                        elif (train_letters[single_alphabet][position_of_alphabet][m] == ' '):
                            alphabet_wh = alphabet_wh + 1
                    elif (train_letters[single_alphabet][position_of_alphabet][m] == '*'):
                        number_of_identical_bl = number_of_identical_bl + 1
                    elif (train_letters[single_alphabet][position_of_alphabet][m] == ' '):
                        number_of_identical_wt = number_of_identical_wt + 1
            if  alphabet_bl_train/train_letters_size < alphabet_bl_test/test_letters_size:
                calculated_emission_probability[position][single_alphabet] = ((THREEFOURTH ** alphabet_bl) * (THREEFOURTH ** alphabet_wh) * (ONEFOURTH ** number_of_identical_bl) * (ONEFOURTH ** number_of_identical_wt))
            else:
                calculated_emission_probability[position][single_alphabet] = ((0.03 ** number_of_identical_wt) * (0.97 ** alphabet_bl) * (THREEFOURTH ** alphabet_wh) * (ONEFOURTH ** number_of_identical_bl))

    return calculated_emission_probability


####Final Calculation of Simplified and HMM Viterbi
calculated_emission_probability = get_emission_probability(train_letters, test_letters)
appended_simple_result = ''
for individual_probability in calculated_emission_probability:
    appended_simple_result = appended_simple_result + ''.join(max(calculated_emission_probability[individual_probability],key = lambda m: calculated_emission_probability[individual_probability][m]))

NEGLIGIBLE_VALUE = 0.000000001

calculated_initial_probability, calculated_transitional_probability = get_initial_transitional_probabilities(train_txt_fname)
present_alphabet = [None] * T
preceeding_alphabets_list = [None] * T
for test_alphabet_position,test_individual_alphabet in enumerate(test_letters):
    for train_alphabet_position,train_individual_alphabet in enumerate(train_letters):
        if test_alphabet_position == 0:
            appended_HMM_Viterbi_result = -math.log(calculated_emission_probability[0][train_individual_alphabet]) - (math.log(calculated_initial_probability[train_individual_alphabet] if train_individual_alphabet in calculated_initial_probability.keys() else NEGLIGIBLE_VALUE))
            present_alphabet[ord(train_individual_alphabet)] = [appended_HMM_Viterbi_result,[train_individual_alphabet]]
        else:
            use_list = []
            for alphabet_position,alphabet in enumerate(train_letters):
                if alphabet in calculated_transitional_probability.keys():
                    previous_transitional_probability = (-math.log(calculated_transitional_probability[alphabet][train_individual_alphabet] if train_individual_alphabet in calculated_transitional_probability[alphabet].keys() else NEGLIGIBLE_VALUE)) + preceeding_alphabets_list[ord(alphabet)][0]
                else:
                    previous_transitional_probability = (-math.log({}[train_individual_alphabet] if train_individual_alphabet in {}.keys() else NEGLIGIBLE_VALUE)) + preceeding_alphabets_list[ord(alphabet)][0]

                use_list.append([previous_transitional_probability,preceeding_alphabets_list[ord(alphabet)][1] + [train_individual_alphabet]])
            minimum_use_list = min(use_list)
            appended_HMM_Viterbi_result = minimum_use_list[0] - math.log(calculated_emission_probability[test_alphabet_position][train_individual_alphabet])
            present_alphabet[ord(train_individual_alphabet)] = [appended_HMM_Viterbi_result,minimum_use_list[1]]
    preceeding_alphabets_list = present_alphabet
    present_alphabet = [None] * T
temporary_result = [preceeding_single_alphabet for preceeding_single_alphabet in preceeding_alphabets_list if preceeding_single_alphabet is not None]
appended_HMM_Viterbi_result = min(temporary_result)


##Printing both the results
print("Simple: " + appended_simple_result)
print("   HMM: " + ''.join(appended_HMM_Viterbi_result[1]))
