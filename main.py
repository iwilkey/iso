import arcade
from renderer import Renderer

def main():
    window = Renderer(800, 600)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
