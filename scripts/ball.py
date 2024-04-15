from enum import Enum

import pygame
from pygame import Surface, event

from asset import Asset
from asset.shape import CIRCLE


class Slingshot(Enum):
    IDLE = 0  # Draw the line between the mouse and the ball in GREY.
    PULL_BACK = 1  # Draw the line between the mouse and the ball in BRIGHT COLOR.
    RELEASE = 2  # DON'T draw the line between the mouse and the ball.


class Ball:
    def __init__(self, game, position):
        self.game = game
        self.asset = Asset([self.game.all_entities, self.game.player_group],
                           CIRCLE(10),
                           self.game.PALETTE['white'][0],
                           position)
        self.level_score = 0
        self.total_score = 0
        self.moving = False
        self.freezes = 6

        self.slingshot = Slingshot.IDLE
        self.slingshot_image = Surface(self.game.screen.get_size())
        self.slingshot_image.set_colorkey([0, 0, 0])
        self.slingshot_rect = self.slingshot_image.get_frect()

    def get_freezes(self) -> int:
        return self.freezes

    def get_score(self):
        """ Calculate the score base_imaged on the current number of hits times the
        level the hits happened on.
        """
        return self.level_score

    def current_level(self) -> int:
        """ Return the current level this player is on in the game. """
        return self.total_score // 3

    def level_up(self):
        """ TODO: DECREASE the number of freezes.
        TODO: Increase the mass or something. Make it easier to break through blocks.
        """
        self.total_score += self.level_score
        self.level_score = 0

    def set_slingshot(self, state) -> None:
        self.slingshot = state

        '''
        if self.slingshot == Slingshot.IDLE:
            self.slingshot = Slingshot.PULL_BACK
            print('slingshot IDLE ->' + str(self.slingshot))

        elif self.slingshot == Slingshot.PULL_BACK:
            self.slingshot = Slingshot.RELEASE
            print('slingshot PULL_BACK ->' + str(self.slingshot))

        elif self.slingshot == Slingshot.RELEASE:
            self.slingshot = Slingshot.IDLE
            print('slingshot RELEASE ->' + str(self.slingshot))
        '''

    def draw_slingshot(self, screen: Surface) -> None:
        self.slingshot_image = Surface(self.game.screen.get_size())
        self.slingshot_image.set_colorkey([0, 0, 0])
        if self.slingshot == Slingshot.IDLE:
            self.slingshot_rect = pygame.draw.line(self.slingshot_image, self.game.PALETTE['black'][5], pygame.mouse.get_pos(), self.asset.rect.center, 5)
            self.slingshot_rect = pygame.draw.circle(self.slingshot_image, self.game.PALETTE['black'][2], pygame.mouse.get_pos(), 8)
        elif self.slingshot == Slingshot.PULL_BACK:
            self.slingshot_rect = pygame.draw.line(self.slingshot_image, self.game.PALETTE['red'][0], pygame.mouse.get_pos(), self.asset.rect.center, 5)
            self.slingshot_rect = pygame.draw.circle(self.slingshot_image, self.game.PALETTE['red'][2], pygame.mouse.get_pos(), 8)

        self.slingshot_rect = self.slingshot_image.get_frect()
        screen.blit(self.slingshot_image, self.slingshot_rect)

    def toggle_moving(self) -> None:
        self.moving = False if self.moving else True

    def update(self, position: tuple[float, float]) -> None:
        self.asset.rect.move_ip(position[0] - self.asset.position[0],
                                position[1] - self.asset.position[1])

    def draw(self, screen: Surface) -> None:
        # Has to be manually called for some reason
        self.draw_slingshot(self.game.screen)
        self.asset.draw(self.game.screen)
