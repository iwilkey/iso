from mth.mat import Mat4

class IsoCamera:
    def __init__(self, elevation=35.264, azimuth=45, scale=2.5):
        self.elevation = elevation
        self.azimuth   = azimuth
        self.scale     = scale

    def get_view_matrix(self) -> Mat4:
        # rotate first around X, then around Z
        rx = Mat4.rotation_x(self.elevation)
        rz = Mat4.rotation_z(self.azimuth)
        return rz * rx

    def get_proj_matrix(self, aspect_ratio: float) -> Mat4:
        s = self.scale
        # symmetric ortho volume
        return Mat4.orthographic(-s*aspect_ratio, s*aspect_ratio,
                                 -s, s,
                                 -10, 10)
