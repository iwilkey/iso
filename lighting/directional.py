import math
from mth.vec import Vec3
from .base import Light
from shader.shader import Shader

class DirectionalLight(Light):

    def __init__(self, direction: Vec3, color: Vec3, intensity: float = 1.0):
        self.direction = direction * (1.0 / math.sqrt(direction.dot(direction)))
        self.color     = color
        self.intensity = intensity

    def bind(self, shader: Shader, index: int = 0):
        prefix = f"dirLights[{index}]"
        shader.set_uniform_int("numDirLights", len(shader.light_mgr.directional))
        shader.set_uniform_vec3(f"{prefix}.direction", [self.direction.x,
                                                           self.direction.y,
                                                           self.direction.z])
        shader.set_uniform_vec3(f"{prefix}.color",     [self.color.x,
                                                           self.color.y,
                                                           self.color.z])
        shader.set_uniform_float(f"{prefix}.intensity", self.intensity)
