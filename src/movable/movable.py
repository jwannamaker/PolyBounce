from abc import ABC, abstractmethod

import pymunk
from pygame import Surface

from src.asset import Asset


class Movable(ABC):
    @abstractmethod
    def draw(self, surface: Surface) -> None:
        pass
    
    @abstractmethod
    def update(self, dt: float) -> None:
        pass
        
    @abstractmethod
    def test_notified(self, data) -> None:
        print(data)
        
    @abstractmethod
    def notified(self, shape: pymunk.Shape):
        print('shape: ' + str(shape))
        print('Updated points: ' + str(shape.get_vertices()))
