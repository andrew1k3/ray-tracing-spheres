from vector3 import Vec3
from math import sqrt

bias = 1e-6

class Plane:
    def __init__(self, center: Vec3, normal: Vec3, surfaceColour: Vec3):
        self.center = center
        self.normal = normal.normalise()
        self.surfaceColour = surfaceColour
    
    def intersect(self, vecPos: Vec3, vecDir: Vec3):
        if abs(self.normal.dot(vecDir)) < bias:
            return None
        t = self.normal.dot(self.center - vecPos)/self.normal.dot(vecDir)
        return (t, t)