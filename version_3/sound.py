"""Sound file."""
import pygame


class Sound:

    def __init__(self, path) -> None:
        self.path = path
        self.sound = pygame.mixer.Sound(path)

    def play(self,) -> None:
        pygame.mixer.Sound.play(self.sound)
