class Vec3:

	def __init__(self, x : float = 0, y : float = 0, z : float = 0, **kwargs):
		self.x = x
		self.y = y
		self.z = z

	def __add__(self, other : 'Vec3') -> 'Vec3':
		return Vec3(
			self.x + other.x, 
			self.y + other.y, 
			self.z + other.z
		)

	def __sub__(self, other : 'Vec3') -> 'Vec3':
		return Vec3(
			self.x - other.x, 
			self.y - other.y, 
			self.z - other.z
		)

	def __mul__(self, scalar : float) -> 'Vec3':
		return Vec3(
			self.x * scalar,
			self.y * scalar,
			self.z * scalar
		)

	def dot(self, other : 'Vec3') -> float:
		return self.x * other.x + self.y * other.y + self.z * other.z

	def cross(self, other: 'Vec3') -> 'Vec3':
		return Vec3(
			self.y * other.z - self.z * other.y,
			self.z * other.x - self.x * other.z,
			self.x * other.y - self.y * other.x
		)

	def to_list(self) -> list:
		return [self.x, self.y, self.z]
