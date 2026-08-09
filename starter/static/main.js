// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const STORAGE_KEY = 'sudoku-high-scores';
let puzzle = [];
let gameStartTime = Date.now();
let checkCount = 0;
let highScores = [];

function loadHighScores() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) {
      return [];
    }
    const parsed = JSON.parse(stored);
    if (!Array.isArray(parsed)) {
      return [];
    }
    return parsed
      .filter(item => item && typeof item.name === 'string' && typeof item.score === 'number')
      .sort((a, b) => b.score - a.score)
      .slice(0, 10);
  } catch (error) {
    console.warn('Unable to load high scores', error);
    return [];
  }
}

function saveHighScores(scores) {
  highScores = scores;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(scores));
  renderHighScores();
}

function renderHighScores() {
  const list = document.getElementById('high-scores-list');
  if (!list) {
    return;
  }
  list.innerHTML = '';
  if (highScores.length === 0) {
    const item = document.createElement('li');
    item.textContent = 'No scores yet';
    list.appendChild(item);
    return;
  }
  highScores.forEach((entry, index) => {
    const item = document.createElement('li');
    item.textContent = `${index + 1}. ${entry.name} — ${entry.score}`;
    list.appendChild(item);
  });
}

function isTopScore(score) {
  return highScores.length < 10 || score > highScores[highScores.length - 1].score;
}

function addHighScore(name, score) {
  if (!isTopScore(score)) {
    return false;
  }
  const updatedScores = [...highScores, {name, score}]
    .sort((a, b) => b.score - a.score)
    .slice(0, 10);
  saveHighScores(updatedScores);
  return true;
}

function getCurrentScore() {
  const elapsedSeconds = Math.max(1, Math.floor((Date.now() - gameStartTime) / 1000));
  return Math.max(100, 1000 - (elapsedSeconds * 5) - (checkCount * 10));
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

async function newGame() {
  const res = await fetch('/new');
  const data = await res.json();
  renderPuzzle(data.puzzle);
  gameStartTime = Date.now();
  checkCount = 0;
  document.getElementById('message').innerText = '';
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  checkCount += 1;
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    }
  }
  if (incorrect.size === 0) {
    const playerName = document.getElementById('player-name').value.trim() || 'Anonymous';
    const score = getCurrentScore();
    const entered = addHighScore(playerName, score);
    msg.style.color = '#388e3c';
    msg.innerText = entered
      ? `Congratulations! You solved it! New high score saved for ${playerName}.`
      : `Congratulations! You solved it! Your score was ${score}.`;
  } else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

// Wire buttons
window.addEventListener('load', () => {
  highScores = loadHighScores();
  renderHighScores();
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  // initialize
  newGame();
});