"""Board file."""

from const import DIMENSION
from piece import Bishop, King, Knight, Pawn, Queen, Rook
from square import Square
from move import Move


class Board:
    """Clas board."""

    def __init__(self) -> None:
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for column in range(DIMENSION)]

        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def calc_move(self, piece, row, column) -> None:
        """Func `calc_moves`."""

        def pawn_moves() -> None:
            steps = 1 if piece.moved else 2
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][column].isempty():
                        initial = Square(row, column)
                        final = Square(possible_move_row, column)
                        move = Move(initial, final)
                        piece.add_move(move)
                    else:
                        break
                else:
                    break
            possible_move_row = row + piece.dir
            possible_move_columns = [column - 1, column + 1]
            for possible_move_column in possible_move_columns:
                if Square.in_range(possible_move_row, possible_move_column):
                    if self.squares[possible_move_row][possible_move_column].has_enamy_piece(piece.color):
                        initial = Square(row, column)
                        final = Square(possible_move_row, possible_move_column)
                        move = Move(initial, final)
                        piece.add_move(move)

        def knight_moves() -> None:
            """Knight_moves."""
            possible_moves = [
                (row - 2, column + 1),
                (row - 1, column + 2),
                (row + 1, column + 2),
                (row + 2, column + 1),
                (row + 2, column - 1),
                (row + 1, column - 2),
                (row - 1, column - 2),
                (row - 2, column - 1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_column = possible_move

                if Square.in_range(possible_move_row, possible_move_column):
                    if self.squares[possible_move_row][possible_move_column].isempty_or_enamy(piece.color):
                        initial = Square(row, column)
                        final = Square(possible_move_row, possible_move_column)
                        move = Move(initial, final)
                        piece.add_move(move)

        def straightline_moves(incrs: list[tuple]) -> None:
            for incr in incrs:
                row_incr, column_incr = incr
                possible_move_row = row + row_incr
                possible_move_column = column + column_incr
                while True:
                    if Square.in_range(possible_move_row, possible_move_column):
                        initial = Square(row, column)
                        final = Square(possible_move_row, possible_move_column)
                        move = Move(initial, final)
                        if self.squares[possible_move_row][possible_move_column].isempty():
                            piece.add_move(move)

                        if self.squares[possible_move_row][possible_move_column].has_enamy_piece(piece.color):
                            piece.add_move(move)
                            break

                        if self.squares[possible_move_row][possible_move_column].has_team_piece(piece.color):
                            break

                    else:
                        break
                    possible_move_row = possible_move_row + row_incr
                    possible_move_column = possible_move_column + column_incr

        def king_mpves() -> None:
            adjs = [
                (row - 1, column + 0),
                (row - 1, column + 1),
                (row + 0, column + 1),
                (row + 1, column + 1),
                (row + 1, column + 0),
                (row + 1, column - 1),
                (row + 0, column - 1),
                (row - 1, column - 1)
            ]

            for possible_move in adjs:
                possible_move_row, possible_move_column = possible_move

                if Square.in_range(possible_move_row, possible_move_column):
                    if self.squares[possible_move_row][possible_move_column].isempty_or_enamy(piece.color):
                        initial = Square(row, column)
                        final = Square(possible_move_row, possible_move_column)
                        move = Move(initial, final)
                        piece.add_move(move)

        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1)
            ])
        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1)
            ])
        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1),
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1)
            ])
        elif isinstance(piece, King):
            king_mpves()

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

        self.squares[4][4] = Square(4, 4, King(color))

        # queens
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # kings
        self.squares[row_other][4] = Square(row_other, 4, King(color))
