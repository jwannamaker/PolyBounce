'''
    _summary_: Utility function module for the hexkeys project.
'''

import os, random, pygame, pymunk, pymunk.pygame_util
import numpy as np
from collections import deque
from typing import NamedTuple
from pygame import Vector2, gfxdraw

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
DATA_DIR = os.path.join(MAIN_DIR, 'data')

SCREEN_SIZE = Vector2(1280, 720)
CENTER = Vector2(SCREEN_SIZE // 2)

class COLOR(NamedTuple):
    value: tuple
    collision_type: int

PALLETE_DICT = {
    'blue': COLOR((150, 170, 200), 1),
    'cyan': COLOR((144, 239, 240), 2),
    'drk-purple': COLOR((63, 45, 112), 3),
    'lt-blue': COLOR((170, 224, 241), 4),
    'lt-purple': COLOR((150, 100, 187), 5),
    'magenta': COLOR((129, 55, 113), 6),
    'mid-blue': COLOR((83, 91, 113), 7),
    'pink': COLOR((201, 93, 177), 8),
    'red': COLOR((255, 100, 100), 9),
    'white': COLOR((250, 250, 250), 10)
}
PALLETE = list(PALLETE_DICT.keys())

def load_font():
    font_file = os.path.join(DATA_DIR, 'Emulogic-zrEw.ttf')
    return pygame.font.Font(font_file, 12)

def create_walls(corners, space: pymunk.Space):
    for i in range(len(corners)):
        j = (i + 1) % len(corners)
        segment = pymunk.Segment(space.static_body, corners[i], corners[j], 3)
        segment.set_neighbors(corners[i], corners[j])  # neighbor present at both endpoints of this segment
        segment.density = 100
        segment.elasticity = 0.999
        segment.friction = 0.7
        space.add(segment)
                                                                       
def attach_segments(vertices, body: pymunk.Body, space: pymunk.Space):
    '''
        Returns the line segments connecting all the passed vertices together,
        adding to the specified body and making all segments neighbors.
        
        Effectively creates a polygon for pymunk purposes.
    '''
    segment_list = []
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
        segment.collision_type = 2 # TODO change to the appropriate type for a color or a category or something more sophisticated than hard coded for chrissake
        segment_list.append(segment)
    # space.add(*segment_list)
    return segment_list

def get_shuffled_colors(N):
    ''' Shuffles the colors and returns N of them without repeats. '''
    global PALLETE
    random.shuffle(PALLETE)
    return random.sample(PALLETE, N)

def rotate_about_center(surface: pygame.Surface, image, angle):
    '''
    Rotates the image, displays onto the surface. Pivots around the center
    '''
    new_rect = pygame.transform.rotate(image, angle).get_rect()
    # new_rect.center = 
    
def begin(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
    print('Collision began this step')
    print('Must get from pygame mask collision now what the colors are')
    print('Then populate the data dict with that collision information')
    collision_color = data['inner_ring'].get_color_at(arbiter.contact_point_set)
    data['ball'] = 'ball obj placeholder'
    data['side'] = 'side obj placeholder'

def pre_solve(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
    print('Collision success')

def post_solve(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
    print('Collision stuff')
    
def separate(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
    print('Separation success')