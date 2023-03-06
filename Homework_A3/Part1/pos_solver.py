###################################
# CS B551 Fall 2022, Assignment #3
#
# Your names and user ids:
# Sakshi Sandeep Sitoot : ssitoot
# Dwarakamai Mannemuddu : dwamanne
# Poojitha Mathi : pmathi
# (Based on skeleton code by D. Crandall)
#


import random
import math


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#


class Solver:
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        if model == "Simple":
            return self.get_simple_posterior(sentence, label)
        elif model == "HMM":
            return self.get_viterbi_posterior(list(sentence), list(label))
        elif model == "Complex":
            return self.get_complex_posterior(list(sentence), list(label))
        else:
            print("Unknown algo!")

    def get_simple_posterior(self, words, pos):
        p_value = 0
        for s, l in zip(words, pos):
            p_value = p_value + self.bayes_net_posterior[l + "|" + s]
        return p_value

    def get_viterbi_posterior(self, words, pos):
        s1_probability = math.log10(self.pos_counts[pos[0]] / sum(self.pos_counts.values()))

        emission_probability = 0
        transition_probability = 0

        for i in range(len(pos)):
            emission_probability += math.log10(self.get_emission_probability(words[i], pos[i]))
            if i != 0:
                transition_probability += math.log10(self.get_transition_probability(pos[i - 1], pos[i]))
        return s1_probability + emission_probability + transition_probability

    def get_complex_posterior(self, words, pos):
        s1_probability = math.log10(
            self.pos_counts[pos[0]] / sum(self.pos_counts.values()))

        emission_probability = 0
        transition_probability = 0
        prev_transition_probability = 0

        for i in range(len(pos)):
            emission_probability += math.log10(self.get_emission_probability(words[i], pos[i]))
            if i != 0:
                transition_probability += math.log10(self.get_transition_probability(pos[i - 1], pos[i]))
            if i != 0 and i != 1:
                prev_transition_probability += math.log10(
                    self.get_prev_transition_probability(pos[i - 2], pos[i - 1], pos[i]))

        return s1_probability + emission_probability + transition_probability + prev_transition_probability

    # Do the training!
    #
    def train(self, data):
        POS = ['det', 'adj', 'adv', 'adp', 'conj', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.', ]

        # Simplied Bayes Net
        self.dictionary = set()
        total_words = 0
        pos_counts = {}
        words_given_pos = {}
        emission_count = {}
        transition_count = {}
        previous_pos = None
        prev_prev_pos = None
        before_level_transition_count = {}

        for pos in POS:
            pos_counts[pos] = 0
            words_given_pos[pos] = {}

        for words, tags in data:
            for i in range(len(words)):
                total_words += 1
                pos_counts[tags[i]] += 1
                if words[i] not in self.dictionary:
                    self.dictionary.add(words[i])
                if words[i] not in words_given_pos[tags[i]].keys():
                    words_given_pos[tags[i]][words[i]] = 0
                words_given_pos[tags[i]][words[i]] += 1

                # set emission counts
                if words[i] in emission_count:
                    if tags[i] in emission_count[words[i]]:
                        emission_count[words[i]][tags[i]] += 1
                    else:
                        emission_count[words[i]][tags[i]] = 1
                else:
                    emission_count[words[i]] = {tags[i]: 1}

                # set transition counts
                if previous_pos is not None:
                    if previous_pos in transition_count:
                        if tags[i] in transition_count[previous_pos]:
                            transition_count[previous_pos][tags[i]] += 1
                        else:
                            transition_count[previous_pos][tags[i]] = 1
                    else:
                        transition_count[previous_pos] = {tags[i]: 1}

                # set previous transition counts
                if (prev_prev_pos and previous_pos) is not None:
                    if prev_prev_pos in before_level_transition_count:
                        if previous_pos in before_level_transition_count[prev_prev_pos]:
                            if tags[i] in before_level_transition_count[prev_prev_pos][previous_pos]:
                                before_level_transition_count[prev_prev_pos][previous_pos][tags[i]] = \
                                    before_level_transition_count[prev_prev_pos][previous_pos][tags[i]] + 1
                            else:
                                before_level_transition_count[prev_prev_pos][previous_pos][tags[i]] = 1
                        else:
                            before_level_transition_count[prev_prev_pos][previous_pos] = {tags[i]: 1}
                    else:
                        before_level_transition_count[prev_prev_pos] = {previous_pos: {tags[i]: 1}}

                previous_pos = tags[i]
                if i > 0:
                    prev_prev_pos = tags[i - 1]

        self.emission_count = emission_count
        self.transition_count = transition_count
        self.before_level_transition_count = before_level_transition_count
        self.parts_of_speech = list(transition_count.keys())
        self.pos_counts = pos_counts
        self.words_given_pos = words_given_pos
        self.total_words = total_words

    def get_initial_probability(self, part_of_speech):
        if part_of_speech in self.pos_counts:
            return self.pos_counts[part_of_speech] / sum(
                self.pos_counts.values())
        return 0.000000001

    emission_probabilities = {}

    def get_emission_probability(self, word, part_of_speech):
        # global emission_probabilities
        if word in self.emission_probabilities and part_of_speech in self.emission_probabilities[word]:
            return self.emission_probabilities[word][part_of_speech]

        if word in self.emission_count and part_of_speech in self.emission_count[
            word] and part_of_speech in self.transition_count:
            result = self.emission_count[word][part_of_speech] / sum(self.transition_count[part_of_speech].values())
            self.emission_probabilities[word] = {part_of_speech: result}
            return result
        return 0.000000001

    transition_probabilities = {}

    def get_transition_probability(self, pos1, pos2):
        # global transition_probabilities
        if pos1 in self.transition_probabilities and pos2 in self.transition_probabilities[
            pos1]:
            return self.transition_probabilities[pos1][pos2]

        if pos1 in self.transition_count and pos2 in self.transition_count[pos1] and pos2 in self.transition_count:
            result = self.transition_count[pos1][pos2] / sum(
                self.transition_count[pos1].values())
            return result
        return 0.000000001

    prev_transition_probabilities = {}

    def get_prev_transition_probability(self, pos1, pos2, pos3):
        # global prev_transition_probabilities
        if pos1 in self.prev_transition_probabilities and pos2 in self.prev_transition_probabilities[
            pos1] and pos3 in self.prev_transition_probabilities[pos1][pos2]:
            return self.prev_transition_probabilities[pos1][pos2][pos3]

        if pos1 in self.before_level_transition_count and pos2 in self.before_level_transition_count[pos1] and pos3 in \
                self.before_level_transition_count[pos1][pos2]:
            result = self.before_level_transition_count[pos1][pos2][pos3] / sum(
                self.before_level_transition_count[pos1][pos2].values())
            self.prev_transition_probabilities[pos1] = {pos2: {pos3: result}}
            return result
        return 0.000000001

    # ref:https://towardsdatascience.com/bayesian-inference-and-markov-chain-monte-carlo-sampling-in-python-bada1beabca7
    def create_sample(self, sentence, sample):
        pos = list(self.pos_counts.keys())
        for i in range(len(sentence)):
            prob = [0] * len(pos)
            prob_log = [0] * len(pos)
            for j in range(len(pos)):
                sample[i] = pos[j]
                prob_log[j] = self.get_complex_posterior(sentence, sample)

            min_probability = min(prob_log)
            for k in range(len(prob_log)):
                prob_log[k] -= min_probability
                prob[k] = math.pow(10, prob_log[k])

            probability_sum = sum(prob)
            prob = [x / probability_sum for x in prob]
            rand = random.random()
            probability = 0
            for l in range(len(prob)):
                probability += prob[l]
                if rand < probability:
                    sample[i] = pos[l]
                    break
        return sample

    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):
        # naive bayes
        posterior = dict()
        posterior_copy = dict()
        result = list()
        pos = ["det", "adj", "adv", "adp", "conj", "noun", "num", "pron", "prt", "verb", "x", "."]
        for word in sentence:
            posterior = dict()
            # added Laplace smoothing to handle the problem of zero probability
            for p in range(0, len(pos)):
                posterior[pos[p] + "|" + word] = math.log10(((self.words_given_pos[pos[p]].get(word, 0.0) + 1) /
                                                             (self.pos_counts[pos[p]] + len(self.dictionary))) * (
                                                                    self.pos_counts[pos[p]] / self.total_words))
                posterior_copy[pos[p] + "|" + word] = posterior[pos[p] + "|" + word]
            max_value = max(posterior.values())
            for key, v in posterior.items():
                if v == max_value:
                    k = key.split("|")
                    result.extend([k[0]])
                    break

        self.bayes_net_posterior = posterior_copy
        return result

    # ref: https://github.com/WuLC/ViterbiAlgorithm/blob/master/Viterbi.py
    def hmm_viterbi(self, sentence):
        viterbi = [{}]
        path = {}

        for pos in self.parts_of_speech:
            viterbi[0][pos] = self.get_initial_probability(pos) * self.get_emission_probability(sentence[0], pos)
            path[pos] = [pos]

        for word in range(1, len(sentence)):
            viterbi.append({})
            current_path = {}

            for current_pos in self.parts_of_speech:
                max_value = 0
                for pre_pos in self.parts_of_speech:
                    value = viterbi[word - 1][pre_pos] * self.get_transition_probability(pre_pos,
                                                                                         current_pos) * self.get_emission_probability(
                        sentence[word], current_pos)
                    if value > max_value:
                        max_value = value
                        state = pre_pos
                viterbi[word][current_pos] = max_value
                current_path[current_pos] = path[state] + [current_pos]

            path = current_path

        max_value = -math.inf
        last_word = len(sentence) - 1
        for pos in self.parts_of_speech:
            if viterbi[last_word][pos] >= max_value:
                max_value = viterbi[last_word][pos]
                max_value_state = pos
        state = max_value_state
        return path[state]

    # ref:https://github.com/srinadhu/Gibbs_Sampling/blob/master/Sampler/Gibbs_Sampling.py
    # ref:https://www.youtube.com/watch?v=dZoHsVO4F3k
    def complex_mcmc(self, sentence):
        samples = []
        total_pos = []
        sample = self.simplified(sentence)
        itr = 30
        burn_in = 10

        for i in range(itr):
            sample = self.create_sample(sentence, sample)
            if i >= burn_in:
                samples.append(sample)

        for j in range(len(sentence)):
            count_pos = {}
            for sample in samples:
                if sample[j] in count_pos.keys():
                    count_pos[sample[j]] += 1
                else:
                    count_pos[sample[j]] = 1
            total_pos.append(count_pos)

        max_count_pos = [max(total_pos[i], key=total_pos[i].get) for i in range(len(sentence))]

        final_pos = []
        for pos in max_count_pos:
            final_pos.append(pos.lower())

        return final_pos

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")
