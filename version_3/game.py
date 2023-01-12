"""Game file."""

import pygame
from const import DIMENSION, SQ_SIZE


class Game:
    """All render methods."""

    def __init__(self) -> None:
        pass

    # show methods

    def show_bg(self, surface: int) -> None:
        """Draw the squares on the board."""
        # colors = [pygame.Color('white'), pygame.Color('gray')] # noqa
        colors = [pygame.Color(234, 235, 200), pygame.Color(119, 154, 88)]
        for row in range(DIMENSION):
            for column in range(DIMENSION):
                color = colors[((row + column) % 2)]
                rect = pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(surface, color, rect)
