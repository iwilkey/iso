import math
from .mat import Mat4

class Quaternion:

	def __init__(self, w: float, x: float, y: float, z: float, **kwargs):
		self.w, self.x, self.y, self.z = w, x, y, z
	
	@staticmethod
	def iden() -> 'Quaternion':
		return Quaternion(1, 0, 0, 0)

	@staticmethod
	def from_euler(rx_deg: float, ry_deg: float, rz_deg: float) -> "Quaternion":
		rx, ry, rz = map(math.radians, (rx_deg, ry_deg, rz_deg))
		cx, sx = math.cos(rx/2), math.sin(rx/2)
		cy, sy = math.cos(ry/2), math.sin(ry/2)
		cz, sz = math.cos(rz/2), math.sin(rz/2)
		# q = qz * qy * qx
		w = cz*cy*cx + sz*sy*sx
		x = cz*cy*sx - sz*sy*cx
		y = cz*sy*cx + sz*cy*sx
		z = sz*cy*cx - cz*sy*sx
		return Quaternion(w, x, y, z).normalized()

	def normalized(self) -> "Quaternion":
		norm = math.sqrt(self.w*self.w + self.x*self.x +
						 self.y*self.y + self.z*self.z)
		return Quaternion(self.w/norm, self.x/norm, self.y/norm, self.z/norm)
	
	def to_matrix4(self) -> Mat4:
		w, x, y, z = self.w, self.x, self.y, self.z
		return Mat4([
			1 - 2*(y*y + z*z),   2*(x*y - z*w),     2*(x*z + y*w),   0,
			2*(x*y + z*w),       1 - 2*(x*x + z*z), 2*(y*z - x*w),   0,
			2*(x*z - y*w),       2*(y*z + x*w),     1 - 2*(x*x + y*y), 0,
			0,                   0,                 0,               1,
		])
