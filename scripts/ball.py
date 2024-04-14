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
    def __init__(self, game):
        self.game = game
        self.asset = Asset([self.game.all_entities, self.game.player_group],
                           CIRCLE(10),
                           self.game.PALETTE['white'][0],
                           self.game.CENTER)
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

    def toggle_slingshot(self) -> None:
        if self.moving is True:
            return
        if self.slingshot == Slingshot.IDLE:
            self.slingshot = Slingshot.PULL_BACK
        elif self.slingshot == Slingshot.PULL_BACK:
            self.slingshot = Slingshot.RELEASE
        else:
            self.slingshot = Slingshot.IDLE

    def draw_slingshot(self, screen: Surface) -> None:
        self.slingshot_image = Surface(self.game.screen.get_size())
        self.slingshot_image.set_colorkey([0, 0, 0])
        if self.slingshot is Slingshot.IDLE:
            self.slingshot_rect = pygame.draw.line(self.slingshot_image,
                                                   self.game.PALETTE['black'][5],
                                                   pygame.mouse.get_pos(),
                                                   self.asset.rect.center,
                                                   round(self.asset.shape.get_width()))
        elif self.slingshot is Slingshot.PULL_BACK:
            self.slingshot_rect = pygame.draw.line(self.slingshot_image,
                                                   self.game.PALETTE['red'][0],
                                                   pygame.mouse.get_pos(),
                                                   self.asset.rect.center,
                                                   round(self.asset.shape.get_width()))
        self.slingshot_rect = self.slingshot_image.get_frect()
        # self.slingshot_rect = self.slingshot_image.get_bounding_rect()
        screen.blit(self.slingshot_image, self.slingshot_rect)

    def toggle_moving(self) -> None:
        self.moving = False if self.moving else True
        if self.moving:
            print('STOP the ball')
        else:
            print('START the ball')

    def update(self, dt: float) -> None:
        self.asset.update(dt)
        if self.moving:
            print('ball moving')
        else:
            print('ball not moving')

    def draw(self, screen: Surface) -> None:
        # Has to be manually called for some reason
        self.draw_slingshot(self.game.screen)
        self.asset.draw(self.game.screen)
