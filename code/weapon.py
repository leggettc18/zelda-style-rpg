"""Sprite subclass for handling weapons"""
import pygame


class Weapon(pygame.sprite.Sprite):
    """Sprite subclass for handling weapons"""

    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        # split status at underscore, we only care about the
        # direction which is index 0 in resulting list.
        direction = player.status.split('_', 1)[0]

        # Graphic
        full_path = f'../graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        # Placement
        if direction == 'right':
            self.rect = self.image.get_rect(
                midleft=player.rect.midright + pygame.math.Vector2(0, 16)
            )
        elif direction == 'left':
            self.rect = self.image.get_rect(
                midright=player.rect.midleft + pygame.math.Vector2(0, 16)
            )
        elif direction == 'down':
            self.rect = self.image.get_rect(
                midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0)
            )
        elif direction == 'up':
            self.rect = self.image.get_rect(
                midbottom=player.rect.midtop + pygame.math.Vector2(-10, 0)
            )
        else:
            self.rect = self.image.get_rect(center=player.rect.center)
