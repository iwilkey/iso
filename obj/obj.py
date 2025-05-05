import uuid
from geom.mesh import IsoMesh
from camera import IsoCamera
from shader.shader import Shader
from mth.transform import Transform
from mth.quaternion import Quaternion
from mth.vec import Vec3

class IsoObject(IsoMesh):
    
    def __init__(self, mesh : IsoMesh, **kwargs):
        self.id : str = str(uuid.uuid4())
        self.mesh : IsoMesh = mesh
        self.transform : Transform = Transform()
    
    def move(self, dx : float = 0.0, dy : float = 0.0, dz : float = 0.0):
        self.set_position(
            self.transform.position.x + dx,
            self.transform.position.y + dy,
            self.transform.position.z + dz,
        )
    
    def rotate(self, dx_deg=0, dy_deg=0, dz_deg=0):
        qx = Quaternion.from_axis_angle(Vec3(1,0,0), dx_deg)
        qy = Quaternion.from_axis_angle(Vec3(0,1,0), dy_deg)
        qz = Quaternion.from_axis_angle(Vec3(0,0,1), dz_deg)
        delta = qz * (qy * qx)
        self.transform.rotation = (self.transform.rotation * delta).normalized()
    
    def scale(self, dx : float = 0.0, dy : float = 0.0, dz : float = 0.0):
        self.set_scale(
            self.transform.scale.x + dx, 
            self.transform.scale.y + dy, 
            self.transform.scale.z + dz, 
        )

    def set_position(self, x : float, y : float, z : float) -> None:
        self.transform.position.x = x
        self.transform.position.y = y
        self.transform.position.z = z
    
    def set_rotation_euler(self, x : float, y : float, z : float) -> None:
        self.transform.rotation = Quaternion.from_euler(x, y, z)
    
    def set_scale(self, x : float, y : float, z : float) -> None:
        self.transform.scale.x = x
        self.transform.scale.y = y
        self.transform.scale.z = z
    
    def tick(self, dt : float):
        pass
