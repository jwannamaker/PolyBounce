from abc import abstractmethod

import pymunk
from pygame import Surface

from asset import Asset
from game import Game

class Movable(Asset):
    def __init__(self, groups, shape, color, position, surface):
        super().__init__(groups, shape, color, position, surface)
        
    @abstractmethod
    def draw(self, surface: Surface) -> None:
        surface.blit(self.image, self.rect.topleft, self.width_height)
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """ The position of this object is expected to change every frame. This
        method needs to do something every time it gets called.
        """
        # TODO: Implement calling to PhysicsEngine for the position of the shape
        # TODO: Convert the position from PhysicsEngine to Pygame coordinates, adjust rect.topleft
        self.rect.topleft = ((self.position[0] - self.width_height[0]), 
                             (self.position[1] - self.width_height[1]))
        
    @abstractmethod
    def test_notified(self, data) -> None:
        print(data)
        
    @abstractmethod
    def notified(self, shape: pymunk.Shape):
        print('shape: ' + str(shape))
        print('Updated points: ' + str(shape.get_vertices()))


class Player(Movable):
    def __init__(self, game: Game, asset: Asset): # type: ignore
        self.game = game
        self.groups = [self.game.all_entities, self.game.player_group]
        super().__init__(self.groups, asset.shape, asset.color, asset.position, asset.surface)
        self.level_score = 0
        self.total_score = 0
        
    def save_and_clear_score(self):
        # TODO: save the score in a json for highscores
        self.total_score += self.level_score
        self.level_score = 0
    
    def get_score(self):
        """ Calculate the score base_imaged on the current number of hits times the
        level the hits happened on.
        """
        return self.level_score + Player.total_score
    
    def current_level(self):
        """ Return the current level this player is on in the game. """
        pass
    
    def level_up(self):
        """ Increase the mass or something. Making it easier to break through 
        blocks.
        """
        pass
    
class Enemy(Movable):
    def __init__(self, game: Game, asset: Asset): # type:ignore
        self.groups = [self.game.all_]
        super().__init__(asset)
        self.hits_taken = 0
        self.hits_to_die = 1
        
    def take_hit(self, hit_strength: int = 1) -> bool:
        self.hits_taken += hit_strength
        if self.hits_taken >= self.hits_to_die:
            # TODO: DETACH FROM PHYSICS ENGINE OBSERVERS
            self.kill()

class Side(Movable):
    def __init__(self,
                 game: Game,   # type: ignore
                 asset: Asset):
        super().__init__()