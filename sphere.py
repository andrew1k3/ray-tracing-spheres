from vector3 import Vec3
from math import sqrt

class Sphere:
    def __init__(self, center: Vec3, radius: int, surfaceColour: Vec3, emissionColour: Vec3):
        self.center = center
        self.radius = radius
        self.radius2 = radius * radius
        self.surfaceColour = surfaceColour
        self.emissionColour = emissionColour
        self.isLight = emissionColour.x > 0

    def intersect(self, vecPos: Vec3, vecDir: Vec3):
        r = self.center - vecPos
        proj = r.dot(vecDir)
        if proj < 0: return None
        d2 = r.dot(r) - proj * proj
        if d2 > self.radius2: return None
        offset = sqrt(self.radius2 - d2)
        return (proj - offset, proj + offset)