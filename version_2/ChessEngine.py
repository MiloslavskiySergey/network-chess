"""
This class is responsible for storing all the information about the current state of a chess game. # noqa
It will also be responsible for dermining the valid moves at the current state. It will also keep a move log.
"""


class GameState():
    """Game state."""

    def __init__(self):
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
        self.white_to_move = True
        self.move_log = []
