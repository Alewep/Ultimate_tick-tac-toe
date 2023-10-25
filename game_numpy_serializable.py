from logic.game_numpy import Game
import numpy as np


class GameSerializable(Game):

    def __init__(self, block_size, n_block):
        super().__init__(block_size, n_block)

    def to_dict(self):
        return {
            'block_size': int(self.block_size),
            'n_block': int(self.n_block),
            'block_size_squared': int(self.block_size_squared),
            'n_block_squared': int(self.n_block_squared),
            'board': self.board.astype(int).tolist(),  # Convert numpy array to list of int
            'big_board': self.big_board.astype(int).tolist(),  # Convert numpy array to list of int
            'grid_to_update': list(map(int, self.grid_to_update)),  # Convert all elements to int
            'valuation': list(map(int, self.valuation.tolist())),  # Convert all elements to int
            'valuation_to_update': list(map(int, self.valuation_to_update)),  # Convert all elements to int
            'last_play': int(self.last_play),  # Convert numpy.int64 to int
            'turn': int(self.turn),  # Convert numpy.int64 to int
        }

    @classmethod
    def from_dict(cls, data):
        game = cls(data['block_size'], data['n_block'])
        game.block_size_squared = data['block_size_squared']
        game.n_block_squared = data['n_block_squared']
        game.board = np.array(data['board'])
        game.big_board = np.array(data['big_board'])
        game.grid_to_update = set(data['grid_to_update'])
        game.valuation = np.array(data['valuation'])  # Convert list back to numpy array with int type
        game.valuation_to_update = set(data['valuation_to_update'])
        game.last_play = data['last_play']  # Already in int format
        game.turn = data['turn']  # Already in int format
        return game
