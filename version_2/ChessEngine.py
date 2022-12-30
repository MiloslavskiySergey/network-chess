"""
This class is responsible for storing all the information about the current state of a chess game. # noqa
It will also be responsible for dermining the valid moves at the current state. It will also keep a move log.
"""


class GameState():
    """Game state."""

    def __init__(self) -> None:
        self.board = [
            ['blackRook', 'blackKnight', 'blackBishop', 'blackQueen',
                'blackKing', 'blackBishop', 'blackKnight', 'blackRook'],
            ['blackPawn', 'blackPawn', 'blackPawn', 'blackPawn', 'blackPawn', 'blackPawn', 'blackPawn', 'blackPawn'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['whitePawn', 'whitePawn', 'whitePawn', 'whitePawn', 'whitePawn', 'whitePawn', 'whitePawn', 'whitePawn'],
            ['whiteRook', 'whiteKnight', 'whiteBishop', 'whiteQueen',
                'whiteKing', 'whiteBishop', 'whiteKnight', 'whiteRook'],
        ]
        self.move_functions = {'Pawn': self.get_pawn_moves,
                               'Rook': self.get_rook_moves,
                               'Knight': self.get_knight_moves,
                               'Bishop': self.get_bishop_moves,
                               'Queen': self.get_queen_moves,
                               'King': self.get_king_moves
                               }
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.in_check = False
        self.pins = []
        self.checks = []

    def make_move(self, move: 'Move') -> None:
        """Make move."""
        self.board[move.start_row][move.start_column] = '--'
        self.board[move.end_row][move.end_column] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        if move.piece_moved == 'whiteKing':
            self.white_king_location = (move.end_row, move.end_column)
        elif move.piece_moved == 'blackKing':
            self.black_king_location = (move.end_row, move.end_column)

    def undo_move(self) -> None:
        """Undo the last move made."""
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_column] = move.piece_moved
            self.board[move.end_row][move.end_column] = move.piece_captured
            self.white_to_move = not self.white_to_move
            if move.piece_moved == 'whiteKing':
                self.white_king_location = (move.start_row, move.start_column)
            elif move.piece_moved == 'blackKing':
                self.black_king_location = (move.start_row, move.start_column)

    def get_valid_moves(self):
        """All moves considering checks."""
        # generate all possible moves
        moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()
        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_column = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_column = self.black_king_location[1]
        if self.in_check:
            if len(self.checks) == 1:  # only 1 check, block check or move king
                moves = self.get_all_possible_moves()
                # to block a check you must move a piece into one of the squares between the enemy piece and king
                check = self.checks[0]  # check information
                check_row = check[0]
                check_column = check[1]
                piece_checking = self.board[check_row][check_column]  # enemy piece causing the check
                valid_squares = []  # squares that pieces can move to
                # if knight, must capture knight or move king, other pieces can be blocked
                if piece_checking[1] == 'Knight':
                    valid_squares = [(check_row, check_column)]
                else:
                    for index in range(1, 8):
                        valid_square = (king_row + check[2] * index, king_column + check[3] * index)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_column:
                            break
                for index in range(len(moves) - 1, -1, -1):
                    if moves[index].piece_moved[1] == 'King':
                        if not (moves[index].end_row, moves[index].end_column) in valid_squares:
                            moves.remove(moves[index])
            else:
                self.get_king_moves(king_row, king_column, moves)
        else:
            moves = self.get_all_possible_moves()
        return moves

    def get_all_possible_moves(self):
        """All moves without considering checks."""
        moves = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                turn = self.board[row][column][0:5]
                if (turn == 'white' and self.white_to_move) or (turn == 'black' and not self.white_to_move):
                    piece = self.board[row][column][5:]
                    self.move_functions[piece](row, column, moves)
        return moves

    def get_pawn_moves(self, row: int, column: int, moves: list) -> None:
        """Get all the Pawn moves for the pawn located at row, column and add these moves to the list."""
        piece_pinned = False
        pin_direction = ()
        for index in range(len(self.pins) - 1, -1, -1):
            if self.pins[index][0] == row and self.pins[index][1] == column:
                piece_pinned = True
                pin_direction = (self.pins[index][2], self.pins[index][3])
                self.pins.remove(self.pins[index])
                break
        # white pawn moves
        if self.white_to_move:
            if self.board[row - 1][column] == '--':
                if not piece_pinned or pin_direction == (-1, 0):
                    moves.append(Move((row, column), (row - 1, column), self.board))
                    if row == 6 and self.board[row - 2][column] == '--':
                        moves.append(Move((row, column), (row - 2, column), self.board))
            # capture to left
            if column - 1 >= 0:
                if self.board[row - 1][column - 1][0:5] == 'black':
                    if not piece_pinned or pin_direction == (-1, -1):
                        moves.append(Move((row, column), (row - 1, column - 1), self.board))
            # capture to right
            if column + 1 <= 7:
                if self.board[row - 1][column + 1][0:5] == 'black':
                    if not piece_pinned or pin_direction == (-1, 1):
                        moves.append(Move((row, column), (row - 1, column + 1), self.board))
        # black pawn moves
        else:
            if self.board[row + 1][column] == '--':
                if not piece_pinned or pin_direction == (1, 0):
                    moves.append(Move((row, column), (row + 1, column), self.board))
                    if row == 1 and self.board[row + 2][column] == '--':
                        moves.append(Move((row, column), (row + 2, column), self.board))
            # capture to left
            if column - 1 >= 0:
                if self.board[row + 1][column - 1][0:5] == 'white':
                    if not piece_pinned or pin_direction == (1, -1):
                        moves.append(Move((row, column), (row + 1, column - 1), self.board))
            # capture to right
            if column + 1 <= 7:
                if self.board[row + 1][column + 1][0:5] == 'white':
                    if not piece_pinned or pin_direction == (1, 1):
                        moves.append(Move((row, column), (row + 1, column + 1), self.board))

    def get_rook_moves(self, row: int, column: int, moves: list) -> None:
        """Get all the Rook moves for the Rook located at row, column and add these moves to the list."""
        piece_pinned = False
        pin_direction = ()
        for index in range(len(self.pins) - 1, -1, -1):
            if self.pins[index][0] == row and self.pins[index][1] == column:
                piece_pinned = True
                pin_direction = (self.pins[index][2], self.pins[index][3])
                if self.board[row][column][1] != 'Queen':
                    self.pins.remove(self.pins[index])
                break
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = 'black' if self.white_to_move else 'white'
        for direction in directions:
            for index in range(1, 8):
                end_row = row + direction[0] * index
                end_column = column + direction[1] * index
                if 0 <= end_row < 8 and 0 <= end_column < 8:
                    if not piece_pinned or \
                            pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_column]
                        if end_piece == '--':
                            moves.append(Move((row, column), (end_row, end_column), self.board))
                        elif end_piece[0:5] == enemy_color:
                            moves.append(Move((row, column), (end_row, end_column), self.board))
                            break
                        else:
                            break
                else:
                    break

    def get_knight_moves(self, row: int, column: int, moves: list) -> None:
        """Get all the Knight moves for the Knight located at row, column and add these moves to the list."""
        piece_pinned = False
        for index in range(len(self.pins) - 1, -1, -1):
            if self.pins[index][0] == row and self.pins[index][1] == column:
                piece_pinned = True
                self.pins.remove(self.pins[index])
                break
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = 'white' if self.white_to_move else 'black'
        for knight_move in knight_moves:
            end_row = row + knight_move[0]
            end_column = column + knight_move[1]
            if 0 <= end_row < 8 and 0 <= end_column < 8:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_column]
                    if end_piece[0:5] != ally_color:
                        moves.append(Move((row, column), (end_row, end_column), self.board))

    def get_bishop_moves(self, row: int, column: int, moves: list) -> None:
        """Get all the Bishop moves for the Bishop located at row, column and add these moves to the list."""
        piece_pinned = False
        pin_direction = ()
        for index in range(len(self.pins) - 1, -1, -1):
            if self.pins[index][0] == row and self.pins[index][1] == column:
                piece_pinned = True
                pin_direction = (self.pins[index][2], self.pins[index][3])
                self.pins.remove(self.pins[index])
                break
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = 'black' if self.white_to_move else 'white'
        for direction in directions:
            for index in range(1, 8):
                end_row = row + direction[0] * index
                end_column = column + direction[1] * index
                if 0 <= end_row < 8 and 0 <= end_column < 8:
                    if not piece_pinned or \
                            pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_column]
                        if end_piece == '--':
                            moves.append(Move((row, column), (end_row, end_column), self.board))
                        elif end_piece[0:5] == enemy_color:
                            moves.append(Move((row, column), (end_row, end_column), self.board))
                            break
                        else:
                            break
                else:
                    break

    def get_queen_moves(self, row: int, column: int, moves: list) -> None:
        """Get all the Queen moves for the Queen located at row, column and add these moves to the list."""
        self.get_rook_moves(row, column, moves)
        self.get_bishop_moves(row, column, moves)

    def get_king_moves(self, row: int, column: int, moves: list) -> None:
        """Get all the King moves for the King located at row, column and add these moves to the list."""
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        column_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = 'white' if self.white_to_move else 'black'
        for index in range(8):
            end_row = row + row_moves[index]
            end_column = column + column_moves[index]
            if 0 <= end_row < 8 and 0 <= end_column < 8:
                end_piece = self.board[end_row][end_column]
                if end_piece[0:5] != ally_color:
                    if ally_color == 'white':
                        self.white_king_location = (end_row, end_column)
                    else:
                        self.black_king_location = (end_row, end_column)
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                    if ally_color == 'white':
                        self.white_king_location = (row, column)
                    else:
                        self.black_king_location = (row, column)

    def check_for_pins_and_checks(self,):
        """Returns if the player is in check, a list of pins, and a list of checks."""
        pins = []
        checks = []
        in_check = False
        if self.white_to_move:
            enemy_color = 'black'
            ally_color = 'white'
            start_row = self.white_king_location[0]
            start_column = self.white_king_location[1]
        else:
            enemy_color = 'white'
            ally_color = 'black'
            start_row = self.black_king_location[0]
            start_column = self.black_king_location[1]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for direction in range(len(directions)):
            direct = directions[direction]
            possible_pin = ()
            for index in range(1, 8):
                end_row = start_row + direct[0] * index
                end_column = start_column + direct[1] * index
                if 0 <= end_row < 8 and 0 <= end_column < 8:
                    end_piece = self.board[end_row][end_column]
                    if end_piece[0:5] == ally_color and end_piece[5:] != 'King':
                        if possible_pin == ():
                            possible_pin = (end_row, end_column, direct[0], direct[1])
                        else:
                            break
                    elif end_piece[0:5] == enemy_color:
                        type = end_piece[5:]
                        if (0 <= direction <= 3 and type == 'Rook') or \
                                (4 <= direction <= 7 and type == 'Bishop') or \
                                (index == 1 and type == 'Pawn' and
                                 ((enemy_color == 'white' and 6 <= direction <= 7) or
                                  (enemy_color == 'black' and 4 <= direction <= 5))) or \
                                (type == 'Queen') or (index == 1 and type == 'King'):
                            if possible_pin == ():
                                in_check = True
                                checks.append((end_row, end_column, direct[0], direct[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            break
                else:
                    break
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for move in knight_moves:
            end_row = start_row + move[0]
            end_column = start_column + move[1]
            if 0 <= end_row < 8 and 0 <= end_column < 8:
                end_piece = self.board[end_row][end_column]
                if end_piece[0:5] == enemy_color and end_piece[5:] == 'Knight':
                    in_check = True
                    checks.append((end_row, end_column, move[0], move[1]))
        return in_check, pins, checks


class Move():
    """Move figures."""

    ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_columns = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    columns_to_files = {v: k for k, v in files_to_columns.items()}

    def __init__(self, start_sq: list, end_sq: list, board: list) -> None:
        self.start_row = start_sq[0]
        self.start_column = start_sq[1]
        self.end_row = end_sq[0]
        self.end_column = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_column]
        self.piece_captured = board[self.end_row][self.end_column]
        self.move_id = self.start_row * 1000 + self.start_column * 100 + self.end_row * 10 + self.end_column

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self) -> str:
        """Get chess notation."""
        return self.get_rank_file(
            self.start_row,
            self.start_column
        ) + self.get_rank_file(
            self.end_row,
            self.end_column
        )

    def get_rank_file(self, row: int, column: int) -> str:
        """Get rank file."""
        return self.columns_to_files[column] + self.rows_to_ranks[row]
