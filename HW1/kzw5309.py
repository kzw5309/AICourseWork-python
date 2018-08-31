############################################################
# CMPSC 442: Homework 1
############################################################

student_name = "Kun Wang"

############################################################
# Section 1: Python Concepts
############################################################

python_concepts_question_1 = """
Python is Strongly typed: 
    Python gives each object a fixed type when it is assigned.
    The operation will not work on two objects with different types.
    Example:  
    x="foo"
    y=2
    z=x+y # it is not allowed

Python is Dynamically typed:
    A variable is defined when it is first assigned.The assigned object automatically determines the type of a variable.
    A variable will always refer to object of any type if assigned an another object. Also, functions do not have type 
    signatures.
    Example:
    x="psu" # x has a type of string
    x=4.5 # the type of x changes to float
"""

python_concepts_question_2 = """
Keys of dictionaries in Python must be immutable, but list is mutable in the first attempt.
Hence, the result is a type error.
My Solution:
points_to_names={(0,0): "home", (1,2):"school", (-1,1):"market"} # use tuples instead of lists
"""

python_concepts_question_3 = """
The concatenate2 function is better. The reason is that strings are immutable, and a new string object must be created
every time you append a string to it, which has space and efficiency cost. In contrast, the concatenate1 function 
takes advantage of 'join' function, which does not need to create new strings during the concatenation. 
Therefore, the concatenate1 which appends strings is slower than the concatenate2.
"""

############################################################
# Section 2: Working with Lists
############################################################

def extract_and_apply(l, p, f):
    return [f(x) for x in l if p(x)]

def concatenate(seqs):
    return [y for x in seqs for y in x]

def transpose(matrix):
    return [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]

############################################################
# Section 3: Sequence Slicing
############################################################

def copy(seq):
    return seq[:]

def all_but_last(seq):
    return seq[:len(seq)-1]

def every_other(seq):
    return seq[::2]

############################################################
# Section 4: Combinatorial Algorithms
############################################################

def prefixes(seq):
    for i in xrange(len(seq)+1):
        yield seq[:i]

def suffixes(seq):
    for i in xrange(len(seq)+1):
        yield seq[i:]

def slices(seq):
    for i in xrange(len(seq)):
        for j in xrange(i, len(seq)):
            j = j+1
            yield seq[i:j]

############################################################
# Section 5: Text Processing
############################################################

def normalize(text):
    result = text.lower()
    result = result.split()
    return " ".join(result)


def no_vowels(text):
    vowels = ("a", "e", "i", "o", "u")
    result = [x for x in text if x.lower() not in vowels]
    return "".join(result)


def digits_to_words(text):
    d = {'1': "one", '2': "two", '3':"three", '4': "four", '5': "five", '6': "six", '7': "seven", '8': "eight"
         , '9': "nine", '0': "zero"}
    result = [d[i] for i in text if i.isdigit()]
    return " ".join(result)


def to_mixed_case(name):
    result = name.strip('_').lower().split('_')
    for i in xrange(len(result)):
        if i != 0:
            result[i] = result[i].capitalize()
    return "".join(result)

############################################################
# Section 6: Polynomials
############################################################


class Polynomial(object):

    def __init__(self, polynomial):
        self.polynomial = tuple((x,y) for x,y in polynomial)

    def get_polynomial(self):
        return self.polynomial

    def __neg__(self):
        return Polynomial([(-x, y) for x, y in self.polynomial])

    def __add__(self, other):
        return Polynomial(self.polynomial + other.get_polynomial())

    def __sub__(self, other):
        return Polynomial([(x, y) for x, y in self.polynomial] + [(-a, b) for a, b in other.get_polynomial()])

    def __mul__(self, other):
        return Polynomial([(x*a, y+b) for x, y in self.polynomial for a,b in other.get_polynomial()])

    def __call__(self, x):
        return sum(a*x**b for a,b in self.polynomial)

    def simplify(self):
        d = {}
        for x, y in self.polynomial:
            d[y] = d.get(y,0)+x
        result = zip(d.values(), d.keys())
        result = sorted(result, key=lambda item: item[1], reverse=True)
        result = tuple((x, y) for x, y in result if x != 0)
        if len(result) == 0:
            result = ((0, 0),)
        self.polynomial = result

    def __str__(self):
        temp = self.polynomial
        container = []
        for i in xrange(len(temp)):
            if temp[i][0] < 0:
                container.append('-')
                if i > 0:
                    container.append(' ')
            elif i > 0:
                container.append('+')
                container.append(' ')
            if abs(temp[i][0]) != 1 or temp[i][1] == 0:
                container.append(str(abs(temp[i][0])))
            if temp[i][1] > 0:
                container.append('x')
            if temp[i][1] > 1:
                container.append('^')
                container.append(str(temp[i][1]))
            if i < len(temp) - 1:
                container.append(" ")
        return "".join(container)










############################################################
# Section 7: Feedback
############################################################

feedback_question_1 = """
I spent 6 hours on this assignment.
"""

feedback_question_2 = """
Section 6 is the most challenging one.
I think the most stumbling part is writing method _str_.
"""

feedback_question_3 = """
I like the Text processing part.
It would be more interesting that "digits_to_words" method can read decimal point.
"""


def find_solution(self):
    visited_states = []
    queue = []
    queue.append(([], self.copy()))
    while len(queue) > 0:
        current_state = queue.pop(0)
        visited_states.append(current_state[1].get_board())
        for move, new_p in current_state[1].successors():
            if new_p.get_board() not in visited_states:
                new_moves = current_state[0] + [move]
                visited_states.append(new_p.get_board())
                print new_moves
                if new_p.is_solved():
                    return new_moves
                queue.append((new_moves, new_p))
    return None