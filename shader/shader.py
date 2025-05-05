from OpenGL.GL import (
    glCreateShader, glShaderSource, glCompileShader, 
    glGetShaderiv, glGetShaderInfoLog,
    glCreateProgram, glAttachShader, glLinkProgram,
    glGetProgramiv, glGetProgramInfoLog,
    glDeleteShader, glUseProgram,
    glGetUniformLocation, glUniformMatrix4fv,
    glUniform1i, glUniform1f, glUniform3fv,
    GL_VERTEX_SHADER, GL_FRAGMENT_SHADER,
    GL_COMPILE_STATUS, GL_LINK_STATUS, GL_FALSE
)

class Shader:

    def __init__(self, vertex_src : str, fragment_src : str, **kwargs):
        self.handle = self._create_program(vertex_src, fragment_src)
    
    def _compile_shader(self, src : str, shader_type) -> int:
        sh = glCreateShader(shader_type)
        glShaderSource(sh, src)
        glCompileShader(sh)
        status = glGetShaderiv(sh, GL_COMPILE_STATUS)
        if not status:
            log = glGetShaderInfoLog(sh).decode()
            raise RuntimeError(f"pyiso: shader compile failed:\n{log}")
        return sh
    
    def _create_program(self, v_src: str, f_src: str) -> int:
        vert = self._compile_shader(v_src, GL_VERTEX_SHADER)
        frag = self._compile_shader(f_src, GL_FRAGMENT_SHADER)
        prog = glCreateProgram()
        glAttachShader(prog, vert)
        glAttachShader(prog, frag)
        glLinkProgram(prog)
        status = glGetProgramiv(prog, GL_LINK_STATUS)
        if not status:
            log = glGetProgramInfoLog(prog).decode()
            raise RuntimeError(f"Program link failed:\n{log}")
        glDeleteShader(vert)
        glDeleteShader(frag)
        return prog
    
    def use(self) -> None:
        glUseProgram(self.handle)

    def set_uniform_mat4(self, name: str, mat4_list: list[float]) -> None:
        loc = glGetUniformLocation(self.handle, name)
        if loc != -1:
            glUniformMatrix4fv(loc, 1, GL_FALSE, mat4_list)

    def set_uniform_int(self, name: str, val: int):
        loc = glGetUniformLocation(self.handle, name)
        if loc != -1:
            glUniform1i(loc, val)

    def set_uniform_float(self, name: str, val: float):
        loc = glGetUniformLocation(self.handle, name)
        if loc != -1:
            glUniform1f(loc, val)

    def set_uniform_vec3(self, name: str, vals: list[float]):
        loc = glGetUniformLocation(self.handle, name)
        if loc != -1:
            glUniform3fv(loc, 1, vals)
