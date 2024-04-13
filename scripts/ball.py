from src.movable import Player
from asset import Asset
from asset.shape import CIRCLE


class Ball(Player):
    def __init__(self, game):
        self.game = game
        self.asset = Asset([self.game.all_entities, self.game.player_group],
                           CIRCLE(10),
                           self.game.PALETTE['white'],
                           self.game.CENTER)
