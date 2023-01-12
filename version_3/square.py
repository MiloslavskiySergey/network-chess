"""Square file."""


class Square:
    """Clas square."""

    def __init__(self, row: int, column: int, piece=None) -> None:
        self.row = row
        self.column = column
        self.piece = piece

    def has_piece(self,) -> bool:
        """Func `has_piece`."""
        return self.piece is not None
