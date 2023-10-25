from logic.game_numpy import Game,winning_combinations
import numpy as np

MAX_HEURISTIQUE = 15


def local_heuristic(board: np.ndarray):
    values = np.take(board, winning_combinations)
    winnable = np.all((values !=-1 ) & (~np.isnan(values)), axis=1)
    total_score_player = np.sum(values[winnable], axis=1).sum()

    values = np.take(board * -1, winning_combinations)
    winnable = np.all((values !=-1 ) & (~np.isnan(values)), axis=1)
    total_score_opponent = np.sum(values[winnable], axis=1).sum()
    print("score :",total_score_player,total_score_opponent,(total_score_player - total_score_opponent)/15)
    return (total_score_player - total_score_opponent)/15

def heuristic(game: Game):
    game.update_big_board()
    for grid_num in game.valuation_to_update:
        if game.big_board[grid_num] != 0:
            game.valuation[grid_num] = game.big_board[grid_num]
        else:
            start = grid_num * game.block_size_squared
            end = start + game.block_size_squared
            subgrid = game.board[start:end]
            print("sub ",subgrid)
            game.valuation[grid_num] = local_heuristic(subgrid)

    game.valuation_to_update.clear()
    print(game.valuation)
    return local_heuristic(game.valuation)
