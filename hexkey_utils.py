'''
    _summary: Utility function module for the hexkeys project.
'''

import pygame
from zipfile import ZipFile

def init_font():
    with ZipFile("emulogic-font.zip", "r") as file:
        print("Initializing font from zip file")
        for name in file.namelist():
            if name.endswith(".ttf"):
                file.extract(name)
                return pygame.font.Font(name, 12)