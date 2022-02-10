"""
    Module contains the base entity class that is inherited by game entities (player, enemies, etc.)
"""
from math import sin
import pygame


class Entity(pygame.sprite.Sprite):
    """Base class for game entities (player, enemies, etc."""

    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        """Controls player movement, including normalizing diagonal vectors and checking
        for collisions."""
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # self.rect.center += self.direction * speed
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        """Checks obstacle sprites for a collision in the specified direction."""
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top

    def wave_value(self):
        """
        Returns either 0 or 255 depending on the value of
        a sine wave according to the current time.
        """
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
