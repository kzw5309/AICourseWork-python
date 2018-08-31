############################################################
# CMPSC442: Homework 4
############################################################

student_name = "Dalton DelPiano"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import math
import Queue
import copy

############################################################
# Section 1: Sudoku
############################################################


def sudoku_cells():
    possible_cells =[]
    for x in range(0, 9):
        for y in range(0, 9):
            possible_cells.append((tuple([x, y])))
    return possible_cells


def sudoku_arcs(regions = [[[] for x in range(9)]for y in range(3)]):
    arcs = []
    for x in range(9):
        for y in range(9):
            for r in range(9):
                if (r, y) != (x, y):
                    arcs.append(tuple([(x, y), (r, y)]))
                    if (r, y) not in regions[0][r]:
                        regions[0][r].append((r, y))
            for c in range(9):
                if (x, c) != (x, y):
                    arcs.append(((x, y), (x, c)))
                    if (x, c) not in regions[1][c]:
                        regions[1][c].append((x, c))
            sqr = int(math.floor(x/3) * 3)
            sqc = int(math.floor(y/3) * 3)

            for r in range(3):
                for c in range(3):
                    if (sqr+r, sqc+c) != (x, y):
                        arcs.append(((x, y), (sqr+r, sqc+c)))
                        if (sqr+r, sqc+c) not in regions[2][sqr + (sqc/3)]:
                            regions[2][sqr + (sqc/3)].append((sqr+r, sqc+c))
    return arcs


def read_board(path):
    file_object = open(path, 'r')
    board = {}
    for x in range(0, 9):
        current_string = file_object.readline()
        for y in range(0, 9):
            if current_string[y] != '*':
                board[tuple([x, y])] = set([int(current_string[y])])
            else:
                board[tuple([x, y])] = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
    file_object.close()
    return board


class Sudoku(object):

    REGIONS = [[[] for x in range(9)]for y in range(3)]
    CELLS = sudoku_cells()
    ARCS = sudoku_arcs(REGIONS)

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        values_removed = False
        cell2values = self.board[cell2]
        if len(cell2values) == 1:
            for x in cell2values:
                if x in self.board[cell1]:
                    self.board[cell1].remove(x)
                    values_removed = True
        return values_removed

    def infer_ac3(self):
        queue = self.ARCS[:]

        while len(queue) != 0:
            cell1, cell2 = queue.pop()
            if self.remove_inconsistent_values(cell1, cell2):
                temp = self.ARCS
                for x, y in temp:
                    if x == cell1:
                        queue.append(tuple([y, cell1]))

    def infer_improved(self):
        changed = True
        while changed:
            self.infer_ac3()
            changed = False
            for r in range(len(self.REGIONS)):
                print self.REGIONS[r]
                for r_c_b in range(len(self.REGIONS[r])):
                    domain = range(0, 9)
                    current = self.REGIONS[r][r_c_b]
                    print self.REGIONS[r][r_c_b]
                    for i in current:
                        if len(self.board[i]) == 1 and list(self.board[i])[0] in domain:
                            domain.remove(list(self.board[i])[0])
                    for d in domain:
                        if sum(list(self.board[k]).count(d) for k in current) == 1:
                            self.board[[k for k in current if list(self.board[k]).count(d) > 0][0]] = set([d])
                            changed = True

    def infer_with_guessing(self):
        queue = Queue.LifoQueue()
        queue.put(copy.deepcopy(self))
        while queue:
            curr = queue.get()
            curr.infer_improved()
            if all([len(curr.board[k]) == 1 for k in curr.board]):
                self.board = curr.board
                return
            if not any([len(curr.board[k]) == 0 for k in curr.board]):
                guesses = [i for i in curr.board if len(curr.board[i]) > 1][0]
                for guess in curr.board[guesses]:
                    succ = copy.deepcopy(curr)
                    succ.board[guesses] = set([guess])
                    queue.put(succ)

# b = read_board('hw4-hard2.txt')
# print ""
# sudoku = Sudoku(b)
# sudoku.infer_with_guessing()
# count = 0
# for x in sorted(sudoku.board):
#     if count % 9 == 0:
#         print ""
#     print list(sudoku.board[x])[0],
#     count = count + 1
# print ""
# for x in sorted(sudoku.board):
#     print x, sudoku.board[x]


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
I spent around 10 hours on this assignment.
"""

feedback_question_2 = """
The aspects of this assignment I found most challenging were deciphering what the prompt
actually wanted us to do. Sometimes it was a bit vague in what it wanted us to implement
so it took a lot of trial and error to understand what I needed to do.
"""

feedback_question_3 = """
I liked this assignment overall, it was pretty enjoyable to create a sudoku solver
and there isn't a whole lot I would change besides maybe being a little more specfic
in the infer_improved part of the prompt.
"""