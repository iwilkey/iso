import math
from .mat import Mat4
from .vec import Vec3

class Quaternion:

	def __init__(self, w: float, x: float, y: float, z: float):
		self.w, self.x, self.y, self.z = w, x, y, z
	
	def __mul__(self, other: 'Quaternion') -> 'Quaternion':
		w1, x1, y1, z1 = self.w, self.x, self.y, self.z
		w2, x2, y2, z2 = other.w, other.x, other.y, other.z
		w = w1*w2 - x1*x2 - y1*y2 - z1*z2
		x = w1*x2 + x1*w2 + y1*z2 - z1*y2
		y = w1*y2 - x1*z2 + y1*w2 + z1*x2
		z = w1*z2 + x1*y2 - y1*x2 + z1*w2
		return Quaternion(w, x, y, z).normalized()

	@staticmethod
	def iden() -> 'Quaternion':
		return Quaternion(1, 0, 0, 0)

	@staticmethod
	def from_axis_angle(axis: Vec3, angle_deg: float) -> "Quaternion":
		half = math.radians(angle_deg) * 0.5
		s = math.sin(half)
		c = math.cos(half)
		nx, ny, nz = axis.x, axis.y, axis.z
		length = math.sqrt(nx*nx + ny*ny + nz*nz)
		if length == 0:
			return Quaternion.iden()
		nx /= length
		ny /= length
		nz /= length
		return Quaternion(c, nx * s, nz * s, ny * s).normalized()

	@staticmethod
	def from_euler(rx_deg: float, ry_deg: float, rz_deg: float) -> "Quaternion":
		rx, ry, rz = map(math.radians, (rx_deg, ry_deg, rz_deg))
		cx, sx = math.cos(rx/2), math.sin(rx/2)
		cy, sy = math.cos(ry/2), math.sin(ry/2)
		cz, sz = math.cos(rz/2), math.sin(rz/2)
		w = cz*cy*cx + sz*sy*sx
		x = cz*cy*sx - sz*sy*cx
		y = cz*sy*cx + sz*cy*sx
		z = sz*cy*cx - cz*sy*sx
		q = Quaternion(w, x, y, z)
		q.y, q.z = q.z, q.y
		return q.normalized()
	
	def to_euler(self) -> Vec3:
		w, x, y, z = self.w, self.x, self.y, self.z
		y, z = z, y
		sinr_cosp = 2 * (w * x + y * z)
		cosr_cosp = 1 - 2 * (x * x + y * y)
		rx = math.atan2(sinr_cosp, cosr_cosp)
		sinp = 2 * (w * y - z * x)
		if abs(sinp) >= 1:
			ry = math.copysign(math.pi / 2, sinp)
		else:
			ry = math.asin(sinp)
		siny_cosp = 2 * (w * z + x * y)
		cosy_cosp = 1 - 2 * (y * y + z * z)
		rz = math.atan2(siny_cosp, cosy_cosp)
		return Vec3(
			math.degrees(rx),
			math.degrees(ry),
			math.degrees(rz)
		)

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
