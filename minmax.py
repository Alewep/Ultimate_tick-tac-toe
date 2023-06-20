from game import Game
import math
import random


def minimax(board: Game, is_maximizing: bool, max_depth: float = math.inf, depth: int = 0, alpha=-math.inf,
            beta=+math.inf) -> float:
    is_terminate = board.terminate()
    if depth >= max_depth or is_terminate:
        states, score = board.evaluate()

        if is_terminate:
            return score * 100
        else:
            return sum(i for i in states) * 10

    else:
        if is_maximizing:

            max_value = -math.inf

            validate_actions = board.validate_actions()
            for action in validate_actions:

                save = board.create_save_play(action, player=1)
                value = minimax(board, False, max_depth, depth + 1)
                board.back(save)
                max_value = max(value, max_value)
                alpha = max(max_value, alpha)

                if alpha >= beta:
                    break

            return max_value

        else:
            min_value = math.inf

            validate_actions = board.validate_actions()
            for action in validate_actions:

                save = board.create_save_play(action, player=-1)
                value = minimax(board, True, max_depth, depth + 1)
                board.back(save)

                min_value = min(value, min_value)
                beta = min(beta, min_value)

                if beta <= alpha:
                    break

            return min_value


def find_best_move(board: Game, valid_actions, max_depth=2):
    best_value = -math.inf
    best_index = None
    random.shuffle(valid_actions)

    for action in valid_actions:
        save = board.create_save_play(action, player=1)
        value = minimax(board, True, max_depth)
        board.back(save)
        if best_value < value:
            best_index = action
            best_value = value

    return best_index



