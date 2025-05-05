from typing import List
from .base import Light
from .directional import DirectionalLight
from shader.shader import Shader

class LightManager:

    def __init__(self):
        self.directional: List[DirectionalLight] = []

    def add_directional(self, light: DirectionalLight):
        self.directional.append(light)

    def bind_all(self, shader: Shader):
        shader.light_mgr = self
        for i, l in enumerate(self.directional):
            l.bind(shader, i)
