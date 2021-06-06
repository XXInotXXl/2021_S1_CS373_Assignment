from service.matrix import Matrix

from math import sqrt, cos, sin, radians, pi


class RGBImage:
    r: Matrix
    g: Matrix
    b: Matrix

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        self.rm, self.gm, self.bm = Matrix(r), Matrix(g), Matrix(b)
        if not self.check():
            raise
        self.w = self.rm.w()
        self.h = self.rm.h()

    def check(self):
        return self.rm.same_size(self.gm) and self.gm.same_size(self.bm)

    def hue(self, degree):
        if not 0 < degree < 360:
            raise InvalidDegreeException
        cosA = cos(degree * pi / 180)
        sinA = sin(degree * pi / 180)
        matrix = [
            [cosA + (1 - cosA) / 3, 1 / 3 * (1 - cosA) - sqrt(1 / 3) * sinA, 1 / 3 * (1 - cosA) + sqrt(1 / 3) * sinA],
            [1 / 3 * (1 - cosA) + sqrt(1 / 3) * sinA, cosA + 1 / 3 * (1 - cosA),
             1 / 3 * (1 - cosA) - sqrt(1 / 3) * sinA],
            [1 / 3 * (1 - cosA) - sqrt(1 / 3) * sinA, 1 / 3 * (1 - cosA) + sqrt(1 / 3) * sinA,
             cosA + 1 / 3 * (1 - cosA)]]

        for y in range(self.h):
            for x in range(self.w):
                r, g, b = self.r[y][x], self.g[y][x], self.b[y][x]
                self.r[y][x] = round(r * matrix[0][0] + g * matrix[0][1] + b * matrix[0][2])
                self.g[y][x] = round(r * matrix[1][0] + g * matrix[1][1] + b * matrix[1][2])
                self.b[y][x] = round(r * matrix[2][0] + g * matrix[2][1] + b * matrix[2][2])


class SizeNotEqualException(Exception):

    def __init__(self):
        self.message = "R, G, B matrix do not have same size!"
        super().__init__(self.message)


class InvalidDegreeException(Exception):

    def __init__(self):
        self.message = "Degree should be between 0 and 360!"
        super().__init__(self.message)
