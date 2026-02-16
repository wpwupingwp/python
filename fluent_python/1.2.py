#!/usr/bin/python3

import attr


@attr.s
class Vector:
    x = attr.ib()
    y = attr.ib()
    z = attr.ib()

    def __add__(self, y):
        return Vector(self.x + y.x, self.y + y.y, self.z + y.z)

    def __abs__(self):
        return pow(sum([self.x * self.x, self.y * self.y, self.z * self.z]), 0.5)

    def __mul__(self, y):
        if isinstance(y, Vector):
            return sum([self.x * y.x, self.y * y.y, self.z * y.z])
        elif isinstance(y, (int, float)):
            return Vector(self.x * y, self.y * y, self.z * y)


a = Vector(1, 0, 1)
b = Vector(-1, 10, -1)
print("a", a)
print("b", b)
for c in ["a*3", "a+b", "a*b", "b*a", "abs(b)", "a*a"]:
    print(c, eval(c))
