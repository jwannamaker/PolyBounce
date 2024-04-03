from scripts.ui import *
from polygon import Polygon
from ball import Ball

class Level:
    def __init__(self, game):
        self.game = game
        """ Game has a player_group, an enemy_group, and a ui_group"""
        