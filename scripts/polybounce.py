import random
import json

import pygame
from pygame import Surface, Color


from fixedposition.borderedbox import BorderedBox


class PolyBounce:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([pygame.display.get_desktop_sizes()[0][0],
                                               pygame.display.get_desktop_sizes()[0][1]])
        self.SCREEN_SIZE = self.screen.get_size()
        self.CENTER = self.SCREEN_SIZE[0] // 2, self.SCREEN_SIZE[1] // 2
        self.PALETTE = self.grab_palette('../data/palette.json')
        self.background = Surface([self.screen.get_size()[0], self.screen.get_size()[1]])
        self.background.fill(self.PALETTE['black'][0])

        self.clock = pygame.Clock()
        self.fps = 60
        self.running = False
        self.frame_start = 0.0
        self.dt = 0.0

        self.all_entities = pygame.sprite.Group()
        self.HUD = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.font = self.load_font('../data/fonts/monogram.ttf')
        self.unit_column = self.screen.get_width() / 8
        self.unit_row = self.screen.get_height() / 9
        self.level_label = None
        self.clock_label = None
        self.score_label = None
        self.load_HUD()

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
        return random.sample([Color(self.PALETTE[color][i]) for i in range(N)], N)

    def load_font(self, font_filename: str, font_size: int = 14):
        pygame.font.init()
        return pygame.font.SysFont('Monaco', 40)

    def load_HUD(self) -> None:
        self.unit_column = self.screen.get_width() // 8
        self.unit_row = self.screen.get_height() // 9
        hud_matrix = {
            'Level': {
                'width': 2,     # multiplied by the unit column width
                'height': 1,    # multiplied by the unit row height
                'border-width': 10,    # in pixels
                'border-radius': 15,    # in pixels
                'position': [1, 0.5],      # center, multiplied by unit column/row
                'font-size': 30,
                'bg-color': self.PALETTE['black'][3],
                'font-color': self.PALETTE['white'][0]
            },
            'Time': {
                'width': 2,     # multiplied by the unit column width
                'height': 1,    # multiplied by the unit row height
                'border-width': 10,   # in pixels
                'border-radius': 15,    # in pixels
                'position': [1, 1.5],      # center, multiplied by unit column/row
                'font-size': 22,
                'bg-color': self.PALETTE['black'][5],
                'font-color': self.PALETTE['white'][0]
            }
        }
        for key in list(hud_matrix.keys()):
            label = BorderedBox(game=self,
                                fixed_text=key,
                                bg_color=hud_matrix[key]['bg-color'],
                                font_color=hud_matrix[key]['font-color'],
                                width=hud_matrix[key]['width'] * self.unit_column,
                                height=hud_matrix[key]['height'] * self.unit_row,
                                border=hud_matrix[key]['border-width'],
                                position=(hud_matrix[key]['position'][0] * self.unit_column,
                                          hud_matrix[key]['position'][1] * self.unit_row))
            label.draw(self.screen)

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
        self.screen.blit(self.background, [0, 0])
        self.all_entities.draw(self.screen)

        self.clock.tick_busy_loop(self.fps)
        # PhysicsEngine.step_by(self.dt)
        pygame.display.flip()


if __name__ == "__main__":
    PolyBounce().start()
