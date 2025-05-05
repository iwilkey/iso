from typing import Optional, List
from .obj import IsoObject
from camera import IsoCamera
from shader.shader import Shader

class IsoObjectGroup:

    def __init__(self, **kwargs):
        self.objs : dict[str, IsoObject] = {}

    def add(self, obj : IsoObject) -> str:
        self.objs[obj.id] = obj
        return obj.id
    
    def get(self, id : str) -> Optional[IsoObject]:
        if id not in self.objs: return None
        return self.objs[id]

    def remove(self, id : str) -> bool:
        if id not in self.objs: return False
        self.objs.remove(id)
        return True

    def tick(self, dt : float):
        for _, obj in self.objs.items():
            obj.tick(dt)

    def render(self, shader : Shader, camera : IsoCamera):
        buckets: dict[IsoMesh, List[Transform]] = {}
        for obj in self.objs.values():
            buckets.setdefault(obj.mesh, []).append(obj.transform)
        for mesh, transforms in buckets.items():
            mats = [t.get_matrix().to_list() for t in transforms]
            mesh.update_instances(mats)
            mesh.draw_instanced()
