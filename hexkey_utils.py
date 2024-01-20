'''
    _summary: Utility function module for the hexkeys project.
'''

import pygame
import numpy as np
from zipfile import ZipFile

def init_font():
    with ZipFile("emulogic-font.zip", "r") as file:
        print("Initializing font from zip file")
        for name in file.namelist():
            if name.endswith(".ttf"):
                file.extract(name)
                return pygame.font.Font(name, 12)

def refresh_background(surface):
    surface.fill("black")

def regular_polygon(surface, center, radius, num_sides):
    vertices = []
    # theta = np.arctan(center.x / center.y)
    delta = (2 * np.pi) / num_sides
    for i in range(num_sides):
        theta = i * delta
        x = (radius * np.cos(theta)) + center.x
        y = (radius * np.sin(theta)) + center.y
        vertices.append(pygame.Vector2(x, y))
    pygame.draw.polygon(surface, "red", vertices)