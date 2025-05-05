import ctypes
import numpy as np
from typing import List
from OpenGL.GL import *
from shader.shader import Shader
from mth.mat import Mat4
from mth.transform import Transform

class IsoMesh:

    def __init__(
        self,
        data: np.ndarray,
        layout: List[int],
        indices: np.ndarray = None,
        mode=GL_TRIANGLES,
        max_instances: int = 1000,
    ):
        assert data.dtype == np.float32 and data.ndim == 2
        assert sum(layout) == data.shape[1]
        self.vertex_count = data.shape[0]
        self.mode = mode
        self.has_indices = indices is not None
        self.attrib_count = len(layout)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
        stride = data.strides[0]
        offset = 0
        for attrib_index, comp_count in enumerate(layout):
            glEnableVertexAttribArray(attrib_index)
            glVertexAttribPointer(
                attrib_index,
                comp_count,
                GL_FLOAT,
                GL_FALSE,
                stride,
                ctypes.c_void_p(offset)
            )
            offset += comp_count * data.dtype.itemsize
        if self.has_indices:
            assert indices.dtype == np.uint32 and indices.ndim == 1
            self.index_count = indices.size
            self.ebo = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                         indices.nbytes, indices, GL_STATIC_DRAW)
        self.enable_instancing(max_instances, base_loc=self.attrib_count)
        glBindVertexArray(0)

    def enable_instancing(self, max_instances: int, base_loc: int):
        self.instance_vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.instance_vbo)
        glBufferData(GL_ARRAY_BUFFER, max_instances * 16 * sizeof(GLfloat),
                     None, GL_DYNAMIC_DRAW)
        stride = 16 * sizeof(GLfloat)
        for i in range(4):
            loc = base_loc + i
            glEnableVertexAttribArray(loc)
            glVertexAttribPointer(
                loc, 4, GL_FLOAT, GL_FALSE,
                stride, ctypes.c_void_p(i * 4 * sizeof(GLfloat))
            )
            glVertexAttribDivisor(loc, 1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        self.max_instances = max_instances
        self.instance_count = 0

    def update_instances(self, matrices: List[List[float]]):
        count = len(matrices)
        assert count <= self.max_instances
        self.instance_count = count
        flat = (GLfloat * (16 * count))(*sum(matrices, []))
        glBindBuffer(GL_ARRAY_BUFFER, self.instance_vbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0, sizeof(flat), flat)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw_instanced(self):
        glBindVertexArray(self.vao)
        glDrawArraysInstanced(
            self.mode,
            0,
            self.vertex_count,
            self.instance_count
        )
        glBindVertexArray(0)
