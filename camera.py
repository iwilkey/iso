from mth.vec import Vec3
from mth.mat import Mat4
import math

class IsoCamera:
    def __init__(
        self,
        elevation_deg: float = 35.264,
        azimuth_deg:   float = 45.0,
        scale:         float = 2.0,
        near:          float = -10.0,
        far:           float =  10.0,
    ):
        self.elevation = elevation_deg
        self.azimuth   = azimuth_deg
        self.scale     = scale
        self.near      = near
        self.far       = far
        self.position  = Vec3(0, 0, 0)

    def get_view_matrix(self) -> Mat4:
        rx = Mat4.rotation_x(self.elevation)
        rz = Mat4.rotation_z(self.azimuth)
        r  = rz * rx
        t = Mat4()
        t.iden()
        t.m[12] = -self.position.x
        t.m[13] = -self.position.y
        t.m[14] = -self.position.z
        return r * t

    def get_proj_matrix(self, aspect_ratio: float) -> Mat4:
        half_h = self.scale
        half_w = self.scale * aspect_ratio
        return Mat4.orthographic(
            -half_w,  half_w,
            -half_h,  half_h,
             self.near, self.far
        )

    def move(self, dx: float, dy: float, dz: float) -> None:
        self.position.x += dx
        self.position.y += dy
        self.position.z += dz

    def rotate(self, d_elev: float, d_azim: float) -> None:
        self.elevation += d_elev
        self.azimuth   += d_azim

    def zoom(self, factor: float) -> None:
        self.scale *= factor
        self.scale = max(0.01, min(self.scale, 100.0))  # clamp
