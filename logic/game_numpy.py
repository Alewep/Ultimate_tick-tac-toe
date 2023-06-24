import numpy as np

winning_combinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]
MAX_HEURISTIQUE = 24


def local_heuristic(board):
    values = np.take(board, winning_combinations)
    no_negative_ones = np.all(values != -1, axis=1)
    total_score_player = np.sum(values[no_negative_ones], axis=1).sum()

    values = np.take(board * -1, winning_combinations)
    no_negative_ones = np.all(values != -1, axis=1)
    total_score_opponent = np.sum(values[no_negative_ones], axis=1).sum()

    return total_score_player - 1.1*total_score_opponent


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
            if self.big_board[grid_num] != 0:
                continue

            start = grid_num * self.block_size_squared
            end = start + self.block_size_squared
            subgrid = self.board[start:end]

            for combination in winning_combinations:
                sums = subgrid[combination].sum()
                if sums == 3:
                    self.big_board[grid_num] = 1
                    break
                if sums == -3:
                    self.big_board[grid_num] = -1
                    break

    def play(self, i, j=None, player=1):
        if j is None:
            index = i
        else:
            index = self.coordinate_to_index(i, j)
        if self.board[index] == 0:
            if player == 1 or player == -1:
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
        self.board[index] = 0
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

    def evaluate(self):
        self.update_big_board()
        for combination in winning_combinations:
            sums = self.big_board[combination].sum()
            if sums == 3:
                return 1
            if sums == -3:
                return -1
        return 0

    def terminate(self):
        return self.evaluate() != 0 or self.turn == (self.block_size_squared * self.n_block_squared)

    def validate_actions(self):
        grid_num = self.last_play % self.block_size_squared
        self.update_big_board()

        if self.last_play >= 0 and self.big_board[grid_num] == 0:
            start = grid_num * self.block_size_squared
            end = (grid_num + 1) * self.block_size_squared
            subgrid = self.board[start:end]

            return np.where(subgrid == 0)[0] + (grid_num * self.block_size_squared)

        else:
            all_valid = np.where(self.board == 0)[0]
            valid_actions = all_valid[self.big_board[all_valid // self.block_size_squared] == 0]

        return valid_actions

    def heuristic(self):
        # TODO: Implement a system to save heuristic values per game turn and depth.

        self.update_big_board()
        for grid_num in self.valuation_to_update:
            if self.big_board[grid_num] != 0:
                self.valuation[grid_num] = MAX_HEURISTIQUE * self.big_board[grid_num]
            else:
                start = grid_num * self.block_size_squared
                end = start + self.block_size_squared
                subgrid = self.board[start:end]
                self.valuation[grid_num] = local_heuristic(subgrid)

        self.valuation_to_update.clear()
        return local_heuristic(self.valuation)
