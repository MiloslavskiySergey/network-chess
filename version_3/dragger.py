"""Dragger file."""
import pygame
from const import SQ_SIZE


class Dragger:
    """Clas dragger."""

    def __init__(self) -> None:
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initional_row = 0
        self.initional_column = 0

    def update_blit(self, surface: int):
        """Func `update_blit`."""
        # texture
        self.piece.set_texture(size=128)
        texture = self.piece.texture
        # image
        img = pygame.image.load(texture)
        # rect
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        # blit
        surface.blit(img, self.piece.texture_rect)

    def update_mouse(self, position: tuple) -> None:
        """Func `update_mouse`."""
        self.mouseX, self.mouseY = position

    def save_initial(self, position: tuple) -> None:
        """Func `save_position`."""
        self.initional_row = position[1] // SQ_SIZE
        self.initional_column = position[0] // SQ_SIZE

    def drag_piece(self, piece) -> None:
        """Func `drag_piece`."""
        self.piece = piece
        self.dragging = True

    def undrad_piece(self,):
        """Func `undrag_piece`."""
        self.piece = None
        self.dragging = False
