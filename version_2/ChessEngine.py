"""
This class is responsible for storing all the information about the current state of a chess game. # noqa
It will also be responsible for dermining the valid moves at the current state. It will also keep a move log.
"""


class GameState():
    """Game state."""

    def __init__(self):
        self.board: list[str] = [
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
        self.white_to_move: bool = True
        self.move_log: list = []

    def make_move(self, move) -> None:
        """Make move."""
        self.board[move.start_row][move.start_column] = '--'
        self.board[move.end_row][move.end_column] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move


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
        self.piece_csptured = board[self.end_row][self.end_column]

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
