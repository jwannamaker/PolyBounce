from pygame import Rect, Color

from game import Game

class DisplayBox:
    box_type = {
        'current_level': {
            'relative_position': 'top-left',
            'rect': Rect(left_top=(0, 0), width_height=(100, 100))},
        'color_queue': {
            'relative_position': 'left',
            'rect': Rect(left_top=(0, 0), width_height=(100, 100))},
        'high_score': {
            'relative_position': 'top-right',
            'rect': Rect(left_top=(0, 0), width_height=(100, 100))},
        'player_score': {
            'relative_position': 'mid-right', 
            'rect': Rect(left_top=(0, 0), width_height=(100, 100))}
    }
    
    def __init__(self, game, box_type):
        """ Gets the pygame.Rect values from the display_type dict. Makes a 
        subsurface from the game's screen.
        
        Needs to be added to the game's list of updatable objects.
        """
        self.game = game
        self.surface = self.game.screen.subsurface(DisplayBox.type[box_type])
        
    def set_stats(self, fields_text_dict):
        player_info = []
        player_info.append('{:15s} {:5f}'.format('HIGH SCORE', 0))
        player_info.append('{:15s} {:5f}'.format('SCORE', 0))
        # TODO Make some fancy display rect for the text to go onto and then blit that onto the screen
        
        for i, line in enumerate(player_info):
            self.game.screen.blit(self.game.ui.font.render(line, True, Color('white')), 
                                  (self.game.ui().SCREEN_SIZE.x / 2, 20 * i))