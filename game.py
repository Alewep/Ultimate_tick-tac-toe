import sys


def check_victory(board) -> int:
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    for combination in winning_combinations:
        values = [board[i] for i in combination]
        if values == [1, 1, 1]:
            return 1
        elif values == [-1, -1, -1]:
            return -1

    return 0


class Game(object):
    def __init__(self, block_size, n_block, first_player=1):
        self.block_size = block_size
        self.n_block = n_block
        self.board = [0 for i in range((block_size ** 2) * (n_block ** 2))]
        self.last_play = -1

    def create_save_play(self, action, player=1):
        self.play(action, player=player)
        return [action, self.last_play]

    def back(self, save):
        self.board[save[0]] = 0
        self.last_play = save[1]

    def coordinate_to_index(self, row, col):
        grid_row = row // self.block_size
        grid_col = col // self.block_size
        grid_num = grid_row * self.n_block + grid_col

        local_row = row % self.block_size
        local_col = col % self.block_size

        return grid_num * (self.block_size ** 2) + (local_row * self.block_size + local_col)

    def index_to_coordinate(self, index):
        block_size_squared = self.block_size ** 2
        grid_num = index // block_size_squared

        local_index = index % block_size_squared

        grid_row = grid_num // self.n_block
        grid_col = grid_num % self.n_block

        local_row = local_index // self.block_size
        local_col = local_index % self.block_size

        row = grid_row * self.block_size + local_row
        col = grid_col * self.block_size + local_col

        return row, col

    def play(self, i, j=None, player=1):

        index = None
        if j is None:
            index = i
        else:
            index = self.coordinate_to_index(i, j)

        if self.board[index] == 0:
            self.board[index] = player
            self.last_play = index
        else:
            raise ValueError("Cell already occupied")

    def evaluate(self):
        uboard = []

        for i in range(self.n_block ** 2):
            start = i * (self.block_size ** 2)
            end = (i + 1) * (self.block_size ** 2)
            uboard.append(check_victory(self.board[start:end]))
        return uboard, check_victory(uboard)

    def terminate(self):
        return self.evaluate()[1] != 0 or (0 not in self.board)

    def validate_actions(self):
        available_actions = []
        num_block = None
        # Get the block number where the next move should be played
        if self.last_play != -1:
            num_block = self.last_play % (self.block_size ** 2)
            start = num_block * (self.block_size ** 2)
            end = (num_block + 1) * (self.block_size ** 2)
            local_board = self.board[start:end]

            # If it's possible to play in this block, return the available actions

            if check_victory(local_board) == 0 and 0 in local_board:
                return [i + (num_block * (self.block_size ** 2)) for i in range(self.block_size ** 2) if
                        local_board[i] == 0]

        # If not possible to play in the local block, check for available actions in other blocks
        for block in range(self.n_block ** 2):
            if block == num_block:
                continue
            start = block * (self.block_size ** 2)
            end = (block + 1) * (self.block_size ** 2)
            block_values = self.board[start:end]

            # If the block is not completed or full, add the available actions in this block
            if check_victory(block_values) == 0 and 0 in block_values:
                available_actions.extend(
                    [i + (block * (self.block_size ** 2)) for i in range(self.block_size ** 2) if block_values[i] == 0])

        return available_actions

    def display_simple_board(self):
        """
        Affiche le plateau de jeu de manière linéaire.
        """
        for row in range(self.n_block * self.block_size):
            row_display = ''
            for col in range(self.n_block * self.block_size):
                index = self.coordinate_to_index(row, col)
                cell_value = self.board[index]

                # Remplacer les valeurs numériques par des caractères pour l'affichage
                if cell_value == 1:
                    cell_display = 'X'
                elif cell_value == -1:
                    cell_display = 'O'
                else:
                    cell_display = '*'

                row_display += cell_display

                # Séparer les cellules avec des |
                if col < (self.n_block * self.block_size) - 1:
                    row_display += '|'

            print(row_display, file=sys.stderr)

            # Afficher des lignes de séparation
            if row < (self.n_block * self.block_size) - 1:
                print('--' * (self.n_block * self.block_size), file=sys.stderr)