from logic.game_numpy import Game
from logic.minmax import find_best_move

game = None
while True:

    opponent_row, opponent_col = [int(i) for i in input().split()]

    first_player = 1 if opponent_row == opponent_col == -1 else -1

    if game is None:
        game = Game(3, 3)

    valid_action_count = int(input())

    if not (opponent_row == opponent_col == -1):
        game.play(opponent_row, opponent_col, player=-1)

    index = find_best_move(game)

    game.play(index, player=1)

    print(*game.index_to_coordinate(index), sep=" ")
