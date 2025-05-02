import math
from typing import List
from vec import Vec3

class Mat4:

	def __init__(self, m : List[float] = None, **kwargs):
		# row-major iden init..
		if m is None:
			self.m = [
				1, 0, 0, 0,
				0, 1, 0 ,0,
				0, 0, 1, 0,
				0, 0, 0, 1
			]
		else:
			assert len(m) == 16
			self.m = m

	def iden(self):
		self.m = [
			1, 0, 0, 0,
			0, 1, 0 ,0,
			0, 0, 1, 0,
			0, 0, 0, 1
		]

	def __mul__(self, other : 'Mat4') -> 'Mat4':
		a = self.m
		b = other.m
		res = [0]*16
		for row in range(4):
			for col in range(4):
				res[row * 4 + col] = sum(a[row * 4 + k] * b[k * 4 + col] for k in range(4))
		return Mat4(res)

	def transform_point(self, v : Vec3) -> Vec3:
		x = v.x*self.m[0] + v.y*self.m[4] + v.z*self.m[8]  + self.m[12]
		y = v.x*self.m[1] + v.y*self.m[5] + v.z*self.m[9]  + self.m[13]
		z = v.x*self.m[2] + v.y*self.m[6] + v.z*self.m[10] + self.m[14]
		w = v.x*self.m[3] + v.y*self.m[7] + v.z*self.m[11] + self.m[15]
		if w != 0 and w != 1:
			x /= w
			y /= w
			z /= w
		return Vec3(x, y, z)

	@staticmethod
	def rotation_x(angle_deg : float) -> 'Mat4':
		a = math.radians(angle_deg)
		c = math.cos(a)
		s = math.sin(a)
		return Mat4([
			1,0,0,0,
			0,c,-s,0,
			0,s, c,0,
			0,0,0,1
		])

	@staticmethod
	def rotation_y(angle_deg: float) -> 'Mat4':
		a = math.radians(angle_deg)
		c = math.cos(a)
		s = math.sin(a)
		return Mat4([
			c, 0, s, 0,
			0, 1, 0, 0,
			-s, 0, c, 0,
			0, 0, 0, 1
		])

	@staticmethod
	def rotation_z(angle_deg : float) -> 'Mat4':
		a = math.radians(angle_deg)
		c = math.cos(a)
		s = math.sin(a)
		return Mat4([
			c,-s,0,0,
			s, c,0,0,
			0, 0,1,0,
			0, 0,0,1
		])

	@staticmethod
	def orthographic(left: float, right: float,
					 bottom: float, top: float,
					 near: float, far: float) -> 'Mat4':
		tx = -(right + left) / (right - left)
		ty = -(top + bottom) / (top - bottom)
		tz = -(far + near) / (far - near)
		return Mat4([
			2/(right-left),    0,                0,              0,
			0,                2/(top-bottom),   0,              0,
			0,                0,               -2/(far-near),   0,
			tx,               ty,               tz,              1
		])
