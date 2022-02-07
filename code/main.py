"""Entrypoint for zelda-style-rpg"""
import sys
import pygame
# pylint: disable=unused-wildcard-import,wildcard-import
from settings import *
from level import Level
# pylint: disable=unused-import
from debug import debug


class Game:
    """Main Game Class"""

    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        """Runs the game"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
