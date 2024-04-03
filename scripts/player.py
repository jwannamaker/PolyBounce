from scripts.entity import Entity

class Player(Entity):
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