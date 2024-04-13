from pygame import Surface, Font

import pymunk
from abc import abstractmethod

from asset import Asset

class FixedPosition(Asset):
    @abstractmethod
    def draw(self, surface: Surface) -> None:
        """ This method will ONLY change the data displayed on this Entity. It 
        will be drawn in the same position every time.
        """
        surface.blit(self.image, self.rect.topleft, self.image.get_size())
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """ This method needs to call check_change() if there are any changes 
        before calling draw().
        """
        # TODO: Implement calling to PhyscicsEngine/Player/Enemy/whatever 
        pass
    
    @abstractmethod
    def test_notified(self, data) -> None:
        print(data)
        
    @abstractmethod
    def notified(self, shape: pymunk.Shape):
        print('shape: ' + str(shape))
        print('Updated points: ' + str(shape.get_vertices()))
    
class TextBox(FixedPosition):
    def __init__(self, asset: Asset, screen_position: tuple[float, float], text: str):
        super().__init__(asset)
        self.text = text
        self.screen_position = screen_position
    
    def draw(self, screen: Surface, font: Font):
        self.image.blit(font.render(self.text, True, self.color), 
                        (15, 15), 
                        (self.rect.width - 15, self.rect.height - 15))
        screen.blit(self.image, 
                    self.screen_position,
                    (self.rect.width, self.rect.height))
   
    def update(self, text):
        if self.text != text:
            self.text = text
            self.draw()