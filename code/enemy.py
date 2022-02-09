"""Module for enemy classes and functions"""
import pygame
from support import import_folder
# pylint:disable=wildcard-import,unused-wildcard-import
from settings import *
from entity import Entity


class Enemy(Entity):
    """Class for managing enemy data"""

    def __init__(self, monster_name, pos, groups, obstacle_sprites):
        # General Setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # Graphics Setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # Movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # Stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        # Player Interaction
        self.can_attack = True
        self.attack_cooldown = 400
        self.attack_time = None

    def import_graphics(self, name):
        """Import graphics for the given monster name"""
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'../graphics/monsters/{name}/'
        for animation in self.animations:
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player):
        """
            Gets the distance and direction between this enemy and the player
            (although technically you could provide any entity to this function
            and it would work just as well).
        """
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        """Sets the enemy status according to the player status"""
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        """Controls which actions the enemy takes based on their status"""
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        """Controls the animations for the enemy instance"""
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def cooldowns(self):
        """Manages enemy cooldowns"""
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

    def update(self):
        """Used to update the enemy instance"""
        self.move(self.speed)
        self.animate()
        self.cooldowns()

    def enemy_update(self, player):
        """Update function for state that requires player state (called from a different
        place in the level code)"""
        self.get_status(player)
        self.actions(player)
