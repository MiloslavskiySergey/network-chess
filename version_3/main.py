"""Main file."""
import sys
from os.path import join

import pygame
from const import HEIGHT, WIDTH
from game import Game
from settings import IMAGES_DIR


class Main:
    """Class main."""

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Game chess')
        pygame.display.set_icon(pygame.image.load(join(IMAGES_DIR, 'iconChess.png')))
        self.game = Game()

    def mainloop(self) -> None:
        """Call other classes."""
        screen = self.screen
        game = self.game

        while True:
            game.show_bg(screen)
            game.show_pieces(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()


if __name__ == '__main__':
    main = Main()
    main.mainloop()
