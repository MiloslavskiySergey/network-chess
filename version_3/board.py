"""Board file."""

import copy

from const import DIMENSION
from move import Move
from piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook
from square import Square


class Board:
    """Clas board."""

    def __init__(self) -> None:
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for column in range(DIMENSION)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move) -> None:
        initial = move.initial
        final = move.final

        # console board move update
        self.squares[initial.row][initial.column].piece = None
        self.squares[final.row][final.column].piece = piece

        # pawn promotion
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        # king castling
        if isinstance(piece, King) and self.castling(initial, final):
            diff = final.column - initial.column
            rook = piece.left_rook if (diff < 0) else piece.right_rook
            self.move(rook, rook.moves[-1])
        # move
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # set last move
        self.last_move = move

    def valid_move(self, piece, move) -> bool:
        return move in piece.moves

    def check_promotion(self, piece: Piece, final) -> None:
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.column].piece = Queen(piece.color)

    def castling(self, initial, final) -> bool:
        return abs(initial.column - final.column) == 2

    def in_check(self, piece, move) -> bool:
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)

        for row in range(DIMENSION):
            for column in range(DIMENSION):
                if temp_board.squares[row][column].has_enamy_piece(piece.color):
                    p = temp_board.squares[row][column].piece
                    temp_board.calc_moves(p, row, column, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False

    def calc_moves(self, piece, row, column, bool=True) -> None:
        """Func `calc_moves`."""

        def pawn_moves() -> None:
            # steps
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][column].isempty():
                        # create initial and final move squares
                        initial = Square(row, column)
                        final = Square(possible_move_row, column)
                        # create a new move
                        move = Move(initial, final)

                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)
                    # blocked
                    else:
                        break
                # is nor range
                else:
                    break

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_columns = [column - 1, column + 1]
            for possible_move_column in possible_move_columns:
                if Square.in_range(possible_move_row, possible_move_column) and \
                        self.squares[possible_move_row][possible_move_column].has_enamy_piece(piece.color):
                    # create initial and final move squares
                    initial = Square(row, column)
                    final_piece = self.squares[possible_move_row][possible_move_column].piece
                    final = Square(possible_move_row, possible_move_column, final_piece)
                    # create a new move
                    move = Move(initial, final)

                    # check potencial checks
                    if bool:
                        if not self.in_check(piece, move):
                            # append new move
                            piece.add_move(move)
                    else:
                        # append new move
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

                if Square.in_range(possible_move_row, possible_move_column) and \
                        self.squares[possible_move_row][possible_move_column].isempty_or_enamy(piece.color):
                    # create squares of the new move
                    initial = Square(row, column)
                    final_piece = self.squares[possible_move_row][possible_move_column].piece
                    final = Square(possible_move_row, possible_move_column, final_piece)
                    # create new move
                    move = Move(initial, final)

                    # check potencial checks
                    if bool:
                        if not self.in_check(piece, move):
                            # append new valid move
                            piece.add_move(move)
                        else:
                            break
                    else:
                        # append new valid move
                        piece.add_move(move)

        def straightline_moves(incrs: list[tuple]) -> None:
            for incr in incrs:
                row_incr, column_incr = incr
                possible_move_row = row + row_incr
                possible_move_column = column + column_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_column):
                        # create squares of the possible new move
                        initial = Square(row, column)
                        final_piece = self.squares[possible_move_row][possible_move_column].piece
                        final = Square(possible_move_row, possible_move_column, final_piece)
                        # create a possible new move
                        move = Move(initial, final)

                        # empty = continue looping
                        if self.squares[possible_move_row][possible_move_column].isempty():
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)

                        # has enemy piece = add move + break
                        elif self.squares[possible_move_row][possible_move_column].has_enamy_piece(piece.color):
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)
                            break

                        # has team piece = break
                        elif self.squares[possible_move_row][possible_move_column].has_team_piece(piece.color):
                            break

                    # not in range
                    else:
                        break
                    possible_move_row = possible_move_row + row_incr
                    possible_move_column = possible_move_column + column_incr

        def king_moves() -> None:
            adjs = [
                (row - 1, column + 0),  # up
                (row - 1, column + 1),  # up-right
                (row + 0, column + 1),  # right
                (row + 1, column + 1),  # down-right
                (row + 1, column + 0),  # down
                (row + 1, column - 1),  # down-left
                (row + 0, column - 1),  # left
                (row - 1, column - 1)  # up-left
            ]

            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_column = possible_move

                if Square.in_range(possible_move_row, possible_move_column) and \
                        self.squares[possible_move_row][possible_move_column].isempty_or_enamy(piece.color):
                    # create squares of the new move
                    initial = Square(row, column)
                    final = Square(possible_move_row, possible_move_column)  # piece=piece
                    # create new move
                    move = Move(initial, final)

                    # check potencial checks
                    if bool:
                        if not self.in_check(piece, move):
                            # append new valid move
                            piece.add_move(move)
                        else:
                            break
                    else:
                        # append new valid move
                        piece.add_move(move)

            # castling moves
            if not piece.moved:
                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook) and not left_rook.moved:
                    for column_castling in range(1, 4):
                        # castling is not possible because there ate pieces in between
                        if self.squares[row][column_castling].has_piece():
                            break

                        if column_castling == 3:
                            # adds left rook to king
                            piece.left_rook = left_rook

                            # rook move
                            initial = Square(row, 0)
                            final = Square(row, 3)
                            move_rook = Move(initial, final)

                            # king move
                            initial = Square(row, column)
                            final = Square(row, 2)
                            move_king = Move(initial, final)

                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move_king) and not self.in_check(left_rook, move_rook):
                                    # append new move to rook
                                    left_rook.add_move(move_rook)
                                    # append new move to king
                                    piece.add_move(move_king)
                            else:
                                # append new move to rook
                                left_rook.add_move(move_rook)
                                # append new move to king
                                piece.add_move(move_king)
                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook) and not right_rook.moved:
                    for column_castling in range(5, 7):
                        # castling is not possible because there ate pieces in between
                        if self.squares[row][column_castling].has_piece():
                            break

                        if column_castling == 6:
                            # adds right rook to king
                            piece.right_rook = right_rook

                            # rook move
                            initial = Square(row, 7)
                            final = Square(row, 5)
                            move_rook = Move(initial, final)

                            # king move
                            initial = Square(row, column)
                            final = Square(row, 6)
                            move_king = Move(initial, final)

                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move_king) and not self.in_check(right_rook, move_rook):
                                    # append new move to rook
                                    right_rook.add_move(move_rook)
                                    # append new move to king
                                    piece.add_move(move_king)
                            else:
                                # append new move to rook
                                right_rook.add_move(move_rook)
                                # append new move to king
                                piece.add_move(move_king)

        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1),  # up-right
                (-1, -1),  # up-left
                (1, 1),  # down-right
                (1, -1)  # down-left
            ])
        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0),  # up
                (0, 1),  # right
                (1, 0),  # down
                (0, -1)  # left
            ])
        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1),  # up-right
                (-1, -1),  # up-left
                (1, 1),  # down-right
                (1, -1),  # down-left
                (-1, 0),  # up
                (0, 1),  # right
                (1, 0),  # down
                (0, -1)  # left
            ])
        elif isinstance(piece, King):
            king_moves()

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
