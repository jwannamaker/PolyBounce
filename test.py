print('\n')
print(' Testing Game.grab_palette() '.center(90, '='), '\n')
from scripts.game import Game
test_game = Game()
test_game.grab_palette('data/palette.json')
print('palette type: ' + str(type(test_game.ui.PALETTE)))
print('palette keys: ' + str(list(test_game.ui.PALETTE.keys())))
#-------------------------------------------------------------------------------
print('\n')
print(' Testing Game.get_shuffled_colors() '.center(90, '='), '\n')
shuffled_colors = test_game.get_shuffled_colors(3)
print('shuffled_colors: ' + str(shuffled_colors))
#-------------------------------------------------------------------------------
print('\n')
print(' Testing Game.get_gradients() '.center(90, '='), '\n')
test_N = 4
for color in shuffled_colors:
    test_gradients = test_game.get_gradients(color, test_N)
    print(color + ' gradient values: ' + str(test_gradients))
#-------------------------------------------------------------------------------
print('\n')
print(' Testing REG_POLY '.center(90, '='), '\n')
from scripts.asset import REG_POLY
test_radius = 10
test_polygon_points = REG_POLY.get_vertices(N=test_N, radius=test_radius)
print('REG_POLY.get_vertices(): ' + str(test_polygon_points))
#-------------------------------------------------------------------------------
print('\n')
print(' Testing PhyscisEngine.space '.center(90, '='), '\n')
from scripts.physics import PhysicsEngine
print('PhysicsEngine.space memory location: ' + str(PhysicsEngine.space))
print('PhysicsEngine.space memory location: ' + str(PhysicsEngine.space))
print('PhysicsEngine.space memory location: ' + str(PhysicsEngine.space))
#-------------------------------------------------------------------------------
print('\n')
print(' Testing PhysicsEngine.create_poly() '.center(90, '='), '\n')
test_position = [10, 10]
test_angular_velocity = 0.5 # radians per second
test_shape = PhysicsEngine.create_poly(center_position=test_position, 
                                       points=test_polygon_points, 
                                       angular_velocity=test_angular_velocity)
print('test_shape in PhysicsEngine.space: ' + str(test_shape in PhysicsEngine.space.shapes))
print('test_shape memory location: ' + str(test_shape))
#-------------------------------------------------------------------------------
print('\n')
print(' Testing Asset '.center(90, '='), '\n')
import random
from scripts.asset import Asset
test_asset = Asset(groups=test_game.player_group, 
                   shape=REG_POLY(N=4, radius=1, vertices=test_polygon_points), 
                   color=test_gradients[random.randint(0, test_N - 1)],
                   position=test_position)
print('test_asset.width_height: ' + str(test_asset.width_height))
print('test_asset memory location: ' + str(test_asset.__dir__))
#-------------------------------------------------------------------------------
# print('\n')
# print(' Testing PhysicsEngine.notify_observers() '.center(90, '='), '\n')
# from scripts.movable import Player
# test_player = Player(test_game, test_asset)
# PhysicsEngine.add_observer(test_player, test_shape)
# PhysicsEngine.notify_observers('testing_event', 'This is data passed as a notification')
#-------------------------------------------------------------------------------
# print('\n')
# from scripts.movable import Player
# print(' Testing Movable(Asset) '.center(90, '='), '\n')
# test_movable = Player(test_game, test_asset)
# PhysicsEngine.add_observer(test_movable, test_shape)
# PhysicsEngine.step_by(0.1)
# print('test_shape.position: ' + test_shape.position)
#-------------------------------------------------------------------------------
print('\n')
print(' Testing PhysicsEngine.start_simulation()')
test_game.screen.fill((0, 0, 0))
PhysicsEngine.start_simulation(test_game.screen)
#-------------------------------------------------------------------------------
print('\n')
print(' Testing Player(Movable) '.center(90, '='), '\n')

#-------------------------------------------------------------------------------