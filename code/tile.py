"""Sprite Subclass for Tiles (i.e. grass, trees, and rocks)"""
import pygame
from settings import TILESIZE


class Tile(pygame.sprite.Sprite):
    """Stores and manages data for various tile objects (trees, rocks, etc.)"""

    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == 'object':
            # do an offset
            self.rect = self.image.get_rect(
                topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
