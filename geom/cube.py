import numpy as np
from .mesh import IsoMesh

class IsoCube(IsoMesh):

    def __init__(self, size: float = 1.0):
        hs = size / 2.0
        base_positions = np.array([
            [-hs, -hs, -hs], [ hs, -hs, -hs],
            [ hs,  hs, -hs], [-hs,  hs, -hs],
            [-hs, -hs,  hs], [ hs, -hs,  hs],
            [ hs,  hs,  hs], [-hs,  hs,  hs],
        ], dtype=np.float32)
        faces = [
            ([0, 2, 1,  0, 3, 2], [1.0, 0.0, 0.0]),
            ([4, 5, 6,  4, 6, 7], [0.0, 1.0, 0.0]),
            ([0, 4, 7,  0, 7, 3], [0.0, 0.0, 1.0]),
            ([1, 2, 6,  1, 6, 5], [1.0, 1.0, 0.0]),
            ([3, 7, 6,  3, 6, 2], [0.0, 1.0, 1.0]),
            ([0, 1, 5,  0, 5, 4], [1.0, 0.0, 1.0]),
        ]
        positions = []
        colors    = []
        for idx_list, color in faces:
            for idx in idx_list:
                positions.append(base_positions[idx])
                colors.append(color)
        positions = np.array(positions, dtype=np.float32)
        colors    = np.array(colors,    dtype=np.float32)
        normals = []
        for idx_list, _ in faces:
            for tri_start in (0, 3):
                i0, i1, i2 = idx_list[tri_start:tri_start+3]
                p0 = base_positions[i0]
                p1 = base_positions[i1]
                p2 = base_positions[i2]
                fn = np.cross(p1-p0, p2-p0)
                fn /= np.linalg.norm(fn)
                normals += [fn, fn, fn]
        normals = np.array(normals, dtype=np.float32)
        data = np.hstack([positions, normals, colors])
        super().__init__(data, layout=[3,3,3], indices=None)
