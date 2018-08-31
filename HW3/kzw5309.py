############################################################
# CMPSC 442: Homework 3
############################################################

student_name = "Kun Wang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
import copy
import Queue
import math


############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    board = [[i+cols*j+1 for i in xrange(cols)] for j in xrange(rows)]
    board[rows-1][cols-1]=0
    return TilePuzzle(board)


def swap(x1,y1,x2,y2,board):
    temp = board[y1][x1]
    board[y1][x1] = board[y2][x2]
    board[y2][x2] = temp


class TilePuzzle(object):
    moves = ['up', 'down', 'left', 'right']

    # Required
    def __init__(self, board):
        self.board = board
        self.c = len(board[0])
        self.r = len(board)
        for i in xrange(len(board)):
            for j in xrange(len(board[0])):
                if board[i][j] == 0:
                    self.x=j
                    self.y=i

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        if direction == 'up':
            if self.y > 0:
                swap(self.x,self.y,self.x,self.y-1,self.board)
                self.y = self.y - 1
                return True
            else:
                return False
        elif direction == 'down':
            if self.y < self.r-1:
                swap(self.x,self.y,self.x,self.y+1,self.board)
                self.y = self.y + 1
                return True
            else:
                return False
        elif direction == 'left':
            if self.x > 0:
                swap(self.x, self.y, self.x-1, self.y, self.board)
                self.x = self.x - 1
                return True
            else:
                return False
        elif direction == 'right':
            if self.x < self.c-1:
                swap(self.x, self.y, self.x+1, self.y, self.board)
                self.x = self.x + 1
                return True
            else:
                return False
        else:
            return False

    def scramble(self, num_moves):
        for i in xrange(num_moves):
            self.perform_move(random.choice(TilePuzzle.moves))

    def is_solved(self):
        for i in xrange(self.r):
            for j in xrange(self.c):
                if i == self.r-1 and j == self.c-1:
                    if self.board[i][j] != 0:
                        return False
                else:
                    if self.board[i][j] != j+self.c*i+1:
                        return False
        return True

    def copy(self):
        return copy.deepcopy(self)

    def successors(self):
        for move in TilePuzzle.moves:
            temp = self.copy()
            if temp.perform_move(move):
                yield (move, temp)

    def iddfs_helper(self, limit, moves, visited_states):
        if self.is_solved():
            yield moves
        elif limit == 0:
            yield None
        else:
            visited_states.add(self.convert_to_tuple())
            for move, new_p in self.successors():
                if new_p.convert_to_tuple() not in visited_states:
                    new_moves = moves + [move]
                    for path in new_p.iddfs_helper(limit-1, new_moves, visited_states):
                        yield path

    def convert_to_tuple(self):
        return tuple(tuple(row) for row in self.get_board())

    # Required
    def find_solutions_iddfs(self):
        i = 0
        moves = []
        flag = False
        if self.is_solved():
            yield None
        else:
            while not flag:
                visited_states = set()
                for item in self.iddfs_helper(i, moves, visited_states):
                    if item:
                        flag = True
                        yield item
                i += 1

    def manhattan_distance(self):
        distance = 0
        for i in xrange(self.r):
            for j in xrange(self.c):
                a = self.board[i][j]
                if a != 0:
                    distance += (abs((a-1)/3-i)+abs((a-1)%3-j))
        return distance

    # Required
    def find_solution_a_star(self):
        pqueue = Queue.PriorityQueue()
        visited_states = set()
        pqueue.put((self.manhattan_distance(), self, []))
        visited_states.add(self.convert_to_tuple())
        while not pqueue.empty():
            d, current_state, moves = pqueue.get()
            distance = d - len(moves)
            if distance == 0: #current_state.manhattan_distance() == 0:
                return moves
            for move, new_p in current_state.successors():
                if new_p.convert_to_tuple() not in visited_states:
                    new_moves = moves + [move]
                    pqueue.put((new_p.manhattan_distance()+len(new_moves), new_p, new_moves))
                    visited_states.add(new_p.convert_to_tuple())

############################################################
# Section 2: Grid Navigation
############################################################


def euclidean_distance(point1,point2):
    return math.sqrt(math.pow((point1[0] - point2[0]),2) + math.pow((point1[1]-point2[1]),2))


def perform_move(direction, current_point, scene):
    r = len(scene)
    c = len(scene[0])
    x = current_point[1]
    y = current_point[0]
    waryd = math.sqrt(2)
    if direction == 'up':
        if y > 0 and not scene[y-1][x]:
            return (y-1, x), 1
        else:
            return False
    elif direction == 'down':
        if y < r - 1 and not scene[y+1][x]:
            return (y+1, x), 1
        else:
            return False
    elif direction == 'left':
        if x > 0 and not scene[y][x-1]:
            return (y, x-1), 1
        else:
            return False
    elif direction == 'right':
        if x < c - 1 and not scene[y][x+1]:
            return (y, x+1), 1
        else:
            return False
    elif direction == 'up_left':
        if x > 0 and y > 0 and not scene[y-1][x-1]:
            return (y-1, x-1), waryd
        else:
            return False
    elif direction == 'up_right':
        if x < c-1 and y > 0 and not scene[y-1][x+1]:
            return (y-1, x+1), waryd
        else:
            return False
    elif direction == 'down_left':
        if x > 0 and y < r - 1 and not scene[y+1][x-1]:
            return (y+1, x-1), waryd
        else:
            return False
    elif direction == 'down_right':
        if x < c - 1 and y < r - 1 and not scene[y+1][x+1]:
            return (y+1, x+1), waryd
        else:
            return False
    else:
        return False


def successor(current_point, scene):
    moves = ['up', 'down', 'left', 'right', 'up_left', 'up_right', 'down_left', 'down_right']
    for move in moves:
        temp = perform_move(move, current_point, scene)
        if temp:
            yield temp


def find_path(start, goal, scene):
    if start == goal or scene[start[0]][start[1]] or scene[goal[0]][goal[1]]:
        return None
    pqueue = Queue.PriorityQueue()
    visited_states = set()
    visited_states.add(start)
    start_g = 0
    pqueue.put((euclidean_distance(start,goal), euclidean_distance(start,goal), start_g, [start]))
    while not pqueue.empty():
        f, h, g, points = pqueue.get()
        #print f
        if h == 0:
            #print g
            #print len(points)
            #print f
            return points
        current_point = points[len(points)-1]
        visited_states.add(current_point)
        for next_point, e_d in successor(current_point, scene):
            if next_point not in visited_states:
                #print next_point
                new_points = points + [next_point]
                h = euclidean_distance(next_point, goal)
                new_g = g + e_d
                f = h + new_g
                pqueue.put((f, h, new_g, new_points))
    return None


############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################


def disk_man_distance(state, goal_state):
    distance = 0
    for i in xrange(len(state)):
        d = abs(goal_state[i] - state[i]) / 2 + abs(goal_state[i] - state[i]) % 2
        distance += d
    return distance


def disk_distinct_successor(state, goal_state, distance, length):
    values = state.values()
    for i in state.items():
        k = i[0]
        v = i[1]
        if v + 1 not in values and v + 1 <= length - 1:
            temp = copy.deepcopy(state)
            temp[k] = v + 1
            old = abs(goal_state[k] - state[k]) / 2 + abs(goal_state[k] - state[k]) % 2
            new = abs(goal_state[k] - temp[k]) / 2 + abs(goal_state[k] - temp[k]) % 2
            d = distance - old + new
            yield ((v, v+1), temp, d)
        if v + 1 in values and v + 2 not in values and v + 2 <= length - 1:
            temp = copy.deepcopy(state)
            temp[k] = v + 2
            old = abs(goal_state[k] - state[k]) / 2 + abs(goal_state[k] - state[k]) % 2
            new = abs(goal_state[k] - temp[k]) / 2 + abs(goal_state[k] - temp[k]) % 2
            d = distance - old + new
            yield ((v, v + 2), temp, d)
        if v - 1 not in values and v - 1 >= 0:
            temp = copy.deepcopy(state)
            temp[k] = v - 1
            old = abs(goal_state[k] - state[k]) / 2 + abs(goal_state[k] - state[k]) % 2
            new = abs(goal_state[k] - temp[k]) / 2 + abs(goal_state[k] - temp[k]) % 2
            d = distance - old + new
            yield ((v, v-1), temp, d)
        if v - 1 in values and v - 2 not in values and v - 2 >= 0:
            temp = copy.deepcopy(state)
            temp[k] = v - 2
            old = abs(goal_state[k] - state[k]) / 2 + abs(goal_state[k] - state[k]) % 2
            new = abs(goal_state[k] - temp[k]) / 2 + abs(goal_state[k] - temp[k]) % 2
            d = distance - old + new
            yield ((v, v - 2), temp, d)


def solve_distinct_disks(length, n):
    if length < n or length <= 0 or n <= 0:
        return None
    initial_state = {i: i for i in xrange(n)}
    goal_state = {length-i-1: i for i in xrange(length - n, length)}
    #print initial_state
    #print goal_state
    pqueue = Queue.PriorityQueue()
    tested_states = set()
    tested_states.add(tuple(initial_state.items()))
    f_h = disk_man_distance(initial_state, goal_state)
    pqueue.put((f_h, f_h, initial_state, []))
    while not pqueue.empty():
        f, h, current_state, moves = pqueue.get()
        #print h
        if h == 0:
            return moves
        #print current_state
        #print list(disk_distinct_successor(current_state, goal_state, h, length))
        for move, next_state, new_distance in disk_distinct_successor(current_state, goal_state, h, length):
            next_tuple = tuple(next_state.items())
            if next_tuple not in tested_states:
                new_moves = moves + [move]
                #print new_moves
                #print next_tuple
                #distance = disk_man_distance(next_state, goal_state)
                new_f = new_distance + len(new_moves)
                tested_states.add(next_tuple)
                pqueue.put((new_f, new_distance, next_state, new_moves))
    return None


############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    board = [[False for i in xrange(cols)] for j in xrange(rows)]
    return DominoesGame(board)

class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.c = len(board[0])
        self.r = len(board)

    def get_board(self):
        return self.board

    def reset(self):
        self.board = [[False for i in xrange(self.c)] for j in xrange(self.r)]

    def is_legal_move(self, row, col, vertical):
        if row < 0 or row >= self.r or col < 0 or col >= self.c:
            return False
        if vertical:
            if row + 1 >= self.r:
                return False
            if self.board[row][col] or self.board[row+1][col]:
                return False
            else:
                return True
        else:
            if col + 1 >= self.c:
                return False
            if self.board[row][col] or self.board[row][col+1]:
                return False
            else:
                return True

    def legal_moves(self, vertical):
        for y in xrange(self.r):
            for x in xrange(self.c):
                if self.is_legal_move(y, x, vertical):
                    yield (y, x)

    def perform_move(self, row, col, vertical):
        if self.is_legal_move(row,col,vertical):
            if vertical:
                self.board[row][col] = True
                self.board[row+1][col] = True
            else:
                self.board[row][col] = True
                self.board[row][col+1] = True

    def game_over(self, vertical):
        if len(list(self.legal_moves(vertical))) > 0:
            return False
        else:
            return True

    def copy(self):
        return copy.deepcopy(self)

    def successors(self, vertical):
        for y, x in self.legal_moves(vertical):
            new_game = self.copy()
            new_game.perform_move(y,x,vertical)
            yield ((y,x), new_game)

    def get_random_move(self, vertical):
        y, x = random.choice(list(self.legal_moves(vertical)))
        self.perform_move(y, x, vertical)

    # Required
    def get_best_move(self, vertical, limit):

        a = float('-inf')
        b = float('inf')

        def utility(state):
            return len(list(state.legal_moves(True))) - len(list(state.legal_moves(False)))

        def alphabeta(state, alpha, beta, depth, v):
            best_move = None
            if depth == 0 or state.game_over(v):
                alphabeta.num_nodes += 1
                #print utility(state)
                return None, utility(state), alphabeta.num_nodes
            if v:
                for (y, x), new_game in state.successors(v):
                    old_alpha = alpha
                    #print (y, x, v)
                    alpha = max(alpha, alphabeta(new_game, alpha, beta, depth-1, not v)[1])
                    #print ('alpha', alpha)
                    if alpha != old_alpha:
                        best_move = (y, x)
                    if alpha >= beta:
                        break
                return best_move, alpha, alphabeta.num_nodes
            else:
                for (y, x), new_game in state.successors(v):
                    old_beta = beta
                    #print (y, x, v)
                    #print ('beta', beta)
                    beta = min(beta, alphabeta(new_game, alpha, beta, depth-1, not v)[1])
                    if beta != old_beta:
                        best_move = (y, x)
                    if alpha >= beta:
                        break
                return best_move, beta, alphabeta.num_nodes
        alphabeta.num_nodes = 0

        best_next_move, value, number = alphabeta(self, a, b, limit, vertical)
        if vertical:
            return best_next_move, value, number
        else:
            return best_next_move, -value, number





############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
I spend about 10 hours on this assignment
"""

feedback_question_2 = """
The last section, dominoes game, is the most challenging one for me. 
The significant stumbling block is recursive max-min function.
"""

feedback_question_3 = """
The gui helps a lot when debugging.
"""
