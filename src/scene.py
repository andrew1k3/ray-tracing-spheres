from sphere import Sphere
from light import Light
from plane import Plane
from vector3 import Vec3
from math import tan, pi
from PIL import Image
from os import remove
INF = 1e8

class Scene:
    def __init__(self, width: int, height: int, fov: float, background: Vec3, name: str = "output"):
        self.name = name
        self.objects = []
        self.width = width
        self.height = height
        self.fov = fov
        self.background = background
        self.screen = [background for _ in range(width * height)]

    def add(self, object):
        self.objects.append(object)
    
    def trace(self, vecPos: Vec3, vecDir: Vec3):
        tnearst = INF
        object = None
        for x in self.objects:
            t = x.intersect(vecPos, vecDir)
            if t:
                if t[0] < tnearst:
                    tnearst = t[0]
                    object = x

        if not object:
            return self.background
        
        point = vecDir * tnearst
        if (isinstance(object, Plane)):
            normal = object.normal
        else:
            normal = (point - object.center).normalise()
        surfaceColor = Vec3(0, 0, 0)
        bias = 1e-4

        for i, l in enumerate(self.objects):
            if isinstance(l, Light):
                pointToLight = (l.center - point).normalise()
                transmission = True
                for j, y in enumerate(self.objects):
                    if i != j:
                        if y.intersect(point + normal * bias, pointToLight):
                            transmission = False
                            break
                surfaceColor += object.surfaceColour * l.emissionColour * max(normal.dot(pointToLight), 0) * transmission

        return surfaceColor.cap(1) * 255

    def render(self):
        invWidth = 1 / self.width
        invHeight = 1 / self.height
        aspectRatio = self.width / self.height
        angle = tan(pi * 0.5 * self.fov / 180)
        for y in range(self.height):
            if y % (self.height//10) == 0:
                print(f"Progress: {int((y/self.height)*100)}%")
            for x in range(self.width):
                xx = (2* ((x + 0.5) * invWidth) -1) * angle * aspectRatio
                yy = (1 - 2 * ((y + 0.5) * invHeight)) * angle
                raydir = Vec3(xx, yy, -1).normalise()
                self.screen[y * self.width + x] = self.trace(Vec3(0,0,0), raydir)

        with open(f"./assets/{self.name}.ppm", "w+b") as f:
            print("Writing to file...")
            header = f"P6\n{self.width} {self.height}\n255\n"
            f.write(header.encode('ascii'))
            for p in self.screen:
                f.write(bytes([int(p.x), int(p.y), int(p.z)]))
            
            image = Image.open(f)
            image.save(f"./assets/{self.name}.png", "PNG", quality=95)
            image.close()
        remove(f"./assets/{self.name}.ppm")
        
        print("Done!")