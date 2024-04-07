import copy
from typing import NamedTuple, Optional
from abc import ABC, abstractmethod

import pygame
from pygame import Rect, mask, Surface, Color

class Asset(pygame.sprite.Sprite):
    """ An Asset handles ONLY the visual aspect of a game object. """
    class CIRCLE(NamedTuple):
        radius: float
        
        def get_center(self) -> tuple[float, float]:
            return (self.radius, self.radius)
    
    class POLY(NamedTuple):
        width: float
        height: float
        vertices: list[tuple[float, float]]
    
    class BOX(NamedTuple):
        width: float
        height: float
        
        def get_corners(self) -> list[tuple[float, float]]:
            return [(0, 0), 
                    (0, self.height), 
                    (self.width, self.height),
                    (self.width, 0)]
    
    def __init__(self, other):
        if isinstance(other, Asset):
            self = copy.deepcopy(other)
    
    def __init__(self, 
                 shape: CIRCLE | POLY | BOX, 
                 color: Color,
                 base_image: Optional[Surface] = None):
        self.shape = shape
        self.color = color
        self.base_image = base_image
        
        if isinstance(self.shape, Asset.CIRCLE):
            self.create_circle_image()
        elif isinstance(self.shape, Asset.POLY):
            self.create_poly_image()
        elif isinstance(self.shape, Asset.BOX):
            self.create_box_image()
            
        self.rect = Rect(self.image.get_rect())
        self.mask = mask.from_surface(self.image)
    
    def create_circle_image(self):
        if self.base_image == None:
            self.base_image = Surface((self.shape.radius*2, self.shape.radius*2))
        self.image = pygame.draw.circle(self.base_image, 
                                        self.color, 
                                        self.shape.get_center(), 
                                        self.shape.radius)
    
    def create_poly_image(self):
        if self.base_image == None:
            self.base_image = Surface((self.shape.width, self.shape.height))
        self.image = pygame.draw.polygon(self.base_image,
                                         self.color,
                                         self.shape.vertices,
                                         width=0)
    
    def create_box_image(self):
        if self.base_image == None:
            self.base_image = Surface((self.shape.width, self.shape.height))
        self.image = pygame.draw.rect(self.base_image,
                                      self.color,
                                      ((0, 0), (self.shape.width, self.shape.height)),
                                      border_radius=5)

    @abstractmethod
    def draw(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
class Movable(Asset, ABC):
    def __init__(self, asset: Asset, start_position: list[float, float]):
        super().__init__(asset)
        self.position = start_position
    
    @abstractmethod
    def draw(self, screen):
        # TODO: Use Pygame and draw the asset at the correct position.
        pass    
    
    @abstractmethod
    def update(self):
        """ The position of this object is expected to change every frame. This
        method needs to do something every time it gets called.
        """
        self.position = self.rect.topleft
        # TODO: Any other logic an Entity needs to take care of during update.

class FixedPosition(Asset, ABC):
    def __init__(self, asset: Asset, screen_position: list[float, float]):
        super().__init__(asset)
        self.screen_position = screen_position
    
    @abstractmethod
    def draw(self, screen):
        """ This method will ONLY change the data (text) displayed on this 
        Entity. It will be drawn in the same position every time.
        """
        pass
    
    @abstractmethod
    def update(self):
        """ This method needs to call check_change() if there are any changes 
        before calling draw().
        """
        pass

class EventHandler(NamedTuple):
    asset: Asset
    event_func: callable
    
    def run_event(self):
        self.asset.event_func()
    
class EventManager(ABC):
    def __init__(self):
        self.observers: dict[str, set[EventHandler]] = {}
    
    def attach_observer(self, event_type: str, handler: EventHandler):
        self.observers[event_type] = handler
    
    def detach_observer(self, event_type: str, handler: EventHandler):
        # TODO: More error checking needed--specifically the case where a
        if event_type in self.observers:
            self.observers[event_type].remove(handler)
        
    def notify_observers(self, event_type):
        if event_type in self.observers:
            for handler in self.observers[event_type].value():
                handler.run_event()