"""Manges the state of our UI"""
import pygame
# pylint:disable=unused-wildcard-import,wildcard-import
from settings import *


class UI:
    """Class for manaing the game UI (weapon selected, health bar, etc.)"""

    def __init__(self):
        # General
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Bars
        self.health_bar_rect = pygame.Rect(
            10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT
        )
        self.energy_bar_rect = pygame.Rect(
            10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT
        )

        # Convert Weapon Dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

    def show_bar(self, current_amount, max_amount, bg_rect, color):
        """Draws various ui bars to the screen flexibly"""
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stats to pixels
        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(
            self.display_surface,
            UI_BORDER_COLOR, bg_rect, 3
        )

    def show_exp(self, exp):
        """Displays the experience amount on the display"""
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        # pylint:disable=invalid-name
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))
        pygame.draw.rect(
            self.display_surface, UI_BG_COLOR,
            text_rect.inflate(20, 20)
        )
        pygame.draw.rect(
            self.display_surface,
            UI_BORDER_COLOR, text_rect.inflate(20, 20), 3
        )
        self.display_surface.blit(text_surf, text_rect)

    def selection_box(self, left, top, has_switched):
        """Draws a selection box"""
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface,
                             UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        """Draws the selected weapon on the screen"""
        bg_rect = self.selection_box(10, 630, has_switched)  # weapon
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)

    def display(self, player):
        """Displays/updates UI elements"""
        self.show_bar(
            player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR
        )
        self.show_bar(
            player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR
        )
        self.show_exp(player.exp)
        self.weapon_overlay(
            player.weapon_index,
            not player.can_switch_weapon
        )
        self.selection_box(80, 635, False)  # magic
