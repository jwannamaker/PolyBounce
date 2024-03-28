'''
main.py

Description:
'''
from polybounce.game import PolyBounce

def main():
    game = PolyBounce()
    game.set_fps(50)
    game.start()

if __name__ == '__main__':
    main()