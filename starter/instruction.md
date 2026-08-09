# Project Instructions for Copilot

## Project
- This project is a Flask-based Sudoku game.
- The backend uses Python and Flask.
- The frontend uses HTML, vanilla JavaScript, and CSS.
- Keep the application simple, modular, readable, and maintainable.

## Coding Conventions
- Use clear and descriptive names for variables, functions, and files.
- Use Python type hints for function parameters and return values where appropriate.
- Keep Flask route handlers focused on handling requests and responses.
- Keep Sudoku/game logic in reusable functions rather than putting all logic inside routes.
- Add comments when they help explain non-obvious logic.
- Handle invalid input and errors gracefully.
- Avoid unnecessary dependencies or frameworks.
- Preserve existing functionality when refactoring code.

## Sudoku Rules
- The Sudoku board is a 9x9 grid.
- Empty cells must be handled consistently with the existing application.
- Each row must contain the numbers 1 through 9 without duplicates.
- Each column must contain the numbers 1 through 9 without duplicates.
- Each 3x3 box must contain the numbers 1 through 9 without duplicates.
- Generated puzzles must have one unique solvable solution.
- Validate Sudoku solutions using reliable solving/validation logic rather than guesswork.
- Prefilled cells must remain locked and cannot be changed by the player.
- Invalid moves should provide clear visual feedback.

## Testing
- Use pytest for automated tests.
- Test both Flask application behavior and Sudoku game logic.
- Add tests when modifying important game functionality.
- Run the test suite after significant changes.

## Frontend
- Use vanilla JavaScript and CSS unless the existing project requires otherwise.
- Keep the Sudoku interface responsive and accessible.
- Preserve the existing game behavior while improving the UI.
- Ensure the 3x3 Sudoku boxes are visually distinguishable.

## What Not To Do
- Do not introduce unnecessary libraries or frameworks.
- Do not use jQuery or other legacy JavaScript libraries.
- Do not use global mutable state for game data when it can be avoided.
- Do not remove existing functionality during refactoring.
- Do not make unrelated changes to the project.