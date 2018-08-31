import kzw5309

print
print "1.2"
p = kzw5309.TilePuzzle([[1,2], [3,0]])
print p.get_board()

p = kzw5309.TilePuzzle([[0,1], [3,2]])
print p.get_board()

print
print "1.3"
p = kzw5309.create_tile_puzzle(3,3)
print p.get_board()

p = kzw5309.create_tile_puzzle(2,4)
print p.get_board()

print
print "1.4"
p = kzw5309.create_tile_puzzle(3,3)
print p.perform_move("up")
print p.get_board()

p = kzw5309.create_tile_puzzle(3,3)
print p.perform_move("down")
print p.get_board()

print
print "1.5"
p = kzw5309.TilePuzzle([[1,2],[3,0]])
print p.is_solved()

p = kzw5309.TilePuzzle([[0, 1], [3, 2]])
print p.is_solved()

print
print "1.6"
p = kzw5309.create_tile_puzzle(3, 3)
p2 = p.copy()
print p.get_board() == p2.get_board()
p.perform_move("left")
print p.get_board() == p2.get_board()

print
print "1.7"
p = kzw5309.create_tile_puzzle(3, 3)
for move, new_p in p.successors():
    print move, new_p.get_board()

print
b = [[1,2,3], [4,0,5], [6, 7, 8]]
p = kzw5309.TilePuzzle(b)
for move, new_p in p.successors():
    print move, new_p.get_board()

print
print "1.8"
b = [[4,1,2], [0,5,3], [7,8,6]]
p = kzw5309.TilePuzzle(b)
print next(p.find_solutions_iddfs())

b = [[1,2,3], [4,0,8], [7,6,5]]
p = kzw5309.TilePuzzle(b)
print list(p.find_solutions_iddfs())

print
print '1.9'
b = [[4,1,2], [0,5,3], [7,8,6]]
p = kzw5309.TilePuzzle(b)
print p.manhattan_distance()
print p.find_solution_a_star()

b = [[1,2,3], [4,0,5], [6,7,8]]
p = kzw5309.TilePuzzle(b)
print p.find_solution_a_star()

'''print
print '2.0'
scene = [[False, False, False],
[False, True , False],
[False, False, False]]
print kzw5309.find_path((0, 0), (2, 1), scene)

scene = [[False, True, False],
[False, True, False],
[False, True, False]]
print kzw5309.find_path((0, 0), (0, 2), scene)'''

scene = [[True, False, False, True, True, False], [False, False, False, True, False, False], [True, False, True, False, False, False], [True, False, False, True, False, False], [True, False, False, False, False, True], [False, False, True, False, False, False], [False, False, False, False, False, True], [False, False, True, True, False, False], [False, True, True, False, False, False], [False, True, False, False, True, True]]
print kzw5309.find_path((0, 1), (9, 2), scene)

print
print '3.0'
print kzw5309.solve_distinct_disks(4, 2)
print kzw5309.solve_distinct_disks(5, 2)
print kzw5309.solve_distinct_disks(4, 3)
print kzw5309.solve_distinct_disks(5, 3)
print kzw5309.solve_distinct_disks(5, 5)
b = kzw5309.solve_distinct_disks(10, 5)
print b
print len(b)

print kzw5309.solve_distinct_disks(7, 5)
print kzw5309.solve_distinct_disks(8, 7)
a = kzw5309.solve_distinct_disks(20, 10)
print a
print len(a)

print
print '4.1'
b = [[False, False], [False, False]]
g = kzw5309.DominoesGame(b)
print g.get_board()

b = [[True, False], [True, False]]
g = kzw5309.DominoesGame(b)
print g.get_board()

print
print '4.2'
g = kzw5309.create_dominoes_game(2, 2)
print g.get_board()

g = kzw5309.create_dominoes_game(2, 3)
print g.get_board()

print
print '4.3'
b = [[False, False], [False, False]]
g = kzw5309.DominoesGame(b)
print g.get_board()
g.reset()
print g.get_board()

b = [[True, False], [True, False]]
g = kzw5309.DominoesGame(b)
print g.get_board()
g.reset()
print g.get_board()

print
print '4.4'
b = [[False, False], [False, False]]
g = kzw5309.DominoesGame(b)
print g.is_legal_move(0, 0, True)
print g.is_legal_move(0, 0, False)

b = [[False, False], [True, False]]
g = kzw5309.DominoesGame(b)
print g.is_legal_move(0, 1, True)
print g.is_legal_move(1, 1, True)

print
print '4.5'
g = kzw5309.create_dominoes_game(3, 3)
print list(g.legal_moves(True))
print list(g.legal_moves(False))

b = [[True, False], [True, False]]
g = kzw5309.DominoesGame(b)
print list(g.legal_moves(True))
print list(g.legal_moves(False))

print
print '4.6'
g = kzw5309.create_dominoes_game(3,3)
g.perform_move(0, 1, True)
print g.get_board()

g = kzw5309.create_dominoes_game(3,3)
g.perform_move(1, 0, False)
print g.get_board()

print
print '4.7'
g = kzw5309.create_dominoes_game(4, 4)
g2 = g.copy()
print g.get_board() == g2.get_board()
g.perform_move(0, 0, True)
print g.get_board() == g2.get_board()

print
print '4.7.1'
b = [[False, False], [False, False]]
g = kzw5309.DominoesGame(b)
print g.game_over(True)
print g.game_over(False)

b = [[True, False], [True, False]]
g = kzw5309.DominoesGame(b)
print g.game_over(True)
print g.game_over(False)

print
print '4.8'
b = [[False, False], [False, False]]
g = kzw5309.DominoesGame(b)
for m, new_g in g.successors(True):
    print m, new_g.get_board()

print
b = [[True, False], [True, False]]
g = kzw5309.DominoesGame(b)
for m, new_g in g.successors(True):
    print m, new_g.get_board()

print
print '4.9'
b = [[False] * 3 for i in range(3)]
g = kzw5309.DominoesGame(b)
print g.get_board()
print g.get_best_move(True, 1)
print g.get_best_move(True, 2)

print
b = [[False] * 3 for i in range(3)]
g = kzw5309.DominoesGame(b)
g.perform_move(0, 1, True)
print g.get_board()
print g.get_best_move(False, 1)
print g.get_best_move(False, 2)

b = [[False] * 4 for i in range(4)]
g = kzw5309.DominoesGame(b)
print g.get_board()
print g.get_best_move(True, 1)
print g.get_best_move(True, 2)
print g.get_best_move(True, 3)
print g.get_best_move(True, 4)
print g.get_best_move(True, 5)
print g.get_best_move(True, 6)
print g.get_best_move(True, 7)
print g.get_best_move(True, 8)
print g.get_best_move(True, 9)

b = [[False] * 4 for i in range(4)]
g = kzw5309.DominoesGame(b)
g.perform_move(0, 1, True)
print g.get_board()
print g.get_best_move(False, 1)
print g.get_best_move(False, 2)
print g.get_best_move(False, 3)
print g.get_best_move(False, 4)
print g.get_best_move(False, 5)
print g.get_best_move(False, 6)
print g.get_best_move(False, 7)
print g.get_best_move(False, 8)
print g.get_best_move(False, 9)