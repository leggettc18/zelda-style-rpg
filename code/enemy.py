"""Module for enemy classes and functions"""
import pygame
from support import import_folder
# pylint:disable=wildcard-import,unused-wildcard-import
from settings import *
from entity import Entity


class Enemy(Entity):
    """Class for managing enemy data"""

    def __init__(self, monster_name, pos, groups):
        # General Setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # Graphics Setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

    def import_graphics(self, name):
        """Import graphics for the given monster name"""
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'../graphics/monsters/{name}/'
        for animation in self.animations:
            self.animations[animation] = import_folder(main_path + animation)
