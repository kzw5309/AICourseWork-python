import kzw5309
#import kzw5309

print'1'
b = kzw5309.read_board('hw4-medium1.txt')
print b.keys()
print kzw5309.Sudoku(b).get_values((0, 0))
print kzw5309.Sudoku(b).get_values((0, 1))
print kzw5309.Sudoku(b).get_values((8, 7))

print
print '2'
b = kzw5309.sudoku_arcs()
c = kzw5309.sudoku_arcs()
print ((0, 0), (0, 8)) in b
print ((0, 0), (8, 0)) in b
print ((0, 8), (0, 0)) in b
print ((0, 0), (2, 1)) in b
print ((2, 2), (0, 0)) in b
print ((2, 3), (0, 0)) in b
print ((0, 0), (0, 0)) in b
print ((0, 4), (0, 5)) in b

print
print '3'
sudoku = kzw5309.Sudoku(kzw5309.read_board("hw4-easy.txt")) # See below for a picture.
sudoku.get_values((0, 3))
for col in [0, 1, 4]:
    removed = sudoku.remove_inconsistent_values((0, 3), (0, col))
    print removed, sudoku.get_values((0, 3))

print
print '4'
sudoku = kzw5309.Sudoku(kzw5309.read_board("hw4-easy.txt")) # See below for a picture.
print sudoku.infer_ac3()
for i in xrange(9):
    for j in xrange(9):
        print sudoku.get_values((i,j)),
    print

print
print '5'
sudoku = kzw5309.Sudoku(kzw5309.read_board("hw4-medium1.txt")) # See below for a picture.
sudoku.infer_improved()
for i in xrange(9):
    for j in xrange(9):
        print sudoku.get_values((i,j)),
    print

print
print '6'
sudoku = kzw5309.Sudoku(kzw5309.read_board("hw4-medium2.txt")) # See below for a picture.
sudoku.infer_improved()
for i in xrange(9):
    for j in xrange(9):
        print sudoku.get_values((i,j)),
    print

print
print '7'
sudoku = kzw5309.Sudoku(kzw5309.read_board("hw4-medium4.txt")) # See below for a picture.
sudoku.infer_improved()
for i in xrange(9):
    for j in xrange(9):
        print sudoku.get_values((i,j)),
    print

print
print '8'
sudoku = kzw5309.Sudoku(kzw5309.read_board("hw4-medium4.txt")) # See below for a picture.
sudoku.infer_improved()
for i in xrange(9):
    for j in xrange(9):
        print sudoku.get_values((i,j)),
    print

print
print '9'
sudoku = kzw5309.Sudoku(kzw5309.read_board("hw4-hard1.txt")) # See below for a picture.
sudoku.infer_with_guessing()
for i in xrange(9):
    for j in xrange(9):
        print sudoku.get_values((i,j)),
    print

print
print '10'
sudoku = kzw5309.Sudoku(kzw5309.read_board("hw4-hard2.txt")) # See below for a picture.
sudoku.infer_with_guessing()
for i in xrange(9):
    for j in xrange(9):
        print sudoku.get_values((i,j)),
    print