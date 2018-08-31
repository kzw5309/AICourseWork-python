############################################################
# CMPSC 442: Homework 8
############################################################

student_name = "Kun Wang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from collections import defaultdict
import math
import os


############################################################
# Section 1: Hidden Markov Models
############################################################
def two_tag_grams(tokens):
    return [tuple([tokens[i][1], tokens[i+1][1]]) for i in xrange(len(tokens)-1)]

def load_corpus(path):
    with open(path, 'r') as f:
        pos_set = list()
        for line in f:
            line = line.replace('\n', '')
            subset = line.split(' ')
            subsetT = [tuple(x.split('=')) for x in subset]
            pos_set.append(subsetT)
        return pos_set

class Tagger(object):

    def __init__(self, sentences):
        self.tag_list = ['ADV','NOUN','ADP','PRON','DET','.','PRT','VERB','X','NUM','CONJ','ADJ']
        self.tag_grams_list = [(x, y) for x in self.tag_list for y in self.tag_list]
        self.pie_dic = defaultdict(float)
        self.transition_dic = defaultdict(lambda: defaultdict(float))
        self.emission_dic = defaultdict(lambda: defaultdict(float))

        tag_set = set(self.tag_list)
        tag_grams_set = set(self.tag_grams_list)
        smoothing = 1e-5
        num_sentence = 0
        num_tokens = 0
        sum_transitions = 0
        num_grams = len(tag_grams_set)

        pie_tag_dic = defaultdict(float)
        two_grams_dic = defaultdict(lambda: defaultdict(float))
        token_dic = defaultdict(lambda: defaultdict(float))
        tag_dic = defaultdict(float)
        tag_prob_dic = defaultdict(float)

        for x in sentences:
            pie_tag_dic[x[0][1]] += 1
            for i in xrange(len(x)):
                if i != len(x) -1:
                    two_grams_dic[x[i][1]][x[i+1][1]] += 1
                    sum_transitions += 1
                token_dic[x[i][1]][x[i]] += 1
                tag_dic[x[i][1]] += 1
                num_tokens += 1
            num_sentence += 1
        print "finish"

        for t in tag_set:
            self.pie_dic[t] = math.log(pie_tag_dic[t] / num_sentence)
            tag_prob_dic[t] = math.log(tag_dic[t] / num_tokens)
        print "pie"

        for g in tag_grams_set:
            self.transition_dic[g[0]][g[1]] = math.log(two_grams_dic[g[0]][g[1]]/tag_dic[g[0]])
        print "grams"


        for t in token_dic.keys():
            temp_num_tag = tag_dic[t]
            temp_num_different_tokens = len(token_dic[t].keys())
            for i in token_dic[t].items():
                self.emission_dic[i[0][0]][t] = math.log((i[1]+smoothing)/(temp_num_tag + smoothing * (temp_num_different_tokens + 1)))
                if i[0][0] == "I":
                    print t
                    print self.emission_dic[i[0][0]][t]
            self.emission_dic["UNK"][t] = math.log(smoothing / (temp_num_tag + smoothing * (temp_num_different_tokens + 1)))
        print "final"

    def most_probable_tags(self, tokens):
        tags_list = list()
        for i in tokens:
            e_i = self.emission_dic[i]
            if e_i:
                tags_list.append(max(e_i, key=e_i.get))
            else:
                tags_list.append("UNK")
        return tags_list

    def viterbi_tags(self, tokens):
        observation_len = len(tokens)
        state_graph_len = len(self.tag_list)
        for i in xrange(len(tokens)):
            e_i = self.emission_dic[tokens[i]]
            if len(e_i) == 0:
                tokens[i] = "UNK"
        print tokens

        viterbi_dic = defaultdict(lambda: defaultdict(float))
        backpointer = defaultdict(lambda: defaultdict(int))
        for s in self.tag_list:
            viterbi_dic[s][0] = self.pie_dic[s] + self.emission_dic[tokens[0]][s]
            backpointer[s][0] = -1
            print self.emission_dic[tokens[0]]["ADV"] == 0
        for t in xrange(1, observation_len):
            for s in self.tag_list:
                prob_list = [viterbi_dic[u][t-1] + self.transition_dic[u][s] + self.emission_dic[tokens[t]][s] for u in self.tag_list]
                viterbi_dic[s][t] = max(prob_list)
                backpointer[s][t] = prob_list.index(viterbi_dic[s][t])
        final_prob_list = [viterbi_dic[u][observation_len-1] for u in self.tag_list]
        viterbi_dic["final"][observation_len-1] = max(final_prob_list)
        backpointer["final"][observation_len-1] = final_prob_list.index(viterbi_dic["final"][observation_len-1])

        result = list()
        previous = self.tag_list[backpointer["final"][observation_len-1]]
        result.append(previous)
        for i in xrange(observation_len-1, 0, -1):
            result.append(previous)
            previous = self.tag_list[backpointer[previous][i]]
            print backpointer[previous][i]
        return list(reversed(result))




############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""
