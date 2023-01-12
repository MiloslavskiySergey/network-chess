"""Board file."""

from const import DIMENSION
from piece import Bishop, King, Knight, Pawn, Queen, Rook
from square import Square


class Board:
    """Clas board."""

    def __init__(self) -> None:
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for column in range(DIMENSION)]

        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def _create(self) -> None:
        for row in range(DIMENSION):
            for column in range(DIMENSION):
                self.squares[row][column] = Square(row, column)

    def _add_pieces(self, color: str) -> None:
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for column in range(DIMENSION):
            self.squares[row_pawn][column] = Square(row_pawn, column, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queens
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # kings
        self.squares[row_other][4] = Square(row_other, 4, King(color))
