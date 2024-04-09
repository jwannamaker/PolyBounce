import copy
from typing import NamedTuple, Optional
from abc import ABC, abstractmethod

import pygame
from pygame import Rect, mask, Surface, Color

class Asset:
    """ An Asset handles ONLY the visual aspect of a game object. """
    class CIRCLE(NamedTuple):
        radius: int
        
        def get_center(self) -> tuple[int, int]:
            return (self.radius, self.radius)
    
    class POLY(NamedTuple):
        width: int
        height: int
        vertices: list[tuple[int, int]]
    
    class BOX(NamedTuple):
        width: int
        height: int
        
        def get_corners(self) -> list[tuple[int, int]]:
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
                 surface: Optional[Surface] = None):
        self.shape = shape
        self.color = color
        self.surface = surface
        self.left_top = (0, 0)
        self.width_height = (0, 0)
        
        if isinstance(self.shape, Asset.CIRCLE):
            self.image = self.create_circle_image()
        elif isinstance(self.shape, Asset.POLY):
            self.image = self.create_poly_image()
        elif isinstance(self.shape, Asset.BOX):
            self.image = self.create_box_image()
        
        self.rect = self.image.get_rect()
        self.center_offset = self.rect.center
        self.mask = mask.from_surface(self.image)
    
    def create_circle_image(self) -> Surface:
        self.width_height = (self.shape.radius*2, self.shape.radius*2)
        if self.surface == None:
            self.surface = Surface(self.width_height)
            self.image = self.surface.subsurface(self.left_top, self.width_height)
        else:
            self.image = Surface(self.width_height)
        pygame.draw.circle(self.image, 
                           self.color, 
                           self.shape.get_center(), 
                           self.shape.radius)
        return self.image
    
    def create_poly_image(self) -> Surface:
        self.width_height = (self.shape.width, self.shape.height)
        if self.surface == None:
            self.surface = Surface(self.width_height)
            self.image = self.surface.subsurface(self.left_top, self.width_height)
        else:
            self.image = Surface(self.width_height)
        pygame.draw.polygon(self.image, 
                            self.color, 
                            self.shape.vertices, 
                            width=0)
        return self.image
    
    def create_box_image(self) -> Surface:
        self.width_height = (self.shape.width, self.shape.height)
        inner_left_top = (self.left_top[0]+15, self.left_top[1]+15)
        inner_width_height = (self.shape.width-15, self.shape.height-15)
        if self.surface == None:
            self.surface = Surface((self.shape.width, self.shape.height)).set_clip((inner_left_top, inner_width_height))
            self.image = self.surface.subsurface(self.left_top, self.width_height)
        else:
            self.image = Surface(self.width_height)
        pygame.draw.rect(self.image,
                         self.color, 
                         (self.left_top, self.width_height), 
                         border_radius=5)
        return self.image

class Movable(pygame.sprite.Sprite):
    def __init__(self, groups: list[pygame.sprite.Group], asset: Asset, start_position: list[int, int]):
        self.groups = groups
        super().__init__(groups)
        self.asset = asset
        self.image = self.asset.image
        self.rect = self.asset.rect
        self.mask = self.asset.mask
        self.position = start_position
        
    def draw(self, surface: Surface) -> None:
        surface.blit(self.image, self.rect.topleft, self.image.get_size())
    
    def update(self, position: tuple[int, int]) -> None:
        """ The position of this object is expected to change every frame. This
        method needs to do something every time it gets called.
        """
        self.rect.topleft = ((position[0] - self.asset.center_offset[0]), (position[1] - self.asset.center_offset[1]))

class FixedPosition(pygame.sprite.Sprite):
    def __init__(self, groups: list[pygame.sprite.Group], asset: Asset, fixed_position: tuple[int, int]):
        super().__init__(groups)
        self.image = asset.image
        self.rect = asset.rect
        self.mask = asset.mask
        self.fixed_position = fixed_position
    
    def draw(self, surface) -> None:
        """ This method will ONLY change the data displayed on this Entity. It 
        will be drawn in the same position every time.
        """
        surface.blit(self.image, self.fixed_position, self.image.get_size())
    
    def update(self) -> None:
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