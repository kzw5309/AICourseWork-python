############################################################
# CMPSC 442: Homework 7
############################################################

student_name = "Kun Wang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import re
from collections import defaultdict
import random
import math


############################################################
# Section 1: Markov Models
############################################################

def tokenize(text):
    return re.findall(r"[\w]+|[^\s\w]", text)

def ngrams(n, tokens):
    list_starts = ["<START>" for i in xrange(n-1)]
    list_end = ["<END>"]
    new_list = list_starts + tokens + list_end
    return [(tuple(new_list[i-1+j] for j in xrange(n) if j > 0), new_list[i+n-1]) for i in xrange(len(tokens)+1)]

class NgramModel(object):

    def __init__(self, n):
        self.model = defaultdict(int)
        self.order = n
        self.context_count = defaultdict(float)
        self.context_members = defaultdict(set)

    def update(self, sentence):
        for x in ngrams(self.order, tokenize(sentence)):
            self.model[x] += 1
            self.context_count[x[0]] += 1
            self.context_members[x[0]].add(x[1])

    def prob(self, context, token):
        return self.model[(context, token)] / self.context_count[context]

    def random_token(self, context):
        sorted_tokens = sorted(self.context_members[context])
        r = random.random()
        left_prob = 0
        for i in xrange(len(sorted_tokens)):
            temp_prob = self.prob(context, sorted_tokens[i])
            new_left_prob = left_prob + temp_prob
            if left_prob <= r < new_left_prob:
                return sorted_tokens[i]
            else:
                left_prob = new_left_prob

    def random_text(self, token_count):
        context_list = ["<START>" for i in xrange(self.order - 1)]
        result_list = []
        for i in xrange(token_count):
            temp_token = self.random_token(tuple(context_list))
            result_list.append(temp_token)
            if temp_token == "<END>":
                context_list = ["<START>" for i in xrange(self.order - 1)]
            elif self.order > 1:
                context_list.pop(0)
                context_list.append(temp_token)

        return " ".join(result_list)

    def perplexity(self, sentence):
        ngrams_sent = ngrams(self.order, tokenize(sentence))
        result = 0
        for x in ngrams_sent:
            if x[0] in self.context_count:
                result += math.log(1.0/self.prob(x[0], x[1]))
        return math.exp(result)**(1.0/len(ngrams_sent))


def create_ngram_model(n, path):
    n_model = NgramModel(n)
    with open(path, 'r') as f:
        for line in f:
            #sentence = line.replace('\n', '')
            n_model.update(line)
    return n_model

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
I spend about 4 hours on this assignment
"""

feedback_question_2 = """
The last section, which ask us to find the perplexity of a sequence of tokens, is the most challenge one. 
"""

feedback_question_3 = """
I do like the section asking us to create ngram model.
"""
