import pygame
import sys
import numpy as np
pygame.font.init()
pygame.init()


# ---------
# CONSTANTS
# ---------
WIDTH, HEIGHT = 600, 700

SIZE_BOARD = 600

BOARD_ROWS, BOARD_COLS = 3, 3

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (181, 178, 177)

O_COLOR = GREY
X_COLOR = GREY
BACKGROUND_COLOR = BLACK

LINE_COLOR = WHITE
LINE_WIDTH = 4
LINE_GAP = 200
WINING_LINE_WIDTH = 2

PLAYER_X = 1
PLAYER_O = 2

CIRCLE_RADIUS = 60
CIRCLE_SIZE_BOARD = 15
CROSS_SIZE_BOARD = 20
SPACE = 50

GAMESTATE_FONT = pygame.font.SysFont('couriernew', 50)


PLAY_SOUND = pygame.mixer.Sound(
    '/Users/lethien/Desktop/Projects/Tic Tac Toe/Assets/play_sound.mp3')
VICTORY_SOUND = pygame.mixer.Sound(
    '/Users/lethien/Desktop/Projects/Tic Tac Toe/Assets/victory_sound.mp3')
TIE_GAME_SOUND = pygame.mixer.Sound(
    '/Users/lethien/Desktop/Projects/Tic Tac Toe/Assets/tie_game.wav')
# ------
# WINDOW
# ------

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')

# -------------
# CONSOLE BOARD
# -------------
board = np.zeros((BOARD_ROWS, BOARD_COLS))


# ************************** GAME FUNCTIONS  **************************


def draw_window():
    WIN.fill(BACKGROUND_COLOR)
    draw_lines()
    pygame.display.update()


def draw_lines():
    # First vertical line
    pygame.draw.line(WIN, LINE_COLOR, (200, 0), (200, 600), LINE_WIDTH)
    # Second vertical line
    pygame.draw.line(WIN, LINE_COLOR, (200 + LINE_GAP, 0),
                     (200 + LINE_GAP, 600), LINE_WIDTH)

    # First horizontal line
    pygame.draw.line(WIN, LINE_COLOR, (0, 200), (600, 200), LINE_WIDTH)
    # Second horizontal line
    pygame.draw.line(WIN, LINE_COLOR, (0, 200 + LINE_GAP),
                     (600, 200 + LINE_GAP), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == PLAYER_O:
                pygame.draw.circle(
                    WIN, O_COLOR, (col * 200 + 100, row * 200 + 100), CIRCLE_RADIUS, CIRCLE_SIZE_BOARD)

            elif board[row][col] == PLAYER_X:
                pygame.draw.line(WIN, X_COLOR, (col * 200 + SPACE, row * 200 + 200 - SPACE),
                                 (col * 200 + 200 - SPACE, row * 200 + SPACE), CROSS_SIZE_BOARD)
                pygame.draw.line(WIN, X_COLOR, (col * 200 + SPACE, row * 200 + SPACE),
                                 (col * 200 + 200 - SPACE, row * 200 + 200 - SPACE), CROSS_SIZE_BOARD)


def mark_squares(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] == 0
    # if board[row][col] == 0:
    #     return True
    # else:
    #     return False


def check_win(player):
    # Vertical win check
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            VICTORY_SOUND.play()
            return True

    # Horizontal win check
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            VICTORY_SOUND.play()
            return True

    # Ascending diagonal win check
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal_winning_line(player)
        VICTORY_SOUND.play()
        return True

    # Descending diagonal win check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_des_diagonal_winning_line(player)
        VICTORY_SOUND.play()
        return True


def draw_vertical_winning_line(col, player):
    posX = col * 200 + 100  # +100 because want it to be in the middle

    color = X_COLOR if player == PLAYER_X else O_COLOR
    pygame.draw.line(WIN, color, (posX, 15),
                     (posX, SIZE_BOARD - 15), WINING_LINE_WIDTH)


def draw_horizontal_winning_line(row, player):
    posY = row * 200 + 100  # + 100 because want it to be in the middle

    color = X_COLOR if player == PLAYER_X else O_COLOR
    pygame.draw.line(WIN, color, (15, posY),
                     (SIZE_BOARD - 15, posY), WINING_LINE_WIDTH)


def draw_asc_diagonal_winning_line(player):
    color = X_COLOR if player == PLAYER_X else O_COLOR
    pygame.draw.line(WIN, color, (15, SIZE_BOARD - 15),
                     (SIZE_BOARD - 15, 15), LINE_WIDTH)


def draw_des_diagonal_winning_line(player):
    color = X_COLOR if player == PLAYER_X else O_COLOR
    pygame.draw.line(WIN, color, (15, 15),
                     (SIZE_BOARD - 15, SIZE_BOARD - 15), LINE_WIDTH)


def isBoard_full():
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if board[r][c] == 0:
                return False
    return True

# ************************** MAIN FUNCTIONS  **************************


def main():
    draw_window()
    player = PLAYER_X
    run = True
    gameOver = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                if mouseY > WIDTH:
                    continue

                clicked_row = int(mouseY // 200)
                clicked_col = int(mouseX // 200)

                if available_square(clicked_row, clicked_col):
                    if player == PLAYER_X:
                        mark_squares(clicked_row, clicked_col, PLAYER_X)
                        if check_win(player):
                            gameState_text = GAMESTATE_FONT.render(
                                'X WON!', True, WHITE)
                            WIN.blit(gameState_text, (WIDTH/2 - gameState_text.get_width() /
                                                      2, 630))
                            gameOver = True
                        player = PLAYER_O

                    elif player == PLAYER_O:
                        mark_squares(clicked_row, clicked_col, PLAYER_O)
                        if check_win(player):
                            gameState_text = GAMESTATE_FONT.render(
                                'O WON!', True, WHITE)
                            WIN.blit(gameState_text, (WIDTH/2 - gameState_text.get_width() /
                                                      2, 630))
                            gameOver = True
                        player = PLAYER_X

                    draw_figures()
                    PLAY_SOUND.play()

                    if isBoard_full() and gameOver == False:
                        gameState_text = GAMESTATE_FONT.render(
                            'TIE GAME', True, WHITE)
                        WIN.blit(gameState_text, (WIDTH/2 - gameState_text.get_width() /
                                                  2, 630))
                        TIE_GAME_SOUND.play()

                    pygame.display.update()

            # If want to restart the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    draw_window()
                    player = PLAYER_X
                    for row in range(BOARD_ROWS):
                        for col in range(BOARD_COLS):
                            board[row][col] = 0
                    gameOver = False


if __name__ == '__main__':
    main()
