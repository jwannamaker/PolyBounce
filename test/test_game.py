import random
import json

import pytest
import pygame
from pygame import Surface, Color

from game import Game
from physics import PhysicsEngine
from asset import Asset, REG_POLY, CIRCLE
from movable import Player



class TestGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
        self.SCREEN_SIZE = self.screen.get_size()
        self.CENTER = self.SCREEN_SIZE[0] // 2, self.SCREEN_SIZE[1] // 2
        self.PALETTE = self.grab_palette('../data/palette.json')
        self.background = Surface(self.screen.get_size())
        self.background.fill(self.PALETTE['black'][0])

        self.clock = pygame.Clock()
        self.fps = 60
        self.running = False
        self.frame_start = 0.0
        self.dt = 0.0

        self.all_entities = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

    def grab_palette(self, json_filename: str) -> dict[str, Color]:
        palette = {}
        with open(json_filename, 'r') as palette_file:
            palette = json.load(palette_file)
        for key in palette.keys():
            palette[key] = [Color(value) for value in palette[key]]
        return palette

    def get_shuffled_colors(self, N: int) -> list[Color]:
        colors = list(self.PALETTE.keys())
        colors.remove('white')
        colors.remove('black')
        random.shuffle(colors)

        return random.sample(colors, N)

    def get_gradients(self, N: int, color: str) -> list[Color]:
        return [Color(self.PALETTE[color][i]) for i in range(N)]

    def start(self) -> None:
        self.running = True
        self.main_loop()

    def main_loop(self) -> None:
        while self.running:
            self.frame_start = pygame.time.get_ticks()
            self.handle_user_input()
            self.process_game_logic()
            self.render()
        pygame.quit()

    def handle_user_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            if event.type == pygame.KEYUP:
                # TODO: Implement the player input
                if event.key == pygame.K_RETURN:
                    print('freeze selected ring + start timer till unfreeze')

    def process_game_logic(self) -> None:
        """ Retrieve the position data from the PhysicsEngine. """
        self.dt = pygame.time.get_ticks() - self.frame_start
        self.all_entities.update(self.dt)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.all_entities.draw(self.screen)

        self.clock.tick_busy_loop(self.fps)
        # PhysicsEngine.step_by(self.dt)
        pygame.display.flip()


@pytest.fixture(scope='session')
def game_instance():
    return TestGame()


def test_palette(game_instance):
    game_instance.grab_palette('../data/palette.json')
    assert type(game_instance.PALETTE) is dict
    assert 'light-blue' in list(game_instance.PALETTE.keys())


def test_palette_value(game_instance):
    assert game_instance.PALETTE['light-blue'][0] == Color(112, 184, 250)


def test_start_game(game_instance):
    game_instance.start()
    assert game_instance.frame_start != 0.0

def test_exit_game(game_instance):
    assert pygame.event.post(pygame.event.Event(pygame.QUIT))
'''
print('palette type: ' + str(type(test_game.ui.PALETTE)))
print('palette keys: ' + str(list(test_game.ui.PALETTE.keys())))
# -------------------------------------------------------------------------------
print('\n')
print(' Testing Game.get_shuffled_colors() '.center(90, '='), '\n')
shuffled_colors = test_game.get_shuffled_colors(3)
print('shuffled_colors: ' + str(shuffled_colors))
# -------------------------------------------------------------------------------
print('\n')
print(' Testing Game.get_gradients() '.center(90, '='), '\n')
test_N = 4
for color in shuffled_colors:
    test_gradients = test_game.get_gradients(color, test_N)
    print(color + ' gradient values: ' + str(test_gradients))
# -------------------------------------------------------------------------------
print('\n')
print(' Testing REG_POLY '.center(90, '='), '\n')
from asset import REG_POLY

test_radius = 10
test_polygon_points = REG_POLY.get_vertices(4, test_radius)
print('REG_POLY.get_vertices(): ' + str(test_polygon_points))
# -------------------------------------------------------------------------------
print('\n')
print(' Testing PhysicsEngine.space '.center(90, '='), '\n')
from physics import PhysicsEngine

print('PhysicsEngine.space memory location: ' + str(PhysicsEngine.space))
print('PhysicsEngine.space memory location: ' + str(PhysicsEngine.space))
print('PhysicsEngine.space memory location: ' + str(PhysicsEngine.space))
# -------------------------------------------------------------------------------
print('\n')
print(' Testing PhysicsEngine.create_poly() '.center(90, '='), '\n')
test_position = [10, 10]
test_angular_velocity = 0.5  # radians per second
test_shape = PhysicsEngine.create_poly(center_position=test_position,
                                       points=test_polygon_points,
                                       angular_velocity=test_angular_velocity)
print('test_shape in PhysicsEngine.space: ' + str(test_shape in PhysicsEngine.space.shapes))
print('test_shape memory location: ' + str(test_shape))
# -------------------------------------------------------------------------------
print('\n')
print(' Testing Asset '.center(90, '='), '\n')
import random
from asset import Asset

test_asset = Asset(groups=test_game.player_group,
                   shape=REG_POLY(N=4, radius=1, vertices=test_polygon_points),
                   color=test_gradients[random.randint(0, test_N - 1)],
                   position=test_position)
print('test_asset.width_height: ' + str(test_asset.width_height))
print('test_asset memory location: ' + str(test_asset.__dir__))
# -------------------------------------------------------------------------------
# print('\n')
# print(' Testing PhysicsEngine.notify_observers() '.center(90, '='), '\n')
# from scripts.movable import Player
# test_player = Player(test_game, test_asset)
# PhysicsEngine.add_observer(test_player, test_shape)
# PhysicsEngine.notify_observers('testing_event', 'This is data passed as a notification')
# -------------------------------------------------------------------------------
# print('\n')
# from scripts.movable import Player
# print(' Testing Movable(Asset) '.center(90, '='), '\n')
# test_movable = Player(test_game, test_asset)
# PhysicsEngine.add_observer(test_movable, test_shape)
# PhysicsEngine.step_by(0.1)
# print('test_shape.position: ' + test_shape.position)
# -------------------------------------------------------------------------------
print('\n')
print(' Testing PhysicsEngine.start_simulation()')
test_game.screen.fill((0, 0, 0))
PhysicsEngine.start_simulation(test_game.screen)
# -------------------------------------------------------------------------------
print('\n')
print(' Testing Player(Movable) '.center(90, '='), '\n')

# -------------------------------------------------------------------------------
'''
