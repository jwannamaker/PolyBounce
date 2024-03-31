'''
    _summary_: Utility function module for the hexkeys project.
'''

import random, pygame, pymunk, pymunk.pygame_util
from pygame import gfxdraw
from collections import deque
from typing import NamedTuple
from pygame import Vector2

IMG_DIR = 'data/images/'
FONT_DIR = 'data/fonts/'

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
    font_file = FONT_DIR + 'Emulogic-zrEw.ttf'
    return pygame.font.Font(font_file, 12)

def load_image(name):
    image = pygame.image.load(IMG_DIR + name).convert()
    image.set_colorkey((0, 0, 0))
    return image

def get_color(color_str):
    return pygame.Color(PALLETE_DICT[color_str].value)

def get_collision_type(color_str):
    return PALLETE_DICT[color_str].collision_type

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
        
        Effectively creates a non-filled polygon from line segments for pymunk.
    '''
    segment_list = []
    space.add(body)
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
        segment.collision_type = 2  # not ball
        segment_list.append(segment)
    space.add(*segment_list)
    # return segment_list

def get_shuffled_colors(N):
    ''' Shuffles the colors and returns N of them without repeats. '''
    random.shuffle(PALLETE)
    return random.sample(PALLETE, N)
    
def rotate_about_center(surface: pygame.Surface, image, angle):
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
    print('pre_solve')

def post_solve(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
    print('post_solve')
    
def separate(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict):
    print('separate')