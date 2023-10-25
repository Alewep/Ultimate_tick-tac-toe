# Ultimate Tic-Tac-Toe

This project is an implementation of the game Ultimate Tic-Tac-Toe using Python and the NumPy library. The game is played on a grid composed of 9 smaller grids, creating a multi-level game structure.

The objective of the game is to get three identical symbols aligned horizontally, vertically, or diagonally in one of the smaller grids, while following certain game rules to determine which grid to play next.

## Project Structure

The project is organized as follows:

- **`logic/game_numpy.py`**: This file contains the `Game` class that represents the game state, game rules, and associated functionalities such as making a move, evaluating the game state, and generating valid actions.

- **`logic/minimax.py`**: This file contains the implementation of the Minimax algorithm with Alpha-Beta pruning to make decisions in the game.

## Key Features

- **Play against the computer**: You can play against the computer by choosing the cells to play in turn. The computer uses the Minimax algorithm to make its decisions.

- **Game State Management with NumPy**: The game state is managed using the NumPy library, allowing efficient manipulation of multidimensional arrays and facilitating search and evaluation operations.

- **Heuristic analysis** : Research and development on heuristic functions to evaluate the game board.

- **Minimax Algorithm with Alpha-Beta Pruning**: The Minimax algorithm is used to make decisions in the game by evaluating different possible game states up to a certain depth. Alpha-Beta pruning reduces the search in the game tree and improves performance.


## Author

This project was developed by Alexandre MONNIER.

