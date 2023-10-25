import timeit
import numpy as np


class MyClass:
    def __init__(self, board):
        self.board = np.array(board)

    def heuristic2(self):
        values = np.take(self.board, winning_combinations)
        score = np.sum(values, axis=1)
        total_score = np.sum(score)
        return total_score

    def heuristic_alternative(self):
        total_score = 0
        for combination in winning_combinations:
            if -1 not in self.board[combination]:
                total_score += self.board[combination].sum()
        return total_score

    def heuristic_alternative2(self):

        values = np.take(self.board, winning_combinations)
        no_negative_ones = np.all(values != -1, axis=1)
        total_score = np.sum(values[no_negative_ones], axis=1).sum()

        return total_score

    def heuristic(self):
        score = 0
        for combinations in winning_combinations:
            score += self.board[combinations].sum()
        return score

    def heuristic_double(self):

        values = np.take(self.board, winning_combinations)
        no_negative_ones = np.all(values != -1, axis=1)
        total_score_player = np.sum(values[no_negative_ones], axis=1).sum()

        values = np.take(self.board * -1, winning_combinations)
        no_negative_ones = np.all(values != -1, axis=1)
        total_score_opponent = np.sum(values[no_negative_ones], axis=1).sum()

        return total_score_player - total_score_opponent

    def heuristic_double2(self,board):
        # Obtenir les valeurs pour toutes les combinaisons gagnantes
        values = np.take(board, winning_combinations, axis=0)

        # Scores pour le joueur et l'adversaire
        player_scores = np.sum(np.where(values > 0, values, 0), axis=1)
        opponent_scores = -np.sum(np.where(values < 0, values, 0), axis=1)

        # Calculer la somme des combinaisons où -1 est absent pour le joueur et l'adversaire
        player_score = np.sum(player_scores[np.all(values != -1, axis=1)])
        opponent_score = np.sum(opponent_scores[np.all(values != 1, axis=1)])

        return player_score - opponent_score

    def heuristic_g(self):
        valuation = np.zeros(9)
        for grid_num in range(8):
            if self.board[grid_num]:
                valuation[grid_num] = 24 * self.board[grid_num]
            else:
                start = grid_num * 9
                end = start + 9
                subgrid = self.board
                valuation[grid_num] = self.heuristic_double2(subgrid)

        return self.heuristic_double2(valuation)

# Exemple d'utilisation
#my_instance = MyClass(board=[1, 0, 0, 1, 0, 0, 0, 0, 0])
#my_instance = MyClass(board=[-1, -1, 0,1, -1, 1,1, 0, 1])
my_instance = MyClass(board=[-1, -1, 1,
                             0, 1, 0,
                             0, 0, 0])
winning_combinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

print(my_instance.heuristic())
print(my_instance.heuristic2())
print(my_instance.heuristic_alternative())
print(my_instance.heuristic_alternative2())
print(my_instance.heuristic_double())
print(my_instance.heuristic_g())
print(timeit.timeit(lambda: my_instance.heuristic(), number=1000)/1000)
print(timeit.timeit(lambda: my_instance.heuristic2(), number=1000)/1000)
print(timeit.timeit(lambda: my_instance.heuristic_alternative(), number=1000)/1000)
print(timeit.timeit(lambda: my_instance.heuristic_alternative2(), number=1000)/1000)
print(timeit.timeit(lambda: my_instance.heuristic_g(), number=1000)/1000)