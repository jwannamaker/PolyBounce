from polybounce import *
from scripts.entity import *
from scripts.physics import PhysicsEngine

print()
print('-------------------- Testing Game.grab_palette() --------------------')
test_game = Game()
test_game.grab_palette('data/palette.json')
print('palette type: ' + str(type(test_game.ui.PALETTE)))
print('palette keys: ' + str(list(test_game.ui.PALETTE.keys())))

print()
print('-------------------- Testing Game.get_shuffled_colors() --------------------')
shuffled_colors = test_game.get_shuffled_colors(3)
print('shuffled_colors: ' + str(shuffled_colors))

print()
print('-------------------- Testing Game.get_gradients() --------------------')
for color in shuffled_colors:
    test_gradients = test_game.get_gradients(color, 6)
    print(color + ' gradient values: ' + str(test_gradients))

print()
print('-------------------- Testing RegularPolygon --------------------')
test_N = 4
test_radius = 1
test_polygon_points = REG_POLY.get_vertices(N=test_N, radius=test_radius)
print('REG_POLY points: ' + str(test_polygon_points))

print()
print('-------------------- Testing PhyscisEngine.space --------------------')
print('PhysicsEngine.space memory location: ' + str(PhysicsEngine.space))
print('PhysicsEngine.space memory location: ' + str(PhysicsEngine.space))
print('PhysicsEngine.space memory location: ' + str(PhysicsEngine.space))

print()
print('-------------------- Testing PhysicsEngine.create_poly() --------------------')
test_position = [1, 1]
test_angular_velocity = 0.5 # radians per second
test_shape = PhysicsEngine.create_poly(center_position=test_position, 
                                       points=test_polygon_points, 
                                       angular_velocity=test_angular_velocity)
print('test_shape in PhysicsEngine.space: ' + str(test_shape in PhysicsEngine.space.shapes))
print('test_shape memory location: ' + str(test_shape))

print()
print('-------------------- Testing Asset --------------------')
test_asset = Asset(groups=test_game.player_group, 
                   shape=REG_POLY(N=4, radius=1, vertices=test_polygon_points), 
                   color=test_gradients[random.randint(0, 5)],
                   position=test_position)
print('test_asset.width_height: ' + str(test_asset.width_height))
print('test_asset memory location: ' + str(test_asset.__dir__))

print()
print('-------------------- Testing PhysicsEngine.notify_observers() --------------------')
test_player = Player(test_game, test_asset)
PhysicsEngine.add_observer(test_player, test_shape)
PhysicsEngine.notify_observers('testing_event', 'This is data passed as a notification')

print()
