from enum import Enum

from asset.shape import Shape, REG_POLY

WALL_THICKNESS = 50


class RING_SIZE(Enum):
    INNER = 100
    MIDDLE = 150
    OUTER = 200


class RingFactory:
    def __init__(self, game, N: int) -> None:
        self.game = game
        self.N = N
        self.base_colors = self.game.get_shuffled_colors(self.N)
        self.colors = self.game.get_gradients(self.base_colors, self.N)

    def create_ring(self, size: str, angular_velocity: float) -> list[pymunk.Shape]:
        outer_radius = RING_SIZE(size).value
        inner_radius = RING_SIZE(size).value - WALL_THICKNESS

        outer_points = REG_POLY(self.N, outer_radius).get_vertices()
        inner_points = REG_POLY(self.N, inner_radius).get_vertices()

        # Splitting and regrouping vertices into (inner_start, OUTER_start, OUTER_END, inner_END)
        for i in range(self.N):
            # self.base_colors[i]
            pass
