from mat import Mat4

class Camera:

	def __init__(self, elevation_deg: float = 60, azimuth_deg: float = 45, **kwargs):
		self.elevation = elevation_deg
		self.azimuth = azimuth_deg

	def get_view_matrix(self) -> Mat4:
		rx = Mat4.rotation_x(-self.elevation)
		rz = Mat4.rotation_z(-self.azimuth)
		return rx * rz

	def get_projection_matrix(
		self, width: int, height: int, scale: float = 1.0
	) -> Mat4:
		aspect = width / height
		half_w = scale * aspect
		half_h = scale
		return Mat4.orthographic(-half_w, half_w, -half_h, half_h, -100, 100)
