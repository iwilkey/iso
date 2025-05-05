from .vec        import Vec3
from .quaternion import Quaternion
from .mat        import Mat4

class Transform:

    def __init__(
        self,
        position: Vec3    = None,
        rotation: Quaternion = None,
        scale:    Vec3    = None,
    ):
        self.position = position if position is not None else Vec3(0, 0, 0)
        self.rotation = rotation if rotation is not None else Quaternion.iden()
        self.scale    = scale    if scale    is not None else Vec3(1, 1, 1)

    def get_matrix(self) -> Mat4:
        T = Mat4.translation(
            self.position.x,
            self.position.z,
            self.position.y
        )
        R = self.rotation.to_matrix4()
        S = Mat4.scale(
            self.scale.x,
            self.scale.z,
            self.scale.y
        )
        return R * T * S
