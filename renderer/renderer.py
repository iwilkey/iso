from OpenGL.GL import *
import glfw

class Renderer:
    def __init__(self, width, height, title="Iso Renderer"):
        if not glfw.init():
            raise RuntimeError("glfw.init failed")
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,3)
        glfw.window_hint(glfw.OPENGL_PROFILE,glfw.OPENGL_CORE_PROFILE)
        self.win = glfw.create_window(width, height, title, None, None)
        if not self.win:
            glfw.terminate()
            raise RuntimeError("glfw.create_window failed")
        glfw.make_context_current(self.win)
        glEnable(GL_DEPTH_TEST)

    def should_close(self):
        return glfw.window_should_close(self.win)

    def swap_buffers(self):
        glfw.swap_buffers(self.win)

    def poll_events(self):
        glfw.poll_events()

    def clear(self):
        glClearColor(0.1,0.1,0.1,1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def terminate(self):
        glfw.terminate()
