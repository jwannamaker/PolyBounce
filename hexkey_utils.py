'''
    _summary_: Utility function module for the hexkeys project.
'''

import pygame, os, random
import numpy as np

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
DATA_DIR = os.path.join(MAIN_DIR, "data")

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
CENTER = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

BACKGROUND_PALLETE = {
    "magenta": (129, 55, 113),
    "dark-purple": (63, 45, 112),
    "grey-blue": (83, 91, 113)
}
    
SHAPE_PALLETE = {
    "pink": (201, 93, 177),
    "light-purple": (137, 100, 187),
    "blue": (157, 169, 214),
    "light-blue": (170, 224, 241),
    "cyan": (144, 239, 240)
}

def load_font():
    font_file = os.path.join(DATA_DIR, "Emulogic-zrEw.ttf")
    return pygame.font.Font(font_file, 12)

def load_image(name, colorkey = None, scale = 1):
    fullname = os.path.join(DATA_DIR, name)
    image = pygame.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

def refresh_background(surface):
    surface.fill(BACKGROUND_PALLETE["dark-purple"])
    regular_polygon(surface, CENTER, 100, 6)
    

def regular_polygon(surface, center, radius, num_sides):
    vertices = []
    # theta = np.arctan(center.x / center.y)
    delta = (2 * np.pi) / num_sides
    for i in range(num_sides):
        theta = i * delta
        x = (radius * np.cos(theta)) + center.x
        y = (radius * np.sin(theta)) + center.y
        vertices.append(pygame.Vector2(x, y))
    pygame.draw.aalines(surface, SHAPE_PALLETE["cyan"], True, vertices)
    # pygame.draw.polygon(surface, "red", vertices, 1)
    
def show_stats(surface, font, stats):
    surface.blit(font.render(stats, True, (255, 255, 255)), (0, 0))