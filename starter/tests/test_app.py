import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import app as app_module
import sudoku_logic


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_current():
    app_module.CURRENT["puzzle"] = None
    app_module.CURRENT["solution"] = None
    yield
    app_module.CURRENT["puzzle"] = None
    app_module.CURRENT["solution"] = None


def test_index_page_renders(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Sudoku Game" in response.data


def test_new_game_returns_puzzle(client):
    response = client.get("/new")
    assert response.status_code == 200
    data = response.get_json()
    assert "puzzle" in data

    puzzle = data["puzzle"]
    assert len(puzzle) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)


def test_check_solution_reports_incorrect_cells(client):
    solution = [[(row * 3 + row // 3 + col) % 9 + 1 for col in range(9)] for row in range(9)]
    app_module.CURRENT["solution"] = solution

    board = [[0 for _ in range(9)] for _ in range(9)]
    response = client.post("/check", json={"board": board})

    assert response.status_code == 200
    payload = response.get_json()
    assert "incorrect" in payload
    assert len(payload["incorrect"]) > 0
