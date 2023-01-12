"""Square file."""


class Square:
    """Clas square."""

    def __init__(self, row: int, column: int, piece=None) -> None:
        self.row = row
        self.column = column
        self.piece = piece

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
