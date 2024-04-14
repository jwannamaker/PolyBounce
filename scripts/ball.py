import pygame

from movable.player import Player
from asset.asset import Asset
from asset.shape import CIRCLE


class Ball(Player):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.asset = Asset([self.game.all_entities, self.game.player_group],
                           CIRCLE(10),
                           self.game.PALETTE['white'][0],
                           self.game.CENTER)
