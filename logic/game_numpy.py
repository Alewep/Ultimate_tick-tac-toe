import math

import numpy as np

winning_combinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]
LOSE = -1
WIN = 1
EQUALITY = np.nan
FREE = 0

status_evaluation = {
    LOSE: -1,
    WIN: 1,
    EQUALITY: 0,
    FREE: 0
}


class Game(object):
    def __init__(self, block_size, n_block):
        self.block_size = block_size
        self.n_block = n_block
        self.block_size_squared = self.block_size ** 2
        self.n_block_squared = self.n_block ** 2
        self.board = np.zeros(self.block_size_squared * self.n_block_squared, dtype=int)
        self.big_board = np.zeros(self.n_block_squared, dtype=int)
        self.grid_to_update = set()
        self.valuation = np.zeros(self.n_block_squared)
        self.valuation_to_update = set()
        self.last_play = -1
        self.turn = 0

    def coordinate_to_index(self, row, col):
        grid_row = row // self.block_size
        grid_col = col // self.block_size
        grid_num = grid_row * self.n_block + grid_col

        local_row = row % self.block_size
        local_col = col % self.block_size

        return grid_num * self.block_size_squared + (local_row * self.block_size + local_col)

    def update_big_board(self):

        for grid_num in self.grid_to_update:
            # If this grid is already marked as won by any player, no need to update
            if self.big_board[grid_num] != FREE:
                continue

            start = grid_num * self.block_size_squared
            end = start + self.block_size_squared
            subgrid = self.board[start:end]

            for combination in winning_combinations:
                sums = self.big_board[combination].sum() / 3
                if sums == WIN or sums == LOSE:
                    self.big_board[grid_num] = sums
                    break

            if self.big_board[grid_num] != FREE and np.count_nonzero(subgrid) == self.block_size_squared:
                self.big_board[grid_num] = EQUALITY

    def play(self, i, j=None, player=1):
        if j is None:
            index = i
        else:
            index = self.coordinate_to_index(i, j)
        if self.board[index] == FREE:
            if player == WIN or player == LOSE:
                self.board[index] = player
            else:
                raise ValueError("The player id is not correct")
            self.last_play = index
        else:
            raise ValueError("Cell already occupied")

        self.grid_to_update.add(index // self.n_block_squared)
        self.valuation_to_update.add(index // self.n_block_squared)
        self.turn += 1

    def save_play(self, index, player=1):
        save = [self.last_play,
                self.valuation[index // self.n_block_squared],
                self.big_board[index // self.n_block_squared],
                index, self.grid_to_update.copy(),
                self.valuation_to_update.copy()]
        self.play(index, player=player)
        return save

    def back(self, save):
        self.last_play, valuation, value_big_board, index, self.grid_to_update, self.valuation_to_update = save
        self.board[index] = FREE
        self.big_board[index // self.block_size_squared] = value_big_board
        self.valuation[index // self.block_size_squared] = valuation
        self.turn -= 1

    def index_to_coordinate(self, index):
        grid_num = index // self.block_size_squared

        local_index = index % self.block_size_squared

        grid_row = grid_num // self.n_block
        grid_col = grid_num % self.n_block

        local_row = local_index // self.block_size
        local_col = local_index % self.block_size

        row = grid_row * self.block_size + local_row
        col = grid_col * self.block_size + local_col

        return row, col

    def status(self):
        self.update_big_board()
        for combination in winning_combinations:
            sums = self.big_board[combination].sum() / 3
            if sums == WIN or sums == LOSE:
                return sums

        if np.count_nonzero(self.big_board) == self.block_size_squared:
            return EQUALITY

        return 0

    def validate_actions(self):
        grid_num = self.last_play % self.block_size_squared
        self.update_big_board()

        if self.last_play >= 0 and self.big_board[grid_num] == FREE:
            start = grid_num * self.block_size_squared
            end = (grid_num + 1) * self.block_size_squared
            subgrid = self.board[start:end]

            return np.where(subgrid == FREE)[0] + (grid_num * self.block_size_squared)

        else:
            all_valid = np.where(self.board == FREE)[0]
            valid_actions = all_valid[self.big_board[all_valid // self.block_size_squared] == FREE]

        return valid_actions


def evaluate(status):
    return status_evaluation[status]
