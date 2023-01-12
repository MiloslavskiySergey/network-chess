"""Main file."""
import sys
from os.path import join

import pygame
from const import HEIGHT, SQ_SIZE, WIDTH
from game import Game
from settings import IMAGES_DIR
from square import Square
from move import Move


class Main:
    """Class main."""

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Game chess')
        pygame.display.set_icon(pygame.image.load(join(IMAGES_DIR, 'iconChess.png')))
        self.game = Game()

    def mainloop(self) -> None:
        """Call other classes."""
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouseY // SQ_SIZE
                    clicked_column = dragger.mouseX // SQ_SIZE

                    if board.squares[clicked_row][clicked_column].has_piece():
                        piece = board.squares[clicked_row][clicked_column].piece

                        if piece.color == game.next_player:
                            board.calc_move(piece, clicked_row, clicked_column)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQ_SIZE
                    motion_column = event.pos[0] // SQ_SIZE

                    game.set_hover(motion_row, motion_column)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                # click release
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQ_SIZE
                        released_column = dragger.mouseX // SQ_SIZE

                        initial = Square(dragger.initial_row, dragger.initial_column)
                        final = Square(released_row, released_column)
                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                            game.next_turn()

                    dragger.undrad_piece()

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()


if __name__ == '__main__':
    main = Main()
    main.mainloop()
