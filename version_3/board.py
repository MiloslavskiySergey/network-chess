"""Board file."""

from const import DIMENSION
from square import Square


class Board:
    """Clas board."""

    def __init__(self) -> None:
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for column in range(DIMENSION)]

        self._create()

    def _create(self):
        for row in range(DIMENSION):
            for column in range(DIMENSION):
                self.squares[row][column] = Square(row, column)

    def _add_pieces(self, color):
        pass
