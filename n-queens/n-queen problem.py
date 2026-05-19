import pygame
import sys
import random
import time

#  Configuration - tweak these before running
N               = 8       # Board size (try 6, 8, 10, 12)
CELL_SIZE       = 72      # Pixels per square
DELAY_MS        = 1000     # Milliseconds between algorithm steps
MAX_SIDEWAYS    = 100     # Sideways moves allowed before restart
STATUS_H        = 90      # Height of the status bar in pixels

#Colour palette
LIGHT_SQ    = (240, 217, 181)   # Cream - light squares
DARK_SQ     = (181, 136,  99)   # Brown - dark squares
QUEEN_COL   = ( 30,  30,  30)   # Near-black queen glyph
ATTACK_COL  = (220,  50,  50)   # Red highlight - conflicting queen
OK_COL      = ( 50, 180,  80)   # Green highlight - safe queen
BG_STATUS   = ( 30,  30,  40)   # Status bar background
TEXT_COL    = (220, 220, 220)   # Status bar text
HIGHLIGHT   = (255, 215,   0)   # Gold - queen being moved this step


#  Heuristic - count attacking pairs
def count_attacks(board: list) -> int:
    """returns the number of attacking queens"""
    attacks = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            # Same row check
            if board[i] == board[j]:
                attacks += 1
            # Same diagonal check - absolute row diff equals absolute col diff
            if abs(board[i] - board[j]) == abs(i - j):
                attacks += 1
    return attacks


#  Initial state - random board (one queen per column)
def random_board(n: int) -> list:
    """Return a random board: board[col] = random row in [0, n)."""
    return [random.randint(0, n - 1) for _ in range(n)]



#  Find conflicting queens
def conflicting_cols(board: list) -> set:
    """ Return the set of column indices whose queens are involved in at least one attacking relationship. """
    n = len(board)
    bad = set()
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                bad.add(i)
                bad.add(j)
    return bad


#  Hill Climbing step - find and apply the best single move
def hill_climbing_step(board: list) -> tuple:
    n = len(board)
    current_attacks = count_attacks(board)

    best_attacks = current_attacks   # Track the globally best score seen
    best_moves   = []                # List of (col, row) ties at best score

    for col in range(n):
        original_row = board[col]
        for row in range(n):
            if row == original_row:
                continue                     # Skip the current position
            board[col] = row                 # Try the move
            a = count_attacks(board)
            if a < best_attacks:
                best_attacks = a
                best_moves   = [(col, row)]  # New best - reset the list
            elif a == best_attacks:
                best_moves.append((col, row))# Tie - add to the list
            board[col] = original_row        # Undo the move

    if best_attacks >= current_attacks:
        # No improvement possible - local minimum reached
        return (-1, -1, current_attacks, True)

    # Choose randomly among all equally-best moves
    best_col, best_row = random.choice(best_moves)
    board[best_col] = best_row               # Apply the chosen move
    return (best_col, best_row, best_attacks, False)


#  Pygame rendering
def draw_board(screen, board, font_queen, font_status,
               moved_col, attacks, moves, restarts, solved):
    
    """ Render the chessboard, queens, and status bar. """
    n   = len(board)
    bad = conflicting_cols(board)

    # Draw the squares
    for col in range(n):
        for row in range(n):
            colour = LIGHT_SQ if (col + row) % 2 == 0 else DARK_SQ
            rect   = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE,
                                 CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, colour, rect)

    # Draw the queens 
    for col in range(n):
        row = board[col]

        # Colour for the queen's square
        if solved:
            bg = OK_COL                      # All green when solved
        elif col == moved_col:
            bg = HIGHLIGHT                   # Gold - just moved this step
        elif col in bad:
            bg = ATTACK_COL                  # Red - currently in conflict
        else:
            bg = OK_COL                      # Green - safe queen

        rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE,
                           CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, bg, rect)   # Colour the square first

        # Render the queen glyph centred in the square
        glyph = font_queen.render("♛", True, QUEEN_COL)
        gx    = col * CELL_SIZE + (CELL_SIZE - glyph.get_width())  // 2
        gy    = row * CELL_SIZE + (CELL_SIZE - glyph.get_height()) // 2
        screen.blit(glyph, (gx, gy))

 #Draw the status bar 
    bar_y = n * CELL_SIZE
    bar_x = n * CELL_SIZE
    pygame.draw.rect(screen, BG_STATUS,
                     pygame.Rect(0, bar_y, bar_x, STATUS_H))

    if solved:
        msg    = f"  Solved!  N={n}   Moves={moves}   Restarts={restarts}   " \
                f"Green=solved   Red=unsolved   Gold=moved queen   [Q/Esc to quit]"
        colour = (80, 220, 100)
    else:
        msg    = f"  N={n}   Attacks={attacks}   Moves={moves}   " \
                f"Restarts={restarts}   Green=solved   Red=unsolved   Gold=moved queen   [R=restart  Q=quit]"
        colour = TEXT_COL

    line1 = f"N={n} Attacks={attacks}   Moves={moves}   Restarts={restarts} [R=restart  Q=quit]"
    line2 = f"Green[solved queen] Red[unsolved queen] Gold[moved queen]"

    if solved:
        line1 = f"  Solved!  N={n}   Moves={moves}   Restarts={restarts}   [Q/Esc to quit]"

    lbl1 = font_status.render(line1, True, colour)
    lbl2 = font_status.render(line2, True, (180, 180, 180))
    screen.blit(lbl1, (6, bar_y + 10))
    screen.blit(lbl2, (6, bar_y + 10 + lbl1.get_height() + 6))

    pygame.display.flip()


# Initialise pygame and run the algorithm
def main():
    pygame.init()

    WIN_W  = N * CELL_SIZE
    WIN_H  = N * CELL_SIZE + STATUS_H
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption(f"N-Queens hill-climbing  (N={N})")

    # Fonts - fall back gracefully if the system font lacks the queen glyph
    try:
        font_queen = pygame.font.SysFont("segoeuisymbol", int(CELL_SIZE * 0.72))
    except Exception:
        font_queen = pygame.font.SysFont("dejavusans",    int(CELL_SIZE * 0.72))

    font_status = pygame.font.SysFont("consolas", 17)

    #Algorithm state
    board     = random_board(N)   # Current board state
    attacks   = count_attacks(board)
    moves     = 0                 # Total moves across all restarts
    restarts  = 0                 # Number of random restarts performed
    moved_col = -1                # Column highlighted in the last step
    solved    = False
    sideways  = 0                 # Consecutive non-improving moves

    clock     = pygame.time.Clock()
    last_step = time.time()       # Throttle algorithm steps by DELAY_MS

    # ── Main event loop ──────────────────────────────────────
    while True:
        # Handle input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_r:           # Manual restart key
                    board     = random_board(N)
                    attacks   = count_attacks(board)
                    moved_col = -1
                    solved    = False
                    sideways  = 0
                    restarts += 1

        # Draw the current board state
        draw_board(screen, board, font_queen, font_status,
                   moved_col, attacks, moves, restarts, solved)

        # Run one algorithm step
        if not solved and (time.time() - last_step) >= DELAY_MS / 1000:
            last_step = time.time()

            col, row, new_attacks, stuck = hill_climbing_step(board)

            if stuck or sideways >= MAX_SIDEWAYS:
                # Local minimum reached - perform a random restart
                board     = random_board(N)
                attacks   = count_attacks(board)
                moved_col = -1
                restarts += 1
                sideways  = 0
            else:
                moves    += 1
                moved_col = col

                if new_attacks == attacks:
                    sideways += 1   # Sideways move - no improvement this step
                else:
                    sideways  = 0

                attacks = new_attacks

                if attacks == 0:
                    solved = True   # Perfect solution found

        clock.tick(60)   # Cap the frame rate at 60 fps


if __name__ == "__main__":
    main()