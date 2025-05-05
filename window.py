import glfw

from OpenGL.GL import glClearColor, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_TRUE
from renderer import IsoRenderer

class IsoWindow:

    def __init__(self, width : int, height : int, title : str, **kwargs):
        if not glfw.init():
            raise RuntimeError("pyiso: failed to initalize GLFW.")
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        self.handle = glfw.create_window(width, height, title, None, None)
        if not self.handle:
            glfw.terminate()
            raise RuntimeError("pyiso: failed to create GLFW window")
        glfw.make_context_current(self.handle)
        self.renderer : IsoRenderer = IsoRenderer(self)
    
    def should_close(self) -> bool:
        return glfw.window_should_close(self.handle)
    
    def poll_events(self) -> None:
        glfw.poll_events()
    
    def terminate(self) -> None:
        glfw.terminate()
