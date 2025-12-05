import random

def create_grid():
    grid = []
    for _ in range(6):
        row = [0 for _ in range(7)]
        grid.append(row)
    return grid


def print_grid(grid):
    for row in grid:
        display_row = []
        for value in row:
            if value == 0:
                display_row.append('.')
            elif value == 1:
                display_row.append('O')
            else:
                display_row.append('X')

        print("| " + " ".join(display_row) + " |")

    # Ligne des numéros de colonnes
    print("  " + " ".join(str(i) for i in range(1, 8)))


def drop_token(grid, col, player):
    # Si la case tout en haut est non vide, la colonne est pleine
    if grid[0][col] != 0:
        return False

    # On cherche depuis le bas la première case vide
    for row in range(len(grid) - 1, -1, -1):  # 5,4,3,2,1,0
        if grid[row][col] == 0:
            grid[row][col] = player
            return True

    return False  # sécurité


def is_full(grid):
    for value in grid[0]:
        if value == 0:
            return False
    return True


def win_check(grid, player):
    # Vérification horizontale
    for row in range(6):
        for col in range(4):
            if all(grid[row][col + i] == player for i in range(4)):
                return True

    # Vérification verticale
    for col in range(7):
        for row in range(3):
            if all(grid[row + i][col] == player for i in range(4)):
                return True

    # Vérification diagonale (bas-gauche à haut-droit)
    for row in range(3, 6):
        for col in range(4):
            if all(grid[row - i][col + i] == player for i in range(4)):
                return True

    # Vérification diagonale (haut-gauche à bas-droit)
    for row in range(3):
        for col in range(4):
            if all(grid[row + i][col + i] == player for i in range(4)):
                return True

    return False

def main():
    grid = create_grid()
    current_player = 1

    while True:
        print_grid(grid)
        print(f"Tour du joueur {current_player} ({'O' if current_player == 1 else 'X'})")

        # Tour joue HUMAIN
        if current_player == 1:
            # Demande de colonne
            choice = input("Choisissez une colonne (1-7) : ")

            # Vérif basique de l'entrée
            if not choice.isdigit():
                print("Veuillez entrer un nombre entre 1 et 7.")
                continue

            col = int(choice)

            if col < 1 or col > 7:
                print("La colonne doit être entre 1 et 7.")
                continue

            # Conversion en index (0-6)
            col_index = col - 1

            # Tentative de poser le pion
            if not drop_token(grid, col_index, current_player):
                print("Cette colonne est pleine, choisissez-en une autre.")
                continue
        else:
            col_index = get_ia_move(grid, 5)
            drop_token(grid, col_index, current_player)
            print(f"L'IA choisit la colonne {col_index + 1}")

        # Vérifier la victoire
        if win_check(grid, current_player):
            print_grid(grid)
            print(f"Le joueur {current_player} ({'O' if current_player == 1 else 'X'}) a gagné !")
            break

        # Vérif match nul (grille pleine)
        if is_full(grid):
            print_grid(grid)
            print("Match nul, la grille est pleine.")
            break

        # Changer de joueur
        current_player = 2 if current_player == 1 else 1



# ____________ PARTIE IA ____________
# Renvoyer les coups possibles pour l'IA
def get_valid_moves(grid):
    valid_moves = []
    for col in range(7):
        if grid[0][col] == 0:
            valid_moves.append(col)
    return valid_moves


# Simuler un coup sans toucher à la vraie grille
def simulate_move(grid, col, player):
    new_grid = [row[:] for row in grid]
    drop_token(new_grid, col, player)
    return new_grid


# Evaluation simple de la grille pour l'IA
def evaluate_grid(grid):
    if win_check(grid, 2):
        return 10000
    if win_check(grid, 1):
        return -10000
    score = 0

    center_col_index = 3
    center_col = [grid[row][center_col_index] for row in range(6)]
    center_count = center_col.count(2)
    score += center_count * 3

    # Horizontales
    for row in range(6):
        for col in range(7 - 3):
            window = [grid[row][col + i] for i in range(4)]
            score += score_window(window)

    # Verticales
    for row in range(6 - 3):
        for col in range(7):
            window = [grid[row + i][col] for i in range(4)]
            score += score_window(window)

    # Diagonales /
    for row in range(6 - 3):
        for col in range(7 - 3):
            window = [grid[row + i][col + i] for i in range(4)]
            score += score_window(window)

    # Diagonales \
    for row in range(3, 6):
        for col in range(7 - 3):
            window = [grid[row - i][col + i] for i in range(4)]
            score += score_window(window)

    return score

# Optimisation de l'ordre des coups
def get_ordered_moves(grid):
    preferred = [3, 2, 4, 1, 5, 0, 6]
    return [col for col in preferred if col in get_valid_moves(grid)]

# Fonction minimax
def minimax(grid, depth, alpha, beta, maximizing_player):
    if depth == 0 or win_check(grid, 1) or win_check(grid, 2) or is_full(grid):
        return evaluate_grid(grid)
    if maximizing_player:
        best_score = float('-inf')
        for col in get_ordered_moves(grid):
            new_grid = simulate_move(grid, col, 2)
            score = minimax(new_grid, depth - 1, alpha, beta, False)
            best_score = max(best_score, score)

            # Alpha Beta
            alpha = max(alpha, score)
            if beta <= alpha:
                break

        return best_score
    else:
        best_score = float('inf')
        for col in get_valid_moves(grid):
            new_grid = simulate_move(grid, col, 1)
            score = minimax(new_grid, depth - 1, alpha, beta, True)
            best_score = min(best_score, score)

            # Alpha Beta
            beta = min(beta, score)
            if beta <= alpha:
                break

        return best_score

def get_ia_move(grid, depth):
    valid_moves = get_valid_moves(grid)

    # 1) Jouer immédiatement un coup gagnant si possible
    for col in valid_moves:
        new_grid = simulate_move(grid, col, 2)
        if win_check(new_grid, 2):
            return col

    # 2) Bloquer une victoire immédiate de l'adversaire
    for col in valid_moves:
        new_grid = simulate_move(grid, col, 1)
        if win_check(new_grid, 1):
            return col

    # 3) Sinon, utiliser minimax avec ordre de colonnes préféré
    best_score = float('-inf')
    best_cols = []
    for col in get_ordered_moves(grid):
        new_grid = simulate_move(grid, col, 2)
        score = minimax(new_grid, depth - 1, float('-inf'), float('inf'), False)

        if score > best_score:
            best_score = score
            best_cols = [col]
        elif score == best_score:
            best_cols.append(col)
    return random.choice(best_cols)

#Calcul du score d'une fenêtre de 4 cases
def score_window(window):
    score = 0
    ia_count = window.count(2)
    human_count = window.count(1)
    empty_count = window.count(0)

    if ia_count == 3 and empty_count == 1:
        score += 5
    elif ia_count == 2 and empty_count == 2:
        score += 2

    if human_count == 3 and empty_count == 1:
        score -= 7
    elif human_count == 2 and empty_count == 2:
        score -= 5

    return score


if __name__ == "__main__":
    main()
