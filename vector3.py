from math import sqrt

class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, (int, float)):
            return Vec3(self.x * other, self.y * other, self.z * other)
        
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        return Vec3(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    def normalise(self):
        mag = sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        self.x = self.x / mag
        self.y = self.y / mag
        self.z = self.z / mag
        return self

    def cap(self, val):
        return Vec3(min(max(self.x, 0), val),
                    min(max(self.y, 0), val),
                    min(max(self.z, 0), val))


def tests():
    vec1 = Vec3(1, 2, 3)
    vec2 = Vec3(4, 5, 6)
    # all tests
    print(vec1 + vec2) # (5, 7, 9)
    print(vec1 - vec2) # (-3, -3, -3)
    print(vec1 * 2) # (2, 4, 6)
    print(vec1 * vec2) # (4, 10, 18)
    print(vec1.dot(vec2)) # 32
    print(vec1.cross(vec2)) # (-3, 6, -3)
    vec1.normalise()
    print(vec1) # (0.2672612419124244, 0.5345224838248488,
    # 0.8017837257372732)


if __name__ == "__main__":
    tests()