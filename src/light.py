from vector3 import Vec3
from math import sqrt

class Light:
    def __init__(self, center: Vec3, radius: int, emissionColour: float):
        self.center = center
        self.radius = radius
        self.radius2 = radius * radius
        self.emissionColour = emissionColour

    def intersect(self, vecPos: Vec3, vecDir: Vec3):
        r = self.center - vecPos
        proj = r.dot(vecDir)
        if proj < 0: return None
        d2 = r.dot(r) - proj * proj
        if d2 > self.radius2: return None
        offset = sqrt(self.radius2 - d2)
        return (proj - offset, proj + offset)