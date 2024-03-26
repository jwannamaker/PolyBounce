'''
    _summary_: Utility function module for the hexkeys project.
'''

import os, random, pygame, pymunk, pymunk.pygame_util
import numpy as np
from collections import deque
from pygame import Vector2, gfxdraw

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
DATA_DIR = os.path.join(MAIN_DIR, 'data')

SCREEN_SIZE = Vector2(1280, 720)
CENTER = Vector2(SCREEN_SIZE // 2)

# every color corresponds to a collision type
POLY_PALLETE = {
    (250, 250, 250): 1, # white
    (201, 93, 177): 2,  # pink
    (150, 100, 187): 3, # light-purple
    (150, 170, 200): 4, # blue
    (144, 239, 240): 5, # cyan
    (255, 100, 100): 6, # red
    (170, 224, 241): 7  # light-blue
}
BACKGROUND_PALLETE = {
    'black': (10, 10, 10),
    'magenta': (129, 55, 113),
    'dark-purple': (63, 45, 112),
    'grey-blue': (83, 91, 113)
}

def load_font():
    font_file = os.path.join(DATA_DIR, 'Emulogic-zrEw.ttf')
    return pygame.font.Font(font_file, 12)

def create_walls(corners, space: pymunk.Space):
    '''
        uses the static body that is included in every pymunk space
    '''                                                            
    for i in range(len(corners)):
        j = i + 1 if i < len(corners) - 1 else 0
        point_a = corners[i][0], corners[i][1]
        point_b = corners[j][0], corners[j][1]
        segment = pymunk.Segment(space.static_body, point_a, point_b, 3)
        
        # neighbor present at both endpoints of this segment
        segment.set_neighbors(point_a, point_b) 
        segment.density = 100
        segment.elasticity = 1
        segment.friction = 0.7
                                                                       
def attach_segments(vertices, body: pymunk.Body, space: pymunk.Space):
    '''
        Returns the line segments connecting all the passed vertices together,
        adding to the specified body and making all segments neighbors.
        
        Effectively creates a polygon for pymunk purposes.
    '''
    for i in range(len(vertices)):
        j = i + 1 if i < len(vertices) - 1 else 0
        point_a = vertices[i][0], vertices[i][1]
        point_b = vertices[j][0], vertices[j][1]
        segment = pymunk.Segment(body, point_a, point_b, 3)
        
        # neighbor present at both endpoints of this segment
        segment.set_neighbors(point_a, point_b) 
        segment.density = 100
        segment.elasticity = 1
        segment.friction = 0.7
        space.add(segment)
    # return segment_list