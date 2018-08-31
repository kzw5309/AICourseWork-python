############################################################
# CMPSC 442: Homework 4
############################################################

student_name = "Kun Wang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import copy


############################################################
# Section 1: Sudoku
############################################################


def sudoku_cells():
    return [(i, j) for i in xrange(9) for j in xrange(9)]


def sudoku_block_cells(block_corner):
    x = block_corner[0]
    y = block_corner[1]
    return [(i+x, j+y) for i in xrange(3) for j in xrange(3)]

def sudoku_row_cells(block_corner):
    r = block_corner[0]
    return [(r, i) for i in xrange(9)]

def sudoku_col_cells(block_corner):
    c = block_corner[1]
    return [(j, c) for j in xrange(9)]

def sudoku_arcs():
    arcs = [((x, j), (y, j)) for j in xrange(9) for x in xrange(9) for y in xrange(9)
            if x != y]
    arcs = arcs + [((j, x), (j, y)) for j in xrange(9) for x in xrange(9) for y in xrange(9)
                   if x != y]
    arcs = arcs + [((x, y), (i, j)) for x in xrange(9) for i in xrange(9)
                   for y in xrange(9) for j in xrange(9) if x / 3 == i / 3 if y / 3 == j / 3
                   if not (x == i and y == j)]
    return set(arcs)


def read_board(path):
    dic = {}
    with open(path, 'r') as f:
        i = 0
        for line in f:
            j = 0
            for char in line:
                if char == '*':
                    temp = {i+1 for i in xrange(9)}
                else:
                    temp = {ord(char)-48}
                dic[(i, j)] = temp
                j += 1
            i += 1

    return dic




class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()
    ALLP = {i+1 for i in xrange(9)}

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        c1 = self.board[cell1]
        c2 = self.board[cell2]
        if len(c2) == 1:
            temp = next(iter(c2))
            if temp in c1:
                c1.discard(temp)
                return True
        else:
            return False

    def infer_ac3(self):
        local_ARCS = Sudoku.ARCS
        while len(local_ARCS) > 0:
            temp_arc = local_ARCS.pop()
            if self.remove_inconsistent_values(temp_arc[0], temp_arc[1]):
                if len(self.board[temp_arc[0]]) == 0:
                    return False
                for x in xrange(9):
                    if x != temp_arc[0][1]:
                        local_ARCS.add(((temp_arc[0][0], x), temp_arc[0]))
                    if x != temp_arc[0][0]:
                        local_ARCS.add(((x, temp_arc[0][1]), temp_arc[0]))
                    for y in xrange(9):
                        if x/3 == temp_arc[0][0]/3 and y/3 == temp_arc[0][1]/3 and x != temp_arc[0][0] and y != temp_arc[0][1]:
                            local_ARCS.add(((x, y), temp_arc[0]))
        return True

    def get_row_number(self, x, y):
        row_numbers = set()
        for j in xrange(9):
            if len(self.board[(x, j)]) == 1:
                row_numbers.add(next(iter(self.board[(x, j)])))
        return row_numbers

    def get_col_number(self, x, y):
        col_numbers = set()
        for i in xrange(9):
            if len(self.board[(i, y)]) == 1:
                col_numbers.add(next(iter(self.board[(i, y)])))
        return col_numbers

    def get_block_number(self, x, y):
        block_numbers = set()
        available_cells = set()
        for i in xrange(9):
            for j in xrange(9):
                if x / 3 == i / 3 and y / 3 == j / 3:
                    if len(self.board[(i, j)]) == 1:
                        block_numbers.add(next(iter(self.board[(i, j)])))
                    else:
                        available_cells.add((i, j))

        return block_numbers, available_cells

    def get_available_block_number(self, x, y):
        block_numbers, available_cells = self.get_block_number(x, y)
        total_set = {i + 1 for i in xrange(9)}
        block_numbers = total_set.difference(block_numbers)
        return block_numbers, available_cells

    def get_available_number(self, x, y):
        temp_set = self.get_block_number(x, y)[0].union(self.get_col_number(x, y).union(self.get_row_number(x, y)))
        return self.board[(x, y)].difference(temp_set)

    def infer_improved(self):
        self.infer_ac3()
        revise_needed = False
        for i in self.CELLS:
                if len(self.board[i]) > 1:
                    revise_needed = True
                    break
        while revise_needed:
            revise_needed = False
            for x in self.CELLS:
                if len(self.board[x]) > 1:
                    temp = self.get_available_number(x[0], x[1])
                    self.board[x] = temp

            for i in xrange(3):
                for j in xrange(3):
                    for cell1 in sudoku_block_cells((i*3, j*3)):
                        if len(self.board[cell1]) > 1:
                            union = set()
                            for cell2 in sudoku_block_cells((i*3, j*3)):
                                if cell2 != cell1:
                                    union = union.union(self.board[cell2])
                            temp_d = self.board[cell1].difference(union)
                            if len(temp_d) == 1:
                                revise_needed = True
                                self.board[cell1] = self.board[cell1].intersection(temp_d)
                            else:
                                union = set()
                                for cell3 in sudoku_row_cells(cell1):
                                    if cell3 != cell1:
                                        union = union.union(self.board[cell3])
                                temp_d = self.board[cell1].difference(union)
                                if len(temp_d) == 1:
                                    revise_needed = True
                                    self.board[cell1] = self.board[cell1].intersection(temp_d)
                                else:
                                    union = set()
                                    for cell4 in sudoku_col_cells(cell1):
                                        if cell4 != cell1:
                                            union = union.union(self.board[cell4])
                                    temp_d = self.board[cell1].difference(union)
                                    if len(temp_d) == 1:
                                        revise_needed = True
                                        self.board[cell1] = self.board[cell1].intersection(temp_d)
            self.infer_ac3()
        return not revise_needed




    def infer_with_guessing(self):
        stack = list()
        stack.append(copy.deepcopy(self))
        while len(stack) > 0:
            current = stack.pop()
            current.infer_improved()
            if all([len(current.board[i]) == 1 for i in current.board]):
                self.board = current.board
                return True
            if not any([len(current.board[i]) == 0 for i in current.board]):
                g = [j for j in current.board if len(current.board[j]) > 1][0]
                for k in current.board[g]:
                    successor = copy.deepcopy(current)
                    successor.board[g] = {k}
                    stack.append(successor)
        return False

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
I spend about 10 hours on this assignment.
"""

feedback_question_2 = """
The infer_improved function is the most challenging section. I spend a lot of time on finding a way to accomplish the inference.
"""

feedback_question_3 = """
I like the process of solving puzzles with various difficulty levels. However, I believe this assignment would be better if
there are more details about the inference part of the assignment.
"""
