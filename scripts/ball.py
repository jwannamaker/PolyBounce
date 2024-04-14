from enum import Enum

import pygame
from pygame import Surface

from movable.player import Player
from asset import Asset
from asset.shape import CIRCLE


class Slingshot(Enum):
    IDLE = 0  # Draw the line between the mouse and the ball in GREY.
    PULL_BACK = 1  # Draw the line between the mouse and the ball in BRIGHT COLOR.
    RELEASE = 2  # DON'T draw the line between the mouse and the ball.

    def draw_vfx(self, screen: Surface) -> None:
        if self.IDLE:
            print('draw line in GREY')
        elif self.PULL_BACK:
            print('draw line BRIGHT')
        else:
            print('DON\'T draw line')


class Ball(Player):
    def __init__(self, game):
        self.game = game
        self.asset = Asset([self.game.all_entities, self.game.player_group],
                           CIRCLE(10),
                           self.game.PALETTE['white'][0],
                           self.game.CENTER)
        super().__init__(self.game, self.asset)
        self.slingshot = Slingshot.IDLE
        self.moving = False

    def toggle_slingshot(self) -> None:
        if self.moving is True:
            return
        if self.slingshot.IDLE:
            self.slingshot = Slingshot.PULL_BACK
        elif self.slingshot.PULL_BACK:
            self.slingshot = Slingshot.RELEASE
        self.slingshot = Slingshot.IDLE

    def update(self, dt: float) -> None:

        self.asset.update()

    def draw(self, screen: Surface) -> None:
        self.asset.draw(self.game.screen)
        if self.moving:
            self.slingshot.draw_vfx(self.game.screen)