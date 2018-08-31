import kzw5309

print kzw5309.num_placements_all(8)
print kzw5309.num_placements_one_per_row(8)
print kzw5309.n_queens_valid([0,4,1,5,2])
solution = kzw5309.n_queens_solutions(4)
print next(solution)
print next(solution)
print list(kzw5309.n_queens_solutions(6))
print len(list(kzw5309.n_queens_solutions(8)))


b1 = [[True, False], [False, True]]
p1 = kzw5309.LightsOutPuzzle(b1)
b2 = [[True, True], [True, True]]
p2 = kzw5309.LightsOutPuzzle(b2)

print p1.get_board()
print p2.get_board()

p3 = kzw5309.create_puzzle(2,2)
print p3.get_board()

p4 = kzw5309.create_puzzle(2,3)
print p4.get_board()

p5 = kzw5309.create_puzzle(3,3)
p5.perform_move(1,1)
print '3'
print p5.get_board()

p5 = kzw5309.create_puzzle(3,3)
p5.perform_move(0,0)

print p5.get_board()

print '5'
p5 = kzw5309.LightsOutPuzzle(b1)
print p5.is_solved()
p5 = kzw5309.LightsOutPuzzle([[False, False],[False, False]])
print p5.is_solved()

p5 = kzw5309.create_puzzle(3,3)
p6 = p5.copy()
p5.perform_move(0,0)
print '6'
print p5.get_board()
print p6.get_board()
print p5.get_board() == p6.get_board()

print'7'
p7 = kzw5309.create_puzzle(2,2)
for move, new_p in p7.successors():
    print move, new_p.get_board()

for i in range(2, 6):
    p8 = kzw5309.create_puzzle(i, i + 1)
    print len(list(p8.successors()))


print
print'8'
p9 = kzw5309.create_puzzle(2, 3)
for row in xrange(2):
    for col in xrange(3):
        p9.perform_move(row, col)

print p9.find_solution()

b9 = [[False,False,False],[False,False,False]]
b9[0][0] = True
p9 = kzw5309.LightsOutPuzzle(b9)
print p9.find_solution() is None

p9 = kzw5309.create_puzzle(3, 3)
for row in range(3):
    for col in range(3):
        p9.perform_move(row, col)

print p9.find_solution()

print kzw5309.solve_identical_disks(4, 2)
print kzw5309.solve_identical_disks(5, 2)
print kzw5309.solve_identical_disks(4, 3)
print kzw5309.solve_identical_disks(5, 3)
print kzw5309.solve_identical_disks(10, 5)

print('distinct')
print kzw5309.solve_distinct_disks(4, 2)
print kzw5309.solve_distinct_disks(5, 2)
print kzw5309.solve_distinct_disks(4, 3)
print kzw5309.solve_distinct_disks(5, 3)
print kzw5309.solve_distinct_disks(5, 5)
print kzw5309.solve_distinct_disks(10, 5)
