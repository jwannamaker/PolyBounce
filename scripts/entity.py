from abc import ABC, abstractmethod

import pygame
from pygame import Vector2, Rect, mask, Surface

class Asset(pygame.sprite.Sprite):
    def __init__(self, groups, shape: str, color_key: str):
        super().__init__(groups)
        self.color_key = color_key
        self.init_sprite()
        
    def create_circle_image(self, radius, color):
        pass
        
    def create_poly_image(self):
        pass    
    
    def set_image(self, picture):
        self.image = Surface((self.radius * 2, self.radius * 2))
    
    def init_sprite(self):
        self.draw(self.image)
        self.image.set_colorkey(self.ui.PALETTE['black'])
        self.rect.topleft = (self.ui.CENTER.x - self.radius, 
                             self.ui.CENTER.y - self.radius)
    
    def create_mask(self):
        self.rect = Rect(self.image.get_rect())
        self.mask = mask.from_surface(self.image)

class Movable(ABC):
    def __init__(self, position):
        self.position = position
    
    @abstractmethod
    def draw(self, screen):
        pass    
    
    @abstractmethod
    def update(self):
        """ The position is changing every time, this method needs to do 
        something everytime it gets called.
        """
        pass
        
class Fixed(ABC):
    @abstractmethod
    def check_change(self):
        pass
    
    @abstractmethod
    def draw(self):
        pass
    
    @abstractmethod
    def update(self):
        """ This method needs to call check_change() if there are any changes before 
        calling draw().
        """
        pass
    
class Entity:
    """ Entity is the Abstract class for every game object. """
    def __init__(self, behavior: Fixed | Movable, asset_type: str):
        self.behavior = behavior
    
    def update(self):
        # TODO: call the abstract class's methods for behavior
        pass
    
    def draw(self):
        # TODO: the image should be taken care of elsewhere
        pass

                
class Player(Movable, Entity):
    def __init__(self):
        super().__init__()
        
    def calculate_score(self):
        """ Calculate the score based on the current number of hits times the
        level the hits happened on.
        """
        pass
    
    def current_level(self):
        """ Return the current level this player is on in the game. """
        pass
    
    def level_up(self):
        """ Increase the mass or something. Making it easier to break through 
        blocks.
        """
        pass

class Enemy(Movable, Entity):
    def __init__(self):
        pass

class Observed(ABC):
    @abstractmethod
    def add_observer(self, observer):
        pass
    
    @abstractmethod
    def remove_observer(self, observer):
        pass
    
    @abstractmethod
    def notify_observers(self):
        pass

class Observer(ABC):
    @abstractmethod
    def set_observed(self, observed):
        pass