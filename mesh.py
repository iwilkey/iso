import arcade
from vec import Vec3
from mat import Mat4
from cam import Camera

class Mesh:

	def __init__(
		self, 
		vertices: list[Vec3], 
	 	faces: list[list[int]], 
	  	colors: list = None, 
	   **kwargs
	):
		self.vertices = vertices
		self.faces = faces
		self.colors = colors if colors else []

class Renderable(Mesh):
	"""
	transformable mesh.
	"""
	
	def __init__(
		self,
		vertices: list[Vec3], 
	 	faces: list[list[int]], 
	  	colors: list = None, 
	   **kwargs
	):
		super().__init__(vertices, faces, colors)
		self.transform = Mat4()

	def iden(self):
		self.transform.iden()
 
	def translate(self, dx : float, dy : float, dz : float):
		self.transform = Mat4([
			1, 0, 0, 0,
			0, 1, 0, 0,
			0, 0, 1, 0,
			dx, dy, dz, 1
		]) * self.transform

	def scale(self, sx: float, sy: float, sz: float):
		self.transform = Mat4([
			sx, 0,  0,  0,
			0, sy,  0,  0,
			0,  0, sz, 0,
			0,  0,  0,  1
		]) * self.transform
	
	def rotate_x(self, angle_deg: float):
		self.transform = Mat4.rotation_x(angle_deg) * self.transform

	def rotate_y(self, angle_deg: float):
		self.transform = Mat4.rotation_y(angle_deg) * self.transform

	def rotate_z(self, angle_deg: float):
		self.transform = Mat4.rotation_z(angle_deg) * self.transform

	def get_transformed_vertices(self) -> list[Vec3]:
		return [self.transform.transform_point(v) for v in self.vertices]

	def project(self, camera : Camera):
		view_matrix = camera.get_view_matrix()
		proj_matrix = camera.get_projection_matrix(arcade.get_window().width, arcade.get_window().height, scale=5.0)
		model_verts = self.get_transformed_vertices()
		world_verts = [view_matrix.transform_point(v) for v in model_verts]
		proj_verts  = [proj_matrix.transform_point(v) for v in world_verts]
		return [
	  		((v.x + 1) * arcade.get_window().width / 2,
			(v.y + 1) * arcade.get_window().height / 2)
			for v in proj_verts
		], world_verts

class Cube(Renderable):
    """
    cube with backface culling.
    """
    
    def __init__(self, size: float = 1.0, **kwargs):
        hs = size / 2
        verts = [
            Vec3(-hs, -hs, -hs),
            Vec3( hs, -hs, -hs),
            Vec3( hs,  hs, -hs),
            Vec3(-hs,  hs, -hs),
            Vec3(-hs, -hs,  hs),
            Vec3( hs, -hs,  hs),
            Vec3( hs,  hs,  hs),
            Vec3(-hs,  hs,  hs),
        ]
        faces = [
            [0, 3, 2, 1],
            [4, 5, 6, 7],
            [0, 1, 5, 4],
            [2, 3, 7, 6],
            [1, 2, 6, 5],
            [0, 4, 7, 3],
        ]
        colors = [
            (200, 200, 200),
            (255, 255, 255),
            (255,   0,   0),
            (  0, 255,   0),
            (  0,   0, 255),
            (255, 255,   0),
        ]
        super().__init__(verts, faces, colors, **kwargs)

    def render(self, camera: Camera):
        screen_points, world_verts = self.project(camera)
        face_depths = [
            (sum(world_verts[i].z for i in face) / len(face), idx, face)
            for idx, face in enumerate(self.faces)
        ]
        sorted_faces = sorted(face_depths)
        faces_drawn = 0
        for _, idx, face in sorted_faces:
            pts = [screen_points[i] for i in face]
            x0, y0 = pts[0]
            x1, y1 = pts[1]
            x2, y2 = pts[2]
            cross = (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)
            if cross < 0:
                continue
            color = self.colors[idx]
            arcade.draw_polygon_filled(pts, color)
            arcade.draw_polygon_outline(pts, arcade.color.BLACK)
            faces_drawn += 1
        #print(f"Faces rendered: {faces_drawn} / {len(self.faces)}")
