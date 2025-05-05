import glfw
from shader.shader import Shader
from camera import IsoCamera
from OpenGL.GL import (
    glEnable, glViewport,
    glClearColor, glClear,
    glCullFace, glFrontFace,
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST, GL_CULL_FACE, GL_BACK, GL_CCW
)
from obj.group import IsoObjectGroup
from obj.obj import IsoObject
from geom.cube import IsoCube
from lighting.manager import LightManager
from lighting.directional import DirectionalLight
from mth.transform import Transform
from mth.vec import Vec3
from mth.quaternion import Quaternion

class IsoRenderer:

    def __init__(self, window : 'IsoWindow', **kwargs):
        self.window : 'IsoWindow' = window
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)   
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)
        self.width = 0
        self.height = 0
        self._resize(*glfw.get_framebuffer_size(self.window.handle))
        glfw.set_framebuffer_size_callback(
            self.window.handle,
            lambda win, w, h: self._resize(w, h)
        )
        with open("shader/src/lighting_vertex.glsl", encoding="utf-8") as f:
            VERT_SRC = f.read()
        with open("shader/src/lighting_fragment.glsl", encoding="utf-8") as f:
            FRAG_SRC = f.read()
        self.shader : Shader = Shader(VERT_SRC, FRAG_SRC)
        self.camera : IsoCamera = IsoCamera(
            elevation_deg=60,
            azimuth_deg=45,
            scale=5.0,
            near=-10.0,
            far=10.0
        )
        self.light_mgr = LightManager()
        self.light_mgr.add_directional(
            DirectionalLight(
                direction=Vec3(-1,-1,-1), 
                color=Vec3(1,1,1), 
                intensity=1.0
            )
        )
        self.batch : IsoObjectGroup = IsoObjectGroup()
        self.ISO_CUBE_MESH : IsoMesh = IsoCube(size=1.0)
        self.cube : str = self.batch.add(IsoObject(self.ISO_CUBE_MESH))
        self.cube2 : str = self.batch.add(IsoObject(self.ISO_CUBE_MESH))

    def _resize(self, width : int, height : int):
        self.width = width
        self.height = height
        glViewport(0, 0, width, height)
    
    def _cls(self) -> None:
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    def render(self, dt : float) -> None:
        self.batch.tick(dt)

        self.batch.get(self.cube).set_position(0, -0.5, 0)
        self.batch.get(self.cube).set_scale(10, 1, 10)
        self.batch.get(self.cube2).set_position(1, 1, 1)
        self.batch.get(self.cube2).rotate(0, dt * 100, dt * 100)
        
        self._cls()
        self.shader.use()
        view = self.camera.get_view_matrix().to_list()
        proj = self.camera.get_proj_matrix(self.width / self.height).to_list()
        self.shader.set_uniform_mat4("uView", view)
        self.shader.set_uniform_mat4("uProj", proj)
        self.light_mgr.bind_all(self.shader)
        self.batch.render(self.shader, self.camera)
        self._swap_buffers()
    
    def _swap_buffers(self) -> None:
        glfw.swap_buffers(self.window.handle)
