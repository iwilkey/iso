from OpenGL.GL import *
import os

def _check_compile(shader):
    status = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not status:
        log = glGetShaderInfoLog(shader).decode()
        raise RuntimeError(f"Shader compile error:\n{log}")

def _check_link(prog):
    status = glGetProgramiv(prog, GL_LINK_STATUS)
    if not status:
        log = glGetProgramInfoLog(prog).decode()
        raise RuntimeError(f"Program link error:\n{log}")

def compile_shader(path: str, shader_type: int) -> int:
    src = open(path).read()
    sh = glCreateShader(shader_type)
    glShaderSource(sh, src)
    glCompileShader(sh)
    _check_compile(sh)
    return sh

def create_program(vs_path: str, fs_path: str) -> int:
    vert = compile_shader(vs_path, GL_VERTEX_SHADER)
    frag = compile_shader(fs_path, GL_FRAGMENT_SHADER)
    prog = glCreateProgram()
    glAttachShader(prog, vert)
    glAttachShader(prog, frag)
    glLinkProgram(prog)
    _check_link(prog)
    glDeleteShader(vert)
    glDeleteShader(frag)
    return prog
