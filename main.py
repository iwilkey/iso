import numpy as np

from shaders.shader import create_program
from mesh.cube import CubeMesh
from camera.iso_camera import IsoCamera
from renderer.renderer import Renderer
from OpenGL.GL import glUseProgram, glGetUniformLocation, glUniformMatrix4fv

def main():
    WIDTH, HEIGHT = 800, 600
    renderer = Renderer(WIDTH, HEIGHT)
    prog = create_program("shaders/vertex.glsl", "shaders/fragment.glsl")
    cube = CubeMesh()
    cam  = IsoCamera()
    model = np.eye(4, dtype=np.float32)
    loc_uM = glGetUniformLocation(prog, "uModel")
    loc_uV = glGetUniformLocation(prog, "uView")
    loc_uP = glGetUniformLocation(prog, "uProj")
    while not renderer.should_close():
        renderer.poll_events()
        renderer.clear()
        glUseProgram(prog)
        view = cam.get_view_matrix().to_list()
        proj = cam.get_proj_matrix(WIDTH/HEIGHT).to_list()
        glUniformMatrix4fv(loc_uM,1,False,model)
        glUniformMatrix4fv(loc_uV,1,False,view)
        glUniformMatrix4fv(loc_uP,1,False,proj)
        cube.draw()
        renderer.swap_buffers()
    renderer.terminate()

if __name__=="__main__":
    main()
