"""Module containing classes and functions that manage the state of the level map and camera."""
from random import choice
import pygame
from enemy import Enemy
# pylint:disable=wildcard-import,unused-wildcard-import
from settings import *
from tile import Tile
from player import Player
from weapon import Weapon
from ui import UI
# pylint:disable=unused-import
from debug import debug
from support import *


class Level:
    """Containts data and functions for managing level state, and sprites"""

    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None

        # sprite setup
        self.create_map()

        # user interface
        # pylint:disable=invalid-name
        self.ui = UI()

    def create_map(self):
        """Imports graphics, creates sprites and adds them to sprite groups,
        and creates the level map."""
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/map_Grass.csv'),
            'object': import_csv_layout('../map/map_Objects.csv'),
            'entities': import_csv_layout('../map/map_Entities.csv')
        }
        graphics = {
            'grass': import_folder('../graphics/grass'),
            'objects': import_folder('../graphics/objects')
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        # pylint:disable=invalid-name
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [
                                self.visible_sprites, self.obstacle_sprites
                            ], 'grass', random_grass_image)
                        if style == 'object':
                            surface = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites,
                                 self.obstacle_sprites], 'object', surface)
                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic
                                )
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites]
                                )

    def create_attack(self):
        """Creates the Weapon Sprite."""
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self):
        """Destroys the current weapon sprite if there is any."""
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic(self, style, strength, cost):
        """Spawns magic spell onto the level"""
        print(style)
        print(strength)
        print(cost)

    def run(self):
        """Draws and updates all the sprites of the game."""
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    """Custom sprite group that sorts sprites by their y coordinate in order for sprite overlaps
    to happen with the correct perspective."""

    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load(
            '../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        """Custom Draw function to handle drawing the sprites offset for the camera position."""
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
