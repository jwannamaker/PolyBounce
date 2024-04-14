from asset import Asset
from asset.shape import BOX
from borderedbox import BorderedBox

class Label(BorderedBox):
    def __init__(self, game):
        self.asset = BOX()