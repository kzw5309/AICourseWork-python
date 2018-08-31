############################################################
# CMPSC 442: Homework 2
############################################################

student_name = "Kun Wang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
import copy

############################################################
# Section 1: N-Queens
############################################################


def num_placements_all(n):
    num = 1
    initial = n*n
    for i in xrange(n):
        num *= (initial-i)
        num /= i+1
    return num


def num_placements_one_per_row(n):
    return n**n


def n_queens_valid(board):
    if len(board) != len(set(board)):
        return False
    for i in xrange(len(board)):
        for j in xrange(i+1,len(board)):
            if(abs(board[i]-board[j]) == abs(i-j)):
                return False
    return True


def n_queens_helper(n, board):
    stack = [board]
    while len(stack) > 0:
        current_state = stack.pop()
        for i in xrange(n):
            test_state = current_state + [i]
            if n_queens_valid(test_state):
                if len(test_state) < n:
                    stack.append(test_state)
                elif len(test_state) == n:
                    yield test_state


def n_queens_solutions(n):
    for i in xrange(n):
        for s in n_queens_helper(n,[i]):
            yield s


############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.c = len(board[0])
        self.r = len(board)

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        self.board[row][col] = self.board[row][col] ^ True
        if row-1 >= 0:
            self.board[row - 1][col] = self.board[row - 1][col] ^ True
        if row+1 < self.r:
            self.board[row + 1][col] = self.board[row + 1][col] ^ True
        if col - 1 >= 0:
            self.board[row][col - 1] = self.board[row][col - 1] ^ True
        if col + 1 < self.c:
            self.board[row][col + 1] = self.board[row][col + 1] ^ True

    def scramble(self):
        for i in xrange(self.r):
            for j in xrange(self.c):
                if random.random() <= 0.5:
                    self.perform_move(i, j)

    def is_solved(self):
        for i in xrange(self.r):
            for j in xrange(self.c):
                if self.board[i][j]:
                    return False
        return True

    def copy(self):
        return copy.deepcopy(self)

    def successors(self):
        for i in xrange(self.r):
            for j in xrange(self.c):
                    temp = self.copy()
                    temp.perform_move(i,j)
                    yield ((i, j), temp)

    def find_solution(self):
        visited_states = set()
        queue = [([],self.copy())]
        visited_states.add(self.convert_to_tuple())
        while len(queue)>0:
            current_state = queue.pop(0)
            for move, new_p in current_state[1].successors():
                if new_p.convert_to_tuple() not in visited_states:
                    new_moves = current_state[0]+[move]
                    visited_states.add(new_p.convert_to_tuple())
                    if new_p.is_solved():
                        return new_moves
                    queue.append((new_moves,new_p))
        return None

    def convert_to_tuple(self):
        return tuple(tuple(row) for row in self.get_board())



def create_puzzle(rows, cols):
    return LightsOutPuzzle([[False for i in xrange(cols)] for j in xrange(rows)])

############################################################
# Section 3: Linear Disk Movement
############################################################


def exchange_element_identical(lists, a, b):
    lists[0].remove(a)
    lists[0].add(b)
    lists[1].remove(b)
    lists[1].add(a)


def disk_identical_successor(sets):
    for i in sets[0]:
        if i+1 in sets[1]:
            temp = copy.deepcopy(sets)
            exchange_element_identical(temp, i, i + 1)
            yield ((i,i+1),temp)
        elif i+1 not in sets[1] and i+2 in sets[1]:
            temp = copy.deepcopy(sets)
            exchange_element_identical(temp, i, i + 2)
            yield ((i,i+2),temp)


def exchange_element_distinct(tuplem, k,v, b):
    tuplem[0][k] = b
    tuplem[1].remove(b)
    tuplem[1].add(v)


def disk_distinct_successor(lists):
    for i in lists[0].items():
        k = i[0]
        v = i[1]
        if v + 1 in lists[1]:
            temp = copy.deepcopy(lists)
            exchange_element_distinct(temp, k, v, v+1)
            yield ((v,v+1),temp)
        elif v+1 not in lists[1] and v+2 in lists[1]:
            temp = copy.deepcopy(lists)
            exchange_element_distinct(temp, k, v, v+2)
            yield ((v,v+2),temp)
        elif v - 1 in lists[1]:
            temp = copy.deepcopy(lists)
            exchange_element_distinct(temp, k, v, v-1)
            yield ((v,v-1),temp)
        elif v - 1 not in lists[1] and v - 2 in lists[1]:
            temp = copy.deepcopy(lists)
            exchange_element_distinct(temp, k, v, v - 2)
            yield ((v, v - 2), temp)


def solve_identical_disks(length, n):
    if length < n or length <= 0 or n <= 0:
        return None
    initial_sets = [set(i for i in xrange(n)), set(i for i in xrange(n,length))]
    goal_sets = [set(i for i in xrange(length - n, length)), set(i for i in xrange(length - n))]
    tested_sets = set()
    tested_sets.add(tuple(initial_sets[0]))
    queue = [([],initial_sets)]
    while len(queue) > 0:
        current_state = queue.pop(0)
        for move, new_sets in disk_identical_successor(current_state[1]):
            new_tuple = tuple(new_sets[0])
            if new_tuple not in tested_sets:
                new_moves = current_state[0] + [move]
                if new_sets == goal_sets:
                    return new_moves
                tested_sets.add(new_tuple)
                queue.append((new_moves,new_sets))
    return None


def solve_distinct_disks(length, n):
    if length < n or length <= 0 or n <= 0:
        return None
    initial_sets = ({i: i for i in xrange(n)}, set(i for i in xrange(n, length)))
    goal_sets = ({length-i-1: i for i in xrange(length - n, length)}, set(i for i in xrange(length - n)))
    tested_sets = set()
    tested_sets.add(tuple(initial_sets[0].items()))
    queue = [([], initial_sets)]
    while len(queue) > 0:
        current_state = queue.pop(0)
        for move, new_sets in disk_distinct_successor(current_state[1]):
            new_tuple = tuple(new_sets[0].items())
            if new_tuple not in tested_sets:
                new_moves = current_state[0] + [move]
                if new_sets == goal_sets:
                    return new_moves
                tested_sets.add(new_tuple)
                queue.append((new_moves, new_sets))
    return None

############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
It took me about 7 hours.
"""

feedback_question_2 = """
The last section is the most challenging one for me. I have to think throughly when choosing proper data structure.
"""

feedback_question_3 = """
I like the second part because it provide me with a good example for the future similar implementation.
"""
