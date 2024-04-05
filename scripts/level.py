from game import Game

class Level:
    def __init__(self, game: Game, level_number: int, difficulty: dict):
        self.game = game
        self.level_number = level_number
        self.difficulty = difficulty
        self.enemies_spawned = 0

    def start(self):
        self.update_ui()
        self.spawn_enemies()

    def update_ui(self):
        """ Update UI elements based on current level state. """
        self.game.ui.update_level_display(self.level_number)
        self.game.ui.update_score_display(self.game.player.score)

    def spawn_enemies(self):
        """ Spawn enemies based on current level's difficulty. """
        for _ in range(self.difficulty['enemy_count']):
            enemy = self.game.spawn_enemy(self.difficulty['enemy_params'])
            self.game.enemy_group.add(enemy)
            self.enemies_spawned += 1

    def reset_player_position(self):
        """ Reset player position to starting position. """
        self.game.player.position = self.difficulty['player_start_position']

    def increase_difficulty(self):
        """Increase difficulty for the next level"""
        self.level_number += 1
        self.difficulty = self.calculate_next_difficulty()
        self.enemies_spawned = 0

    def calculate_next_difficulty(self):
        """Calculate difficulty parameters for the next level"""
        # Example: increase enemy count and spawn rate for the next level
        next_difficulty = {
            'enemy_count': self.difficulty['enemy_count'] + 1,
            'enemy_params': self.difficulty['enemy_params'],
            'player_start_position': self.difficulty['player_start_position']
        }
        return next_difficulty
