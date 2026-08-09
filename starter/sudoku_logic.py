import copy
import random

SIZE = 9
EMPTY = 0

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True


def is_valid_board(board):
    for row in range(SIZE):
        seen = [False] * (SIZE + 1)
        for col in range(SIZE):
            value = board[row][col]
            if value == EMPTY:
                continue
            if seen[value]:
                return False
            seen[value] = True

    for col in range(SIZE):
        seen = [False] * (SIZE + 1)
        for row in range(SIZE):
            value = board[row][col]
            if value == EMPTY:
                continue
            if seen[value]:
                return False
            seen[value] = True

    for box_row in range(0, SIZE, 3):
        for box_col in range(0, SIZE, 3):
            seen = [False] * (SIZE + 1)
            for row in range(box_row, box_row + 3):
                for col in range(box_col, box_col + 3):
                    value = board[row][col]
                    if value == EMPTY:
                        continue
                    if seen[value]:
                        return False
                    seen[value] = True

    return True


def count_solutions(board, limit=2):
    if not is_valid_board(board):
        return 0

    best_row = None
    best_col = None
    best_candidates = None

    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] != EMPTY:
                continue
            candidates = [
                candidate
                for candidate in range(1, SIZE + 1)
                if is_safe(board, row, col, candidate)
            ]
            if not candidates:
                return 0
            if best_candidates is None or len(candidates) < len(best_candidates):
                best_row = row
                best_col = col
                best_candidates = candidates
                if len(best_candidates) == 1:
                    break
        if best_candidates is not None and len(best_candidates) == 1:
            break

    if best_candidates is None:
        return 1

    solutions = 0
    for candidate in best_candidates:
        board[best_row][best_col] = candidate
        solutions += count_solutions(board, limit)
        board[best_row][best_col] = EMPTY
        if solutions >= limit:
            return solutions

    return solutions


def has_unique_solution(board):
    return count_solutions(deep_copy(board), limit=2) == 1


def remove_cells(board, clues):
    cells = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(cells)
    removed = 0

    for row, col in cells:
        if removed >= SIZE * SIZE - clues:
            break
        if board[row][col] == EMPTY:
            continue

        value = board[row][col]
        board[row][col] = EMPTY
        if not has_unique_solution(board):
            board[row][col] = value
        else:
            removed += 1


def generate_puzzle(clues=35):
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    return puzzle, solution
