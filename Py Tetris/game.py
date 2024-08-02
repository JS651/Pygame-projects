# game.py
import pygame
import sys
import time
from models import (
    initialize_game_matrix,
    render_board,
    render_active_piece,
    render_score,
    is_position_valid,
    handle_user_input,
    clear_full_lines,
    TetrisPiece,
    update_game_matrix_with_piece
)

class TetrisGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('Tetris')
        self.game_matrix = initialize_game_matrix()
        self.last_move_time = time.time()
        self.current_piece = TetrisPiece()
        self.score = 0
        self.move_speed = 0.3

    def main_loop(self):
        while True:
            self.screen.fill((0, 0, 0))
            if time.time() - self.last_move_time > self.move_speed:
                self.current_piece.row += 1
                self.last_move_time = time.time()

            render_active_piece(self.screen, self.current_piece)
            pygame.draw.rect(
                self.screen,
                (0, 0, 155),
                [100, 50, 10 * 20 + 10, 20 * 20 + 10], 5
            )

            render_board(self.screen, self.game_matrix)
            render_score(self.screen, self.score)

            self.move_speed = handle_user_input(self.game_matrix, self.current_piece, self.move_speed)
            if not is_position_valid(self.game_matrix, self.current_piece, adj_row=1):
                self.game_matrix = update_game_matrix_with_piece(self.game_matrix, self.current_piece)
                lines_cleared = clear_full_lines(self.game_matrix)
                self.score += lines_cleared
                self.current_piece = TetrisPiece()

            pygame.display.update()
            for event in pygame.event.get(pygame.QUIT):
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    game = TetrisGame()
    game.main_loop()
