"""Game file."""

import pygame
from board import Board
from config import Config
from const import DIMENSION, HEIGHT, SQ_SIZE
from dragger import Dragger
from square import Square


class Game:
    """All render methods."""

    def __init__(self) -> None:
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    # show methods

    def show_bg(self, surface: int) -> None:
        """Show board."""
        theme = self.config.theme
        colors = [theme.bg.light, theme.bg.dark]

        for row in range(DIMENSION):
            for column in range(DIMENSION):
                color = colors[((row + column) % 2)]
                rect = pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if column == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label
                    label = self.config.font.render(str(DIMENSION - row), 1, color)
                    label_position = (5, 5 + row * SQ_SIZE)
                    # blit
                    surface.blit(label, label_position)
                # column coordinates
                if row == 7:
                    color = theme.bg.dark if (row + column) % 2 == 0 else theme.bg.light
                    # label
                    label = self.config.font.render(Square.get_alphacolumn(column), 1, color)
                    label_position = (column * SQ_SIZE + SQ_SIZE - 20, HEIGHT - 20)
                    # blit
                    surface.blit(label, label_position)

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
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                color = theme.moves.light if (move.final.row + move.final.column) % 2 == 0 else theme.moves.dark
                rect = (move.final.column * SQ_SIZE, move.final.row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface: int) -> None:
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for position in [initial, final]:
                color = theme.trace.light if (position.row + position.column) % 2 == 0 else theme.trace.dark
                rect = (position.column * SQ_SIZE, position.row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface: int) -> None:
        if self.hovered_sqr:
            color = (180, 180, 180)
            rect = (self.hovered_sqr.column * SQ_SIZE, self.hovered_sqr.row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    def next_turn(self) -> None:
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, column) -> None:
        self.hovered_sqr = self.board.squares[row][column]

    def change_theme(self) -> None:
        self.config.change_theme()

    def play_sound(self, captured=False) -> None:
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()
