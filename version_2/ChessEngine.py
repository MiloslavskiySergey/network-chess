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
            ['blackPawn', 'blackPawn', 'blackPawn', 'blackPawn', 'blackPawn', 'blackPawn', 'whitePawn', 'blackPawn'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['whitePawn', 'whitePawn', 'whitePawn', 'whitePawn', 'whitePawn', 'whitePawn', 'blackPawn', 'whitePawn'],
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
        self.check_mate = False
        self.stale_mate = False
        self.enpassant_possible = ()

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
        # pawn promotion
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_column] = move.piece_moved[0:5] + 'Queen'

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

    def get_valid_moves(self) -> list:
        """All moves considering checks."""
        # generate all possible moves
        moves = self.get_all_possible_moves()
        # for each move, make the move
        for index in range(len(moves) - 1, -1, -1):
            # generate all opponent's moves
            # for each of your opponent's moves, see if they  attack your king
            self.make_move(moves[index])
            self.white_to_move = not self.white_to_move
            if self.in_check():
                # if they do attack your king, not a valid move
                moves.remove(moves[index])
            self.white_to_move = not self.white_to_move
            self.undo_move()
        if len(moves) == 0:
            if self.in_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False
        return moves

    def in_check(self,) -> bool:
        """Determine if the current player is in check."""
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    def square_under_attack(self, row: int, column: int):
        """Determine if the enemy can attack the square row, column."""
        self.white_to_move = not self.white_to_move
        opp_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        return any(move.end_row == row and move.end_column == column for move in opp_moves)
        """for move in opp_moves:
            if move.end_row == row and move.end_column == column:
                return True
        return False"""

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
        if self.white_to_move:
            if self.board[row - 1][column] == '--':
                moves.append(Move((row, column), (row - 1, column), self.board))
                if row == 6 and self.board[row - 2][column] == '--':
                    moves.append(Move((row, column), (row - 2, column), self.board))
            if column - 1 >= 0:
                if self.board[row - 1][column - 1][0:5] == 'black':
                    moves.append(Move((row, column), (row - 1, column - 1), self.board))
                elif (row - 1, column - 1) == self.enpassant_possible:
                    moves.append(Move((row, column), (row - 1, column - 1), self.board, is_enpassant_move=True))
            if column + 1 <= 7:
                if self.board[row - 1][column + 1][0:5] == 'black':
                    moves.append(Move((row, column), (row - 1, column + 1), self.board))
                elif (row - 1, column + 1) == self.enpassant_possible:
                    moves.append(Move((row, column), (row - 1, column + 1), self.board, is_enpassant_move=True))
        else:
            if self.board[row + 1][column] == '--':
                moves.append(Move((row, column), (row + 1, column), self.board))
                if row == 1 and self.board[row + 2][column] == '--':
                    moves.append(Move((row, column), (row + 2, column), self.board))
            if column - 1 >= 0:
                if self.board[row + 1][column - 1][0:5] == 'white':
                    moves.append(Move((row, column), (row + 1, column - 1), self.board))
                elif (row + 1, column - 1) == self.enpassant_possible:
                    moves.append(Move((row, column), (row + 1, column - 1), self.board, is_enpassant_move=True))
            if column + 1 <= 7:
                if self.board[row + 1][column + 1][0:5] == 'white':
                    moves.append(Move((row, column), (row + 1, column + 1), self.board))
                elif (row + 1, column + 1) == self.enpassant_possible:
                    moves.append(Move((row, column), (row + 1, column + 1), self.board, is_enpassant_move=True))

    def get_rook_moves(self, row: int, column: int, moves: list) -> None:
        """Get all the Rook moves for the Rook located at row, column and add these moves to the list."""
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = 'black' if self.white_to_move else 'white'
        for direction in directions:
            for index in range(1, 8):
                end_row = row + direction[0] * index
                end_column = column + direction[1] * index
                if 0 <= end_row < 8 and 0 <= end_column < 8:
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
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = 'white' if self.white_to_move else 'black'
        for knight_move in knight_moves:
            end_row = row + knight_move[0]
            end_column = column + knight_move[1]
            if 0 <= end_row < 8 and 0 <= end_column < 8:
                end_piece = self.board[end_row][end_column]
                if end_piece[0:5] != ally_color:
                    moves.append(Move((row, column), (end_row, end_column), self.board))

    def get_bishop_moves(self, row: int, column: int, moves: list) -> None:
        """Get all the Bishop moves for the Bishop located at row, column and add these moves to the list."""
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = 'black' if self.white_to_move else 'white'
        for direction in directions:
            for index in range(1, 8):
                end_row = row + direction[0] * index
                end_column = column + direction[1] * index
                if 0 <= end_row < 8 and 0 <= end_column < 8:
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
        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally_color = 'white' if self.white_to_move else 'black'
        for index in range(8):
            end_row = row + king_moves[index][0]
            end_column = column + king_moves[index][1]
            if 0 <= end_row < 8 and 0 <= end_column < 8:
                end_piece = self.board[end_row][end_column]
                if end_piece[0:5] != ally_color:
                    moves.append(Move((row, column), (end_row, end_column), self.board))


class Move():
    """Move figures."""

    ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_columns = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    columns_to_files = {v: k for k, v in files_to_columns.items()}

    def __init__(self, start_sq: list, end_sq: list, board: list, is_enpassant_move=False) -> None:
        self.start_row = start_sq[0]
        self.start_column = start_sq[1]
        self.end_row = end_sq[0]
        self.end_column = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_column]
        self.piece_captured = board[self.end_row][self.end_column]
        # pawn promotion
        self.is_pawn_promotion = (self.piece_moved == 'whitePawn' and self.end_row == 0) or \
            (self.piece_moved == 'blackPawn' and self.end_row == 7)
        # en passant
        self.is_enpassant_move = is_enpassant_move
        self.move_id = self.start_row * 1000 + self.start_column * 100 + self.end_row * 10 + self.end_column

    def __eq__(self, other):
        """Overriding the equals method."""
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
