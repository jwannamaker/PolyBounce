from enum import Enum

import pygame
from pygame import Surface
import pymunk

from game import Game
from physics import PhysicsEngine
from asset import Asset, REG_POLY, CIRCLE
from movable import Player

WALL_THICKNESS = 50


class RING_SIZE(Enum):
    INNER = 100
    MIDDLE = 150
    OUTER = 200


class RingFactory:
    def __init__(self, game: Game, N: int) -> None:
        self.game = game
        self.N = N
        self.base_colors = self.game.get_shuffled_colors(self.N)
        self.colors = self.game.get_gradients(self.base_colors, self.N)

    def create_ring(self, size: RING_SIZE, angular_velocity: float) -> list[pymunk.Shape]:
        outer_radius = size
        inner_radius = size - WALL_THICKNESS

        outer_points = REG_POLY(self.N, outer_radius).get_vertices()
        inner_points = REG_POLY(self.N, inner_radius).get_vertices()

        # Splitting and regrouping vertices into (inner_start, OUTER_start, OUTER_END, inner_END)
        for i in self.N:
            self.base_colors[i]


class PolyBounce(Game):
    def __init__(self):
        super().__init__()
        self.grab_palette('../data/palette.json')

        self.fps = 60
        self.frame_start: float = 0.0  # milliseconds
        self.running = False
        self.dt = 0.0
        pygame.init()
        self.screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
        pygame.display.set_caption('PolyBounce')
        pygame.display.toggle_fullscreen()
        self.ui.SCREEN_SIZE = (self.screen.get_size()[0], self.screen.get_size()[1])
        self.ui.CENTER = (self.ui.SCREEN_SIZE[0] // 2, self.ui.SCREEN_SIZE[1] // 2)
        pygame.display.message_box('Welcome to PolyBounce!',
                                   'Your Color Meters are on the right -->\n\
                                    Fill them up by bouncing on the correct color rings!\n\n\
                                    Press [ENTER] to toggle Falling.\n\
                                    Press [ESC] to Quit.')
        self.background = Surface(self.screen.get_size())
        self.background.fill((0, 0, 0))

        self.all_entities = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.player_asset = Asset([self.all_entities, self.player_group],
                                  CIRCLE(radius=10),
                                  self.get_color('white'),
                                  self.ui.CENTER)
        self.player = Player(self, self.player_asset)

    def reset_player(self):
        self.player.level_score = 0

    def handle_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            if event.type == pygame.KEYUP:
                # TODO: Implement the player input 
                if event.key == pygame.K_RETURN:
                    # self.player.stop_moving()
                    pass

    def process_game_logic(self):
        """ Retrieve the position data from the PhysicsEngine. """
        self.all_entities.update(self.dt)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.all_entities.draw(self.screen)

        # TODO: Add some logic here to address the need for semi-fixed framerate?
        # self.clock.tick_busy_loop(self.fps)
        PhysicsEngine.step_by(self.get_dt())
        pygame.display.flip()


if __name__ == "__main__":
    PolyBounce().start()
