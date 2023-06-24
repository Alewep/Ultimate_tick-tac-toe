import pytest
from game_bitarray import Game


@pytest.fixture
def empty_game():
    return Game(block_size=3, n_block=3)


def test_initialization():
    game = Game(block_size=3, n_block=3)

    assert game.block_size == 3
    assert game.n_block == 3
    assert game.block_size_squared == 9
    assert game.n_block_squared == 9


def test_coordinate_to_index():
    game = Game(block_size=3, n_block=3)

    # Test a few coordinates
    assert game.coordinate_to_index(0, 0) == 0
    assert game.coordinate_to_index(2, 2) == 8
    assert game.coordinate_to_index(3, 3) == 36
    assert game.coordinate_to_index(4, 4) == 40
    assert game.coordinate_to_index(8, 8) == 80


def test_index_to_coordinate():
    game = Game(block_size=3, n_block=3)

    # Test a few indexes
    assert game.index_to_coordinate(0) == (0, 0)
    assert game.index_to_coordinate(8) == (2, 2)
    assert game.index_to_coordinate(36) == (3, 3)
    assert game.index_to_coordinate(40) == (4, 4)
    assert game.index_to_coordinate(80) == (8, 8)


def test_play():
    game = Game(block_size=3, n_block=3)

    # Player 1 plays at (0, 0)
    game.play(0, 0, player=1)
    assert game.board_player[0]
    assert not (game.board_opponent[0])
    # Player -1 plays at (1, 1)
    game.play(1, 1, player=-1)
    index = game.coordinate_to_index(1, 1)
    assert not (game.board_player[index])
    assert game.board_opponent[index]

    # Attempting to play in an occupied cell
    with pytest.raises(ValueError):
        game.play(0, 0, player=1)


def test_empty_board():
    empty_game = Game(block_size=3, n_block=3)
    valid_actions = empty_game.validate_actions()
    assert len(valid_actions) == 81  # As all cells are empty


def test_partially_filled_board(empty_game):
    empty_game.play(0, 0, player=1)  # Play one move
    valid_actions = empty_game.validate_actions()
    assert len(valid_actions) == 8


def test_completely_filled_board(empty_game):
    for index in range(81):
        player = 1 if index % 2 == 0 else -1
        empty_game.play(index, player=player)

    valid_actions = empty_game.validate_actions()
    assert len(valid_actions) == 0  # All cells are filled


def test_smaller_board_won(empty_game):
    # Player 1 wins the first smaller board
    for i in range(3):
        empty_game.play(i, 0, player=1)

    # Update the big_board_player (assuming evaluate() does this)
    empty_game.big_board_player.data = 0b1

    valid_actions = empty_game.validate_actions()
    assert not any(action < 9 for action in valid_actions)  # No actions within the first smaller board are valid


def test_after_specific_action(empty_game):
    empty_game.play(1, 1, player=1)
    valid_actions = empty_game.validate_actions()
    taken_action = empty_game.coordinate_to_index(1, 1)
    assert taken_action not in valid_actions  # The action taken is no longer valid


import pytest


@pytest.fixture
def game():
    return Game(block_size=3, n_block=3)


def test_play_valid_moves(game):
    # Jouer un coup valide et vérifier l'état de la grille
    game.play(7, 7, player=1)
    assert game.board_player[game.coordinate_to_index(7, 7)]
    assert not (game.board_opponent[game.coordinate_to_index(7, 7)])
    assert not (game.big_board_player.all_bits_set())
    assert not (game.big_board_opponent.all_bits_set())

    # Jouer un second coup valide et vérifier l'état de la grille
    game.play(8, 8, player=-1)
    assert not (game.board_player[game.coordinate_to_index(8, 8)])
    assert game.board_opponent[game.coordinate_to_index(8, 8)]

    # Continuer de jouer jusqu'à compléter une ligne
    game.play(0, player=-1)
    game.play(1, player=-1)
    game.play(2, player=-1)

    assert game.board_opponent[0]
    assert game.board_opponent[1]
    assert game.board_opponent[2]
    # Vérifier si la mise à jour du grand plateau est correcte
    assert game.big_board_opponent[0]


def test_play_in_occupied_cell(game):
    # Jouer un coup dans une cellule occupée et vérifier si une exception est levée
    game.play(0, 0, player=1)
    with pytest.raises(ValueError):
        game.play(0, 0, player=-1)


def test_big_board_update_after_play(game):
    # Jouer des coups pour compléter une ligne dans une sous-grille
    game.play(0, 0, player=1)
    game.play(0, 1, player=1)
    game.play(0, 2, player=1)

    # Vérifier si la mise à jour du grand plateau est correcte
    assert game.big_board_opponent[0] == False
    assert game.big_board_player[0] == True



    # Jouer des coups pour compléter une colonne dans une autre sous-grille
    game.play(3, 4, player=-1)
    game.play(4, 4, player=-1)
    game.play(5, 4, player=-1)

    # Vérifier si la mise à jour du grand plateau est correcte
    assert game.big_board_opponent[4] == True
    assert game.big_board_player[4] == False

    assert game.terminate() == False


if __name__ == "__main__":
    pytest.main()
