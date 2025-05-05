from abc import ABC, abstractmethod
from shader.shader import Shader

class Light(ABC):

    @abstractmethod
    def bind(self, shader: Shader, index: int):
        pass
