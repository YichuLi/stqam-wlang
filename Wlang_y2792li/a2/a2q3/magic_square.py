'''Magic Square

https://en.wikipedia.org/wiki/Magic_square

A magic square is a n * n square grid filled with distinct positive integers in
the range 1, 2, ..., n^2 such that each cell contains a different integer and
the sum of the integers in each row, column, and diagonal is equal.

'''

from z3 import Solver, sat, unsat, Int, Distinct, Sum


def solve_magic_square(n, r, c, val):
    solver = Solver()

    # CREATE VARIABLES
    X = [[Int('x_%s_%s' % (i, j)) for j in range(n)] for i in range(n)]

    solver.add(Distinct([X[i][j] for j in range(n) for i in range(n)]))
    for i in range(n):
        for j in range(n):
            solver.add(1 <= X[i][j], X[i][j] <= n * n)

    # solver.add(X[i][j] <= n * n for j in range(n) for i in range(n))

    solver.add(X[r][c] == val)

    # rows and columns
    for i in range(n):
        solver.add(Sum([X[i][j] for j in range(n)]) == n * (n * n + 1) / 2)
        solver.add(Sum([X[j][i] for j in range(n)]) == n * (n * n + 1) / 2)

    # diagonals
    solver.add(Sum([X[i][i] for i in range(n)]) == n * (n * n + 1) / 2)
    solver.add(Sum([X[i][n - i - 1] for i in range(n)]) == n * (n * n + 1) / 2)


    # CREATE CONSTRAINTS AND LOAD STORE THEM IN THE SOLVER

    if solver.check() == sat:
        mod = solver.model()
        res = [[mod.evaluate(X[i][j]).as_long() for j in range(n)] for i in range(n)]

        # CREATE RESULT MAGIC SQUARE BASED ON THE MODEL FROM THE SOLVER

        return res
    else:
        return None


def print_square(square):
    '''
    Prints a magic square as a square on the console
    '''
    n = len(square)

    assert n > 0
    for i in range(n):
        assert len(square[i]) == n

    for i in range(n):
        line = []
        for j in range(n):
            line.append(str(square[i][j]))
        print('\t'.join(line))


def puzzle(n, r, c, val):
    res = solve_magic_square(n, r, c, val)
    if res is None:
        print('No solution!')
    else:
        print('Solution:')
        print_square(res)


if __name__ == '__main__':
    n = 3
    r = 1
    c = 1
    val = 5
    puzzle(n, r, c, val)
