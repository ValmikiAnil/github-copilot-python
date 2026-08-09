import sudoku_logic


def test_create_empty_board_has_expected_size():
    board = sudoku_logic.create_empty_board()
    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_deep_copy_returns_independent_board_copy():
    board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    copied = sudoku_logic.deep_copy(board)

    copied[0][0] = 99
    assert board[0][0] == 1
    assert copied[0][0] == 99


def test_is_safe_accepts_valid_move():
    board = sudoku_logic.create_empty_board()
    assert sudoku_logic.is_safe(board, 0, 0, 1) is True


def test_is_safe_rejects_conflict_in_row():
    board = sudoku_logic.create_empty_board()
    board[0][1] = 1
    assert sudoku_logic.is_safe(board, 0, 0, 1) is False


def test_is_safe_rejects_conflict_in_column():
    board = sudoku_logic.create_empty_board()
    board[1][0] = 1
    assert sudoku_logic.is_safe(board, 0, 0, 1) is False


def test_is_safe_rejects_conflict_in_box():
    board = sudoku_logic.create_empty_board()
    board[1][1] = 1
    assert sudoku_logic.is_safe(board, 0, 0, 1) is False


def test_generate_puzzle_returns_solution_and_puzzle():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)
    assert len(puzzle) == sudoku_logic.SIZE
    assert len(solution) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert all(len(row) == sudoku_logic.SIZE for row in solution)
    assert puzzle != solution


def test_generated_solution_contains_no_empty_cells():
    _, solution = sudoku_logic.generate_puzzle(clues=35)
    assert all(cell != sudoku_logic.EMPTY for row in solution for cell in row)


def test_generated_puzzle_contains_at_least_one_empty_cell():
    puzzle, _ = sudoku_logic.generate_puzzle(clues=35)
    assert any(cell == sudoku_logic.EMPTY for row in puzzle for cell in row)


def test_has_unique_solution_returns_true_for_completed_board():
    board = [[(row * 3 + row // 3 + col) % 9 + 1 for col in range(9)] for row in range(9)]
    assert sudoku_logic.has_unique_solution(board) is True


def test_has_unique_solution_returns_false_for_empty_board():
    board = sudoku_logic.create_empty_board()
    assert sudoku_logic.has_unique_solution(board) is False


def test_generated_puzzle_has_exactly_one_solution():
    puzzle, _ = sudoku_logic.generate_puzzle(clues=35)
    assert sudoku_logic.has_unique_solution(puzzle) is True
