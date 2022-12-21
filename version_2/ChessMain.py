"""
This in our main driver file. # noqa
It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
import ChessEngine
from settings import IMAGES_DIR

from os.path import join

WIDTH = HEIGNT = 512
DIMENSION = 8
SQ_SIZE = HEIGNT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images() -> None:
    """Load images."""
    pieces = ['whitePawn', 'whiteRook', 'whiteKnight', 'whiteBishop', 'whiteKing', 'whiteQueen',
              'blackPawn', 'blackRook', 'blackKnight', 'blackBishop', 'blackKing', 'blackQueen']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(join(IMAGES_DIR, 'figures', f'{piece}.png')), (SQ_SIZE, SQ_SIZE))


def main() -> None:
    """Point run."""
    p.init()
    p.display.set_caption('Game chess')
    p.display.set_icon(p.image.load(join(IMAGES_DIR, 'iconChess.png')))
    screen = p.display.set_mode((WIDTH, HEIGNT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False
    load_images()
    running = True
    sq_selected = ()
    player_clicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                column = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, column):
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, column)
                    player_clicks.append(sq_selected)
                if len(player_clicks) == 2:
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                        sq_selected = ()
                        player_clicks = []
                    else:
                        player_clicks = [sq_selected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    move_made = True
        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False
        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_game_state(screen, gs) -> None:
    """Responsible for all the graphics within a current game state."""
    draw_board(screen)
    draw_pieces(screen, gs.board)


def draw_board(screen) -> None:
    """Draw the squares on the board."""
    colors = [p.Color('white'), p.Color('gray')]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board) -> None:
    """Draw the pieces on the board using the current GameState.board."""
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
