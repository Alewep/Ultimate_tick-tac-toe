from logic.game_numpy import Game
import math


def minimax(board: Game, is_maximizing: bool, max_depth: float = math.inf, depth: int = 0, alpha=-math.inf,
            beta=+math.inf, trace=[]) -> float:
    board.update_big_board()
    is_terminate = board.terminate()
    if depth >= max_depth or is_terminate:
        score = board.evaluate()

        if is_terminate:
            score = score * math.inf
            return 0 if score == math.nan else score
        else:
            return board.heuristic()

    else:
        if is_maximizing:

            max_value = -math.inf

            validate_actions = board.validate_actions()
            for action in validate_actions:
                save = board.save_play(action, player=1)
                value = minimax(board, False, max_depth, depth + 1, alpha=alpha, beta=beta, trace=trace + [action])
                board.back(save)
                max_value = max(value, max_value)
                alpha = max(max_value, alpha)

                if beta <= alpha:
                    break

            return max_value

        else:
            min_value = math.inf

            validate_actions = board.validate_actions()
            for action in validate_actions:
                save = board.save_play(action, player=-1)
                value = minimax(board, True, max_depth, depth + 1, alpha=alpha, beta=beta, trace=trace + [action])
                board.back(save)

                min_value = min(value, min_value)
                beta = min(beta, min_value)

                if beta <= alpha:
                    break

            return min_value


def find_best_move(board: Game, max_depth=2):
    valid_actions = board.validate_actions()
    # random.shuffle(valid_actions)

    best_value = -math.inf
    best_index = valid_actions[0]

    valuations = {}
    for action in valid_actions:
        save = board.save_play(action, player=1)
        value = minimax(board, False, max_depth, trace=[action])
        board.back(save)
        if best_value <= value:
            best_index = action
            best_value = value

        valuations[int(action)] = value

    return best_index, valuations
