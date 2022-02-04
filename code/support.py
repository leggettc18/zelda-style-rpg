"""Contains various helper functions for use in other game files."""
from csv import reader
from os import walk
import pygame


def import_csv_layout(path):
    """Reads CSV files into a dictionary"""
    terrain_map = []
    with open(path, encoding="utf-8") as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    """Imports all image files in a folder."""
    surface_list = []
    for _, __, img_files in walk(path):
        for image in sorted(img_files, key=lambda image: image):
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list
