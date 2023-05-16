n = 3
N = n * n

def print_sudoku(board):
    print(("+" + "-" * 11) * 3 + "+")
    for i, row in enumerate(board):
        print(("|" + " {}   {}   {} |" * 3).format(*[x if x != 0 else " " for x in row]))
        if i in {2, 5}:
            print(("|" + "-" * 11) * 3 + "|")
        else:
            if i == 8:
                print(("+" + "-" * 11) * 3 + "+")
            else:
                print("|" + ("   +" * 2 + "   |") * 3)

def find_first_free(board):
    for i, row in enumerate(board):
        for j, e in enumerate(row):
            if e == 0:
                return (i, j)
    return (None, None)

def insert_num(i, j, board):
    i_sq = i - i % n
    j_sq = j - j % n
    for s in range(i_sq, i_sq + n):
        for t in range(j_sq, j_sq + n):
            if i != s and j != t and board[i][j] == board[s][t]:
                return False
    for s in range(0,N):
        if s != i and board[i][j] == board[s][j]:
            return False
        if s != j and board[i][j] == board[i][s]:
            return False
    return True

def next_solution(board):
    (i, j) = find_first_free(board)
    if i == None:
        yield board
        return
    for x in range(1, N + 1):
        board[i][j] = x
        if insert_num(i, j, board) == True:
            yield from next_solution(board.copy())
    board[i][j] = 0


sudoku1 = [
    [9, 6, 3,  8, 0, 4,  2, 7, 0],
    [2, 4, 0,  9, 0, 5,  8, 1, 3],
    [0, 0, 0,  3, 0, 7,  0, 0, 6],

    [7, 2, 0,  6, 8, 0,  0, 0, 0],
    [0, 0, 0,  2, 0, 0,  0, 0, 1],
    [3, 0, 5,  0, 4, 0,  0, 8, 0],

    [0, 0, 0,  4, 0, 0,  5, 2, 0],
    [6, 0, 2,  0, 0, 0,  1, 0, 4],
    [0, 5, 0,  0, 3, 0,  0, 0, 0],
]

sudoku2 = [
    [1, 4, 7,  2, 3, 5,  6, 8, 9],
    [2, 5, 8,  1, 6, 9,  3, 4, 7],
    [3, 6, 9,  4, 7, 8,  2, 1, 5],

    [4, 1, 0,  0, 9, 0,  8, 0, 0],
    [0, 0, 0,  7, 0, 2,  0, 0, 0],
    [0, 3, 0,  0, 0, 1,  0, 6, 0],

    [0, 0, 0,  0, 0, 0,  1, 2, 3],
    [0, 0, 0,  0, 0, 0,  4, 0, 6],
    [6, 0, 0,  0, 0, 0,  7, 0, 0]
]

sudoku3 = [
    [9, 6, 3,  8, 0, 4,  2, 7, 0],
    [2, 4, 0,  9, 0, 5,  8, 1, 3],
    [0, 0, 0,  3, 0, 7,  0, 0, 6],

    [7, 2, 0,  6, 8, 0,  0, 0, 0],
    [0, 0, 0,  2, 7, 0,  0, 0, 1],
    [3, 0, 5,  0, 4, 0,  0, 8, 0],

    [0, 0, 0,  4, 0, 0,  5, 2, 0],
    [6, 0, 2,  0, 0, 0,  1, 0, 4],
    [0, 5, 0,  0, 3, 0,  0, 0, 0],
]

print ("Sudoku 1 :")
for s in next_solution(sudoku1): # only one solution
    print_sudoku(s)
    print ("\n")

print ("Sudoku 2 :")
for s in next_solution(sudoku2): # many solutions
    print_sudoku(s)
    print ("\n")

print ("Sudoku 3 :")
for s in next_solution(sudoku3): # no solutions
    print_sudoku(s)
    print ("\n")




