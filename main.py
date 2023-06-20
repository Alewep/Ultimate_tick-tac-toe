from game import Game
from minmax import find_best_move

game = None
while True:

    opponent_row, opponent_col = [int(i) for i in input().split()]

    first_player = 1 if opponent_row == opponent_col == -1 else -1

    if game is None:
        game = Game(3, 3, first_player)

    valid_action_count = int(input())

    valid_actions = []
    for i in range(valid_action_count):
        row, col = [int(j) for j in input().split()]
        valid_actions.append(game.coordinate_to_index(row, col))

    if not (opponent_row == opponent_col == -1):
        game.play(opponent_row, opponent_col, player=-1)

    index = find_best_move(game, valid_actions)

    game.play(index, player=1)

    print(*game.index_to_coordinate(index), sep=" ")