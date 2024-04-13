from abc import ABC, abstractmethod

import pymunk
from pygame import Surface


class FixedPosition(ABC):
    @abstractmethod
    def draw(self, surface: Surface) -> None:
        """ This method will ONLY change the data displayed on this Entity. It 
        will be drawn in the same position every time.
        """
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass
    
    @abstractmethod
    def test_notified(self, data) -> None:
        print(data)
        pass
        
    @abstractmethod
    def notified(self, shape: pymunk.Shape) -> None:
        pass
