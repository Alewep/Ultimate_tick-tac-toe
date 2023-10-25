import numpy as np
import timeit

winning_combinations = [
    [1, 2, 3], [4, 5, 6], [7, 8, 9],
    [1, 4, 7], [2, 5, 8], [3, 6, 9],
    [1, 5, 9], [3, 5, 7]
]


class MyClass:
    def __init__(self, big_board, prevent_score):
        self.big_board = np.array(big_board)
        self.prevent_score = prevent_score

    # Méthode originale
    def evaluate_original(self):
        opp_preven, player_preven = self.prevent_score
        if opp_preven < 3 and player_preven < 3:
            return 0

        for combination in winning_combinations:
            sum = self.big_board[combination].sum()
            if sum == 3:
                return 1
            if sum == -3:
                return -1
        return 0

    # Méthode optimisée
    def evaluate_optimized(self):
        opp_preven, player_preven = self.prevent_score
        if opp_preven < 3 and player_preven < 3:
            return 0

        # Extraire les valeurs pour toutes les combinaisons gagnantes
        values = np.take(self.big_board, winning_combinations)

        # Calculer la somme le long des lignes
        sums = np.sum(values, axis=1)

        # Vérifier si l'une des sommes est égale à 3 ou -1
        if np.abs(sums) == 3:
            return sums / 3
        else:
            return 0


# Créer une instance de MyClass
my_instance = MyClass(big_board=[0, 1, 1, 1, 0, -1, 0, 1, 0], prevent_score=(2, 2))

# Mesurer le temps d'exécution de la méthode originale
time_original = timeit.timeit(my_instance.evaluate_original, number=100000)
print(f"Temps d'exécution de la méthode originale: {time_original:.6f} secondes")

# Mesurer le temps d'exécution de la méthode optimisée
time_optimized = timeit.timeit(my_instance.evaluate_optimized, number=100000)
print(f"Temps d'exécution de la méthode optimisée: {time_optimized:.6f} secondes")
