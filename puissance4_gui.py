import sys
import pygame

from puissance4 import (
    create_grid,
    drop_token,
    win_check,
    is_full,
    get_ia_move,
)

# Constantes du jeu
ROWS = 6
COLS = 7

SQUARE_SIZE = 100
RADIUS = SQUARE_SIZE // 2 - 5

WIDTH = COLS * SQUARE_SIZE
HEIGHT = (ROWS + 1) * SQUARE_SIZE

# Couleurs
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)      # joueur humain
YELLOW = (255, 255, 0) # IA (pour plus tard)

pygame.init()
FONT = pygame.font.SysFont("monospace", 40)
BIG_FONT = pygame.font.SysFont("monospace", 80, bold=True)


def draw_board(screen, grid):
    """Dessine le plateau et les pions à partir de la grille."""
    for c in range(COLS):
        for r in range(ROWS):
            # Dessiner le fond bleu
            rect_x = c * SQUARE_SIZE
            rect_y = r * SQUARE_SIZE + SQUARE_SIZE  # on laisse une ligne au-dessus
            pygame.draw.rect(
                screen,
                BLUE,
                (rect_x, rect_y, SQUARE_SIZE, SQUARE_SIZE),
            )

            # Position du pion au centre de la case
            center_x = c * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE // 2

            value = grid[r][c]
            if value == 0:
                color = BLACK
            elif value == 1:
                color = RED
            else:
                color = YELLOW

            pygame.draw.circle(screen, color, (center_x, center_y), RADIUS)

    pygame.display.update()

def show_end_message(screen, text, color):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    label = BIG_FONT.render(text, True, color)
    x = (WIDTH - label.get_width()) // 2
    y = (HEIGHT - label.get_height()) // 2
    screen.blit(label, (x, y))

    # Sous-texte
    sub = FONT.render("R: Rejouer | Échap: Quitter", True, (255, 255, 255))
    sub_x = (WIDTH - sub.get_width()) // 2
    sub_y = y + label.get_height() + 20
    screen.blit(sub, (sub_x, sub_y))

    pygame.display.update()

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Puissance 4 - GUI")

    grid = create_grid()
    current_player = 1
    running = True
    game_over = False

    while running:
        if not game_over:
            screen.fill(BLACK)
            draw_board(screen, grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        grid = create_grid()
                        current_player = 1
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False

                continue

            # Clic souris pour le joueur humain
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_player != 1:
                    continue

                x_pos = event.pos[0]
                col = x_pos // SQUARE_SIZE

                if 0 <= col < COLS:
                    if drop_token(grid, col, current_player):
                        # Vérif victoire
                        if win_check(grid, current_player):
                            show_end_message(screen, "VICTOIRE", RED)
                            game_over = True
                        elif is_full(grid):
                            show_end_message(screen, "MATCH NUL", (255, 255, 255))
                            game_over = True

                        # ------ TOUR DE L'IA ------
                        if not game_over:
                            current_player = 2  # IA

                            # Pause visuelle entre le coup du joueur et celui de l'IA
                            draw_board(screen, grid)
                            pygame.display.update()
                            pygame.time.delay(600)

                            col_ia = get_ia_move(grid, depth=5)

                            drop_token(grid, col_ia, 2)

                            # Afficher le pion de l'IA avant le message de fin
                            draw_board(screen, grid)
                            pygame.display.update()
                            pygame.time.delay(300)

                            if win_check(grid, 2):
                                show_end_message(screen, "DÉFAITE", YELLOW)
                                game_over = True

                            elif is_full(grid):
                                show_end_message(screen, "MATCH NUL", (255, 255, 255))
                                game_over = True

                            else:
                                # On vide les clics accumulés pendant le tour de l'IA
                                pygame.event.clear(pygame.MOUSEBUTTONDOWN)
                                current_player = 1
                        break
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
