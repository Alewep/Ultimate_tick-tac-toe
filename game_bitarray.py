from __future__ import annotations
import sys
import copy


class BitArray:
    def __init__(self, size):
        self.size = size
        self.data = 0

    def __iter__(self):
        for i in range(self.size):
            yield self.__getitem__(i)

    def __getitem__(self, key: int):
        if isinstance(key, int):
            return bool((self.data >> key) & 1)
        elif isinstance(key, slice):
            start, stop, step = key.indices(self.size)

            mask = ((1 << (stop - start)) - 1) << start
            result_data = (self.data & mask) >> start

            result = BitArray(stop - start)
            result.data = result_data
            return result
        else:
            print(key)
            raise TypeError("Invalid argument type.")

    def __setitem__(self, index: int, value):

        if bool(value):
            self.data |= 1 << index
        else:
            self.data &= ~(1 << index)

    def __and__(self, other):
        if isinstance(other, int):
            result_data = self.data & other
        elif isinstance(other, BitArray):
            result_data = self.data & other.data
        else:
            raise TypeError("Unsupported operand type for &: BitArray and {}".format(type(other).__name__))
        result = BitArray(self.size)
        result.data = result_data
        return result

    def __rand__(self, other):
        if isinstance(other, int):
            result_data = other & self.data
        else:
            raise TypeError("Unsupported operand type for &: {} and BitArray".format(type(other).__name__))
        result = BitArray(self.size)
        result.data = result_data
        return result

    def __or__(self, other):
        if isinstance(other, int):
            result_data = self.data | other
        elif isinstance(other, BitArray):
            result_data = self.data | other.data
        else:
            raise TypeError("Unsupported operand type for |: BitArray and {}".format(type(other).__name__))
        result = BitArray(self.size)
        result.data = result_data
        return result

    def __ror__(self, other):
        if isinstance(other, int):
            result_data = other | self.data
        else:
            raise TypeError("Unsupported operand type for |: {} and BitArray".format(type(other).__name__))
        result = BitArray(self.size)
        result.data = result_data
        return result

    def __invert__(self):
        result = BitArray(self.size)
        result.data = ~self.data & ((1 << self.size) - 1)
        return result

    def __eq__(self, other):
        if isinstance(other, int):
            return self.data == other
        elif isinstance(other, BitArray):
            return self.data == other.data
        else:
            raise TypeError("Unsupported operand type for |: BitArray and {}".format(type(other).__name__))

    def all_bits_set(self) -> bool:
        return self.data == (1 << self.size) - 1

    def repeat_bits(self, n):
        binary_str = bin(self.data)[2:]
        repeated_bits = ''.join(bit * n for bit in binary_str)
        result = BitArray(self.size)
        result.data = int(repeated_bits, 2)
        return result

    def __str__(self):
        return bin(self.data)

    def __len__(self):
        return self.size


winning_combinations = [
    0b111000000, 0b000111000, 0b000000111,
    0b100100100, 0b010010010, 0b001001001,
    0b100010001, 0b001010100
]


class Game(object):
    def __init__(self, block_size, n_block, first_player=1):
        self.block_size = block_size
        self.n_block = n_block
        self.block_size_squared = self.block_size ** 2
        self.n_block_squared = self.n_block ** 2
        self.board_player = BitArray(self.block_size_squared * self.n_block_squared)
        self.board_opponent = BitArray(self.block_size_squared * self.n_block_squared)

        self.big_board_player = BitArray(self.block_size_squared)
        self.big_board_opponent = BitArray(self.block_size_squared)

        self.last_play = -1

    def coordinate_to_index(self, row, col):
        grid_row = row // self.block_size
        grid_col = col // self.block_size
        grid_num = grid_row * self.n_block + grid_col

        local_row = row % self.block_size
        local_col = col % self.block_size

        return grid_num * self.block_size_squared + (local_row * self.block_size + local_col)

    def update_big_board(self, index_of_last_move):

        grid_num = index_of_last_move // self.block_size_squared

        # If this grid is already marked as won by any player, no need to update
        if self.big_board_player[grid_num] or self.big_board_opponent[grid_num]:
            return

        start = grid_num * self.block_size_squared
        end = start + self.block_size_squared
        subgrid_player = self.board_player[start:end]
        subgrid_opponent = self.board_opponent[start:end]

        # Check if this grid is won by any player
        for combination in winning_combinations:
            if subgrid_player & combination == combination:
                self.big_board_player[grid_num] = True
                break
            if subgrid_opponent & combination == combination:
                self.big_board_opponent[grid_num] = True
                break

    def play(self, i, j=None, player=1):
        if j is None:
            index = i
        else:
            index = self.coordinate_to_index(i, j)

        if not (self.board_player[index] or self.board_opponent[index]):
            if player == 1:
                self.board_player[index] = True
            elif player == -1:
                self.board_opponent[index] = True
            else:

                raise ValueError("The player id is not correct")

            self.last_play = index
        else:
            raise ValueError("Cell already occupied")

        self.update_big_board(index)

    def save_play(self, index, player=1):
        save = [self.last_play, index]
        self.play(index, player=player)
        return save

    def back(self, save):
        self.last_play, index = save
        self.board_player[index] = 0
        self.board_opponent[index] = 0
        self.big_board_player[index // self.block_size_squared] = 0
        self.big_board_opponent[index // self.block_size_squared] = 0

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

        for combination in winning_combinations:
            if (self.big_board_opponent.data & combination) == combination:
                return -1

        for combination in winning_combinations:
            if (self.big_board_player.data & combination) == combination:
                return 1

        return 0

    def terminate(self):
        return self.evaluate() != 0 or (self.board_opponent | self.board_player).all_bits_set()

    def validate_actions(self):
        grid_num = self.last_play % self.block_size_squared
        valid_actions = []
        if self.last_play >= 0 and self.big_board_opponent[grid_num] == self.big_board_player[grid_num] == False:
            start = grid_num * self.block_size_squared
            end = (grid_num + 1) * self.block_size_squared
            local = ~(self.board_opponent[start:end] | self.board_player[start:end])
            for index, valid in enumerate(local):
                if valid:
                    valid_actions.append((grid_num * self.block_size_squared) + index)

        else:
            big_board_mask = (self.big_board_player | self.big_board_opponent)
            big_board_mask = big_board_mask.repeat_bits(self.block_size_squared)
            board_mask = (self.board_player | self.board_opponent)
            valid_mask = ~(board_mask | big_board_mask)

            for index, valid in enumerate(valid_mask):
                if valid:
                    valid_actions.append(index)

        return valid_actions

    def heuristic(self):
        return sum((int(i) for i in self.big_board_player)) - sum((int(i) for i in self.big_board_opponent))
