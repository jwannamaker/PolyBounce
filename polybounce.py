import pygame

from game import Game
from scripts.ui import PolyBounceUI
from scripts.ball import Ball
from scripts.polygon import Polygon

class PolyBounce(Game):
    def __init__(self):
        super().__init__(title='PolyBounce', 
                         ui_type=PolyBounceUI, 
                         player_type=Ball, 
                         enemy_type=Polygon)
        
        # Entities setup
        
        
        # Now that all the game objects are created, I can add collision handling for them
        
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.display_stats()
        for entity in self.entities:
            entity.draw(self.ui.screen)
        
        # TODO: Add some logic to address the need for semi-fixed framerate?
        self.clock.tick(self.fps)
        self.space.step(self.dt)
        self.space.debug_draw(self.draw_options)
        pygame.display.flip()
        
if __name__ == "__main__":
    PolyBounce().start()