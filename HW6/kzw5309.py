############################################################
# CMPSC 442: Homework 6
############################################################

student_name = "Kun Wang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import email
from collections import defaultdict
import math
import os



############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    f = open(email_path, "r")
    msgs = email.message_from_file(f)
    body = email.iterators.body_line_iterator(msgs)
    lol = [x.split() for x in body]
    return [i for x in lol for i in x]

def log_probs(email_paths, smoothing):
    dic = defaultdict(float)
    vocabulary_lists = [load_tokens(path) for path in email_paths]
    vocabulary = [v for vlist in vocabulary_lists for v in vlist]

    for v in vocabulary:
        dic[v] += 1

    vocabulary_set = set(vocabulary)
    sum_words = len(vocabulary)
    num_vocabulary = len(vocabulary_set)
    for vs in vocabulary_set:
        dic[vs] = math.log((dic[vs]+smoothing)/(sum_words+smoothing*(num_vocabulary+1)))
    dic["<UNK>"] = math.log(smoothing/(sum_words+smoothing*(num_vocabulary+1)))
    return dic

class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        spam_paths = [os.path.join(spam_dir, f) for f in os.listdir(spam_dir) if os.path.isfile(os.path.join(spam_dir, f))]
        ham_paths = [os.path.join(ham_dir, f) for f in os.listdir(ham_dir) if os.path.isfile(os.path.join(ham_dir, f))]
        self.spam_dic = log_probs(spam_paths, smoothing)
        self.ham_dic = log_probs(ham_paths, smoothing)
        self.prob_spam = math.log(float(len(spam_paths))/(len(ham_paths)+len(spam_paths)))
        self.prob_ham = math.log(float(len(ham_paths))/(len(ham_paths)+len(spam_paths)))
    
    def is_spam(self, email_path):
        vocabulary = load_tokens(email_path)
        prob_joint_spam = self.prob_spam
        prob_joint_ham = self.prob_ham
        for w in vocabulary:
            if w in self.spam_dic:
                prob_joint_spam += self.spam_dic[w]
            else:
                prob_joint_spam += self.spam_dic["<UNK>"]
            if w in self.ham_dic:
                prob_joint_ham += self.ham_dic[w]
            else:
                prob_joint_ham += self.ham_dic["<UNK>"]
        if prob_joint_spam >= prob_joint_ham:
            return True
        else:
            return False

    def most_indicative_spam(self, n):
        i = 0
        most_indicative_s_list = list()
        dic_s = defaultdict()
        for w in self.spam_dic.keys():
            if w in self.ham_dic:
                dic_s[w] = self.spam_dic[w]-math.log(math.exp(self.spam_dic[w])*math.exp(self.prob_spam)+math.exp(self.ham_dic[w])*math.exp(self.prob_ham))
        for key, value in sorted(dic_s.iteritems(), key=lambda (k, v): (v, k), reverse=True):
            if key != "<UNK>":
                most_indicative_s_list.append(key)
                i += 1
                if i >= n:
                    return most_indicative_s_list

    def most_indicative_ham(self, n):
        i = 0
        most_indicative_h_list = list()
        dic = defaultdict()
        for w in self.spam_dic.keys():
            if w in self.ham_dic:
                dic[w] = self.ham_dic[w]-math.log(math.exp(self.spam_dic[w])*math.exp(self.prob_spam)+math.exp(self.ham_dic[w])*math.exp(self.prob_ham))
        for key, value in sorted(dic.iteritems(), key=lambda (k, v): (v, k), reverse=True):
            if key != "<UNK>":
                most_indicative_h_list.append(key)
                i += 1
                if i >= n:
                    return most_indicative_h_list

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
It takes me about 5 hours to finish this homework
"""

feedback_question_2 = """
The last section to find most indicative words is the most challenging. 
"""

feedback_question_3 = """
This assignment contains the most details among all homework until now. Add a instruction for how to test the filter with dev data.
"""
