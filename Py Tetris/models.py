# models.py
import pygame
import time
import random

# Constants
BLUE = (0, 0, 155)
BOX_SIZE = 20
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BOARD_WIDTH = 10

# Tetris shapes
SHAPE_TEMPLATES = {
    'S': [['.....', '.....', '..cc.', '.cc..', '.....'],
          ['.....', '..c..', '..cc.', '...c.', '.....']],
    'I': [['..c..', '..c..', '..c..', '..c..', '.....'],
          ['.....', '.....', 'cccc.', '.....', '.....']],
    'O': [['.....', '.....', '.cc..', '.cc..', '.....']]
}

class TetrisPiece:
    def __init__(self):
        self.shape = random.choice(list(SHAPE_TEMPLATES.keys()))
        self.rotation = 0
        self.column = 2  # Updated from 4
        self.row = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(SHAPE_TEMPLATES[self.shape])

def initialize_game_matrix():
    columns, rows = 10, 20
    return [['.' for _ in range(columns)] for _ in range(rows)]

def is_within_board(row, column):
    return 0 <= column < 10 and row < 20

def is_position_valid(game_matrix, piece, adj_column=0, adj_row=0):
    shape_template = SHAPE_TEMPLATES[piece.shape][piece.rotation]
    for row in range(5):
        for col in range(5):
            if shape_template[row][col] == '.':
                continue
            if not is_within_board(piece.row + row + adj_row, piece.column + col + adj_column):
                return False
            if game_matrix[piece.row + row + adj_row][piece.column + col + adj_column] != '.':
                return False
    return True

def update_game_matrix_with_piece(matrix, piece):
    shape_template = SHAPE_TEMPLATES[piece.shape][piece.rotation]
    for row in range(5):
        for col in range(5):
            if shape_template[row][col] != '.':
                matrix[piece.row + row][piece.column + col] = 'c'
    return matrix

def render_board(screen, matrix):
    for row in range(20):
        for column in range(10):
            if matrix[row][column] != '.':
                draw_block(screen, row, column, (255, 255, 255), (217, 222, 226))

def draw_block(screen, row, col, color, shadow_color):
    origin_x = 100 + 5 + (col * BOX_SIZE + 1)
    origin_y = 50 + 5 + (row * BOX_SIZE + 1)
    pygame.draw.rect(screen, shadow_color, [origin_x, origin_y, BOX_SIZE, BOX_SIZE])
    pygame.draw.rect(screen, color, [origin_x, origin_y, BOX_SIZE - 2, BOX_SIZE - 2])

def render_active_piece(screen, piece):
    shape_to_draw = SHAPE_TEMPLATES[piece.shape][piece.rotation]
    for row in range(5):
        for col in range(5):
            if shape_to_draw[row][col] != '.':
                draw_block(screen, piece.row + row, piece.column + col, (255, 255, 255), (217, 222, 226))

def render_score(screen, score):
    font = pygame.font.Font('freesansbold.ttf', 18)
    score_surface = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_surface, (SCREEN_WIDTH - 150, 20))

def clear_full_lines(game_matrix):
    lines_cleared = 0
    for row in range(20):
        if all(cell != '.' for cell in game_matrix[row]):
            for row_to_move_down in range(row, 0, -1):
                game_matrix[row_to_move_down] = game_matrix[row_to_move_down - 1]
            game_matrix[0] = ['.'] * 10
            lines_cleared += 1
    return lines_cleared

def handle_user_input(game_matrix, piece, move_speed):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and is_position_valid(game_matrix, piece, adj_column=-1):
                piece.column -= 1
            elif event.key == pygame.K_RIGHT and is_position_valid(game_matrix, piece, adj_column=1):
                piece.column += 1
            elif event.key == pygame.K_UP:
                piece.rotate()
                if not is_position_valid(game_matrix, piece):
                    piece.rotate()
                    piece.rotate()
                    piece.rotate()
            elif event.key == pygame.K_DOWN:
                move_speed = 0.1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                move_speed = 0.3
    return move_speed
