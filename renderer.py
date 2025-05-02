import arcade
from cam import Camera
from mesh import Cube
import math

class Renderer(arcade.Window):
	
	def __init__(self, width: int, height: int, title: str = "Isometric Renderer"):
		super().__init__(width, height, title)
		self.camera = Camera(30, 0)
		self.c0 = Cube()
		self.c1 = Cube()
		self.t = 0
  
	def setup(self):
		pass

	def on_update(self, dt: float):
		self.t += dt
		self.c0.iden()
		self.c0.translate(math.sin(self.t), math.sin(self.t), math.cos(self.t))
		self.c0.rotate_y(45 * math.sin(self.t))
  
	def on_draw(self):
		self.clear()
		self.c0.render(self.camera)
