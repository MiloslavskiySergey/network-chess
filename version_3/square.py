"""Square file."""


class Square:
    """Clas square."""

    ALPHACOLUMNS = {
        0: 'a',
        1: 'b',
        2: 'c',
        3: 'd',
        4: 'e',
        5: 'f',
        6: 'g',
        7: 'h'
    }

    def __init__(self, row: int, column: int, piece=None) -> None:
        self.row = row
        self.column = column
        self.piece = piece
        self.alphacolumn = self.ALPHACOLUMNS[column]

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

    def has_piece(self,) -> bool:
        """Func `has_piece`."""
        return self.piece is not None

    def isempty(self) -> bool:
        return not self.has_piece()

    def has_team_piece(self, color: str):
        return self.has_piece() and self.piece.color == color

    def has_enamy_piece(self, color: str):
        return self.has_piece() and self.piece.color != color

    def isempty_or_enamy(self, color: str):
        return self.isempty() or self.has_enamy_piece(color)

    @staticmethod
    def in_range(*args) -> bool:
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True

    @staticmethod
    def get_alphacolumn(column):
        ALPHACOLUMNS = {
            0: 'a',
            1: 'b',
            2: 'c',
            3: 'd',
            4: 'e',
            5: 'f',
            6: 'g',
            7: 'h'
        }
        return ALPHACOLUMNS[column]
