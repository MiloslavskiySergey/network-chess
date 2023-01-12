"""Game file."""

import pygame
from board import Board
from const import DIMENSION, SQ_SIZE
from dragger import Dragger


class Game:
    """All render methods."""

    def __init__(self) -> None:
        self.next_player = 'white'
        self.hovered_sqr = None
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

    def show_moves(self, surface: int) -> None:

        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                color = '#C86464' if (move.final.row + move.final.column) % 2 == 0 else '#C84646'
                rect = (move.final.column * SQ_SIZE, move.final.row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface: int) -> None:
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for position in [initial, final]:
                color = (244, 247, 116) if (position.row + position.column) % 2 == 0 else (172, 195, 51)
                rect = (position.column * SQ_SIZE, position.row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface: int):
        if self.hovered_sqr:
            color = (180, 180, 180)
            rect = (self.hovered_sqr.column * SQ_SIZE, self.hovered_sqr.row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    def next_turn(self) -> None:
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, column):
        self.hovered_sqr = self.board.squares[row][column]
