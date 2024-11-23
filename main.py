from sphere import Sphere
from vector3 import Vec3
from math import tan, pi
from PIL import Image
from os import remove

INF = 1e8

class Scene:
    def __init__(self, width: int, height: int, fov: float, background: Vec3):
        self.spheres = []
        self.width = width
        self.height = height
        self.fov = fov
        self.background = background
        self.screen = [background for _ in range(width * height)]

    def addSphere(self, sphere: Sphere):
        self.spheres.append(sphere)
    
    def trace(self, vecPos: Vec3, vecDir: Vec3):
        tnearst = INF
        sphere = None
        for s in self.spheres:
            t = s.intersect(vecPos, vecDir)
            if t:
                if t[0] < tnearst:
                    tnearst = t[0]
                    sphere = s

        if not sphere:
            return self.background
        
        point = vecPos + vecDir * tnearst
        normal = (point - sphere.center).normalise()
        surfaceColor = Vec3(0, 0, 0)
        bias = 1e-4

        for i, s in enumerate(self.spheres):
            if s.isLight:
                l = (s.center - point).normalise()
                transmission = True
                for j in range(len(self.spheres)):
                    if i != j:
                        if self.spheres[j].intersect(point + normal * bias, l):
                            transmission = False
                            break
                surfaceColor += (sphere.surfaceColour * s.emissionColour) * max(normal.dot(l), 0) * transmission

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
                self.screen[y * self.width + x] = self.trace(Vec3(0, 0, 0), raydir)

        with open("output.ppm", "w+b") as f:
            print("Writing to file...")
            header = f"P6\n{self.width} {self.height}\n255\n"
            f.write(header.encode('ascii'))
            for p in self.screen:
                f.write(bytes([int(p.x), int(p.y), int(p.z)]))
            
            image = Image.open(f)
            image.save("output.png", "PNG", quality=95)
            image.close()
        remove("./output.ppm")
        
        print("Done!")


def main():
    width = input("Enter width: ")
    if width == "":
        width = 640 
        height = 360
        fov = 50
    else:
        height = input("Enter height: ")
        fov = input("Enter FOV: ")

    # scene
    scene = Scene(int(width), int(height), int(fov), Vec3(0, 0, 0))
    
    # platform
    # scene.addSphere(Sphere(Vec3(0, -10004, -20), 10000, Vec3(0.62, 0.71, 0.28), Vec3(0, 0, 0)))

    # lights
    scene.addSphere(Sphere(Vec3(0, 2, 1), 0.1, Vec3(1, 1, 1),  Vec3(0.25, 0.25, 0.25)))
    scene.addSphere(Sphere(Vec3(0, -2, 1), 0.1, Vec3(1, 1, 1), Vec3(0.25, 0.25, 0.25)))
    scene.addSphere(Sphere(Vec3(2, 0, 1), 0.1, Vec3(1, 1, 1),  Vec3(0.25, 0.25, 0.25)))
    scene.addSphere(Sphere(Vec3(-2, 0, 1), 0.1, Vec3(1, 1, 1), Vec3(0.25, 0.25, 0.25)))

    # spheres
    scene.addSphere(Sphere(Vec3(-0.35, 0.75, -10), 1, Vec3(0.96, 0.40, 0.10), Vec3(0, 0, 0)))
    scene.addSphere(Sphere(Vec3(0.615, 0.25, -10), 1, Vec3(0.64, 0.85, 0.31), Vec3(0, 0, 0)))
    scene.addSphere(Sphere(Vec3(-1, -0.5, -10), 1, Vec3(0.05, 0.67, 0.93), Vec3(0, 0, 0)))
    scene.addSphere(Sphere(Vec3(0, -1, -10), 1, Vec3(0.97, 0.97, 0.46), Vec3(0, 0, 0)))

    scene.render()

if __name__ == "__main__":
    main()