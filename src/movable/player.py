import pymunk
import pygame
from pygame import Surface

from movable import Movable


class Player(Movable):
    def __init__(self, asset: pygame.sprite.Sprite):
        self.asset = asset
        self.level_score = 0
        self.total_score = 0

    def update(self, dt: float) -> None:
        pass

    def test_notified(self, data) -> None:
        pass

    def notified(self, shape: pymunk.Shape):
        pass

    def save_and_clear_score(self):
        # TODO: save the score in a json for highscores
        self.total_score += self.level_score
        self.level_score = 0

    def get_score(self):
        """ Calculate the score base_imaged on the current number of hits times the
        level the hits happened on.
        """
        return self.level_score

    def current_level(self):
        """ Return the current level this player is on in the game. """
        pass

    def level_up(self):
        """ Increase the mass or something. Making it easier to break through
        blocks.
        """
        pass
