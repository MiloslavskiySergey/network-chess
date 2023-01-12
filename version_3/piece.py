"""Piece file."""

from os.path import join

from settings import IMAGES_DIR


class Piece:
    """Clas piece."""

    def __init__(self, name: str, color: str, value: float, texture=None, texture_rect=None) -> None:
        self.name = name
        self.color = color
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size: int = 80) -> None:
        """Func `set_texture`."""
        self.texture = join(IMAGES_DIR, f'imgs-{size}px', f'{self.color}_{self.name}.png')

    def add_move(self, move) -> None:
        """Func add move."""
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []


class Pawn(Piece):
    """Clas pawn."""

    def __init__(self, color: str) -> None:
        self.dir = -1 if color == 'white' else 1
        super().__init__('pawn', color, 1.0)


class Knight(Piece):
    """Clas knight."""

    def __init__(self, color: str) -> None:
        super().__init__('knight', color, 3.0)


class Bishop(Piece):
    """Clas bishop."""

    def __init__(self, color: str) -> None:
        super().__init__('bishop', color, 3.001)


class Rook(Piece):
    """Clas rook."""

    def __init__(self, color: str) -> None:
        super().__init__('rook', color, 5.0)


class Queen(Piece):
    """Clas queen."""

    def __init__(self, color: str) -> None:
        super().__init__('queen', color, 9.0)


class King(Piece):
    """Clas king."""

    def __init__(self, color: str) -> None:
        super().__init__('king', color, 10000.0)
