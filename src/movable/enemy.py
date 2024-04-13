import pygame

from movable import Movable
from asset import Asset


class Enemy(Movable):
    def __init__(self, game: Game, asset: pygame.sprite.Sprite):
        self.game = game
        self.asset = asset
        self.hits_taken = 0
        self.hits_to_die = 1

    def take_hit(self, hit_strength: int = 1) -> bool:
        self.hits_taken += hit_strength
        if self.hits_taken >= self.hits_to_die:
            # TODO: DETACH FROM PHYSICS ENGINE OBSERVERS
            self.asset.kill()


class Side(Movable):
    def __init__(self,
                 game: Game,  # type: ignore
                 asset: Asset):
        super().__init__()