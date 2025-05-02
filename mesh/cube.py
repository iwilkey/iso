from OpenGL.GL import *
import numpy as np

class CubeMesh:
    def __init__(self):
        # 8 corners
        self.positions = np.array([
            [-1, -1, -1], [ 1, -1, -1],
            [ 1,  1, -1], [-1,  1, -1],
            [-1, -1,  1], [ 1, -1,  1],
            [ 1,  1,  1], [-1,  1,  1],
        ], dtype=np.float32)

        # face‑by‑face colors (6 faces × 2 triangles × 3 verts)
        face_colors = [
            [1,0,0], [0,1,0], [0,0,1],
            [1,1,0], [0,1,1], [1,0,1]
        ]
        colors = []
        for color in face_colors:
            colors += color*6  # 6 vertices per face
        self.colors = np.array(colors, dtype=np.float32)

        # indices
        self.indices = np.array([
            0,1,2, 2,3,0,  # back
            4,5,6, 6,7,4,  # front
            0,4,7, 7,3,0,  # left
            1,5,6, 6,2,1,  # right
            3,2,6, 6,7,3,  # top
            0,1,5, 5,4,0   # bottom
        ], dtype=np.uint32)

        # upload to GPU
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # positions
        self.vbo_pos = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_pos)
        glBufferData(GL_ARRAY_BUFFER, self.positions.nbytes,
                     self.positions, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,3,GL_FLOAT,False,0,None)

        # colors
        self.vbo_col = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_col)
        glBufferData(GL_ARRAY_BUFFER, self.colors.nbytes,
                     self.colors, GL_STATIC_DRAW)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1,3,GL_FLOAT,False,0,None)

        # indices
        self.ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                     self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        glBindVertexArray(0)

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
