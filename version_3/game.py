"""Game file."""

import pygame
from board import Board
from const import DIMENSION, SQ_SIZE
from dragger import Dragger


class Game:
    """All render methods."""

    def __init__(self) -> None:
        self.board = Board()
        self.dragger = Dragger()

    # show methods

    def show_bg(self, surface: int) -> None:
        """Show board."""
        # colors = [pygame.Color('white'), pygame.Color('gray')] # noqa
        colors = [pygame.Color(234, 235, 200), pygame.Color(119, 154, 88)]
        for row in range(DIMENSION):
            for column in range(DIMENSION):
                color = colors[((row + column) % 2)]
                rect = pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface: int) -> None:
        """Show pieces."""
        for row in range(DIMENSION):
            for column in range(DIMENSION):
                if self.board.squares[row][column].has_piece():
                    piece = self.board.squares[row][column].piece

                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = column * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)
