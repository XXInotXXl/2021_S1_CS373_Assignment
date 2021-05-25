import math

from service.matrix import Matrix


def new(w, h, ini=0.0):
    return [[ini for i in range(w)] for i in range(h)]


def extrema(lis):
    return min([min(x) for x in lis]), max([max(x) for x in lis])


def RGB_to_Grey(r, g, b, w, h):
    img = new(w, h)
    for row in range(h):
        for col in range(w):
            img[row][col] = round(r[row][col] * 0.299 + g[row][col] * 0.587 + b[row][col] * 0.114)
    return img


def scale_and_quantize(org, w, h, low=0, high=255):
    img = new(w, h)
    mi, ma = extrema(org)
    for row in range(h):
        for col in range(w):
            try:
                temp = round((org[row][col] - mi) * high / (ma - mi))
                if temp < low:
                    raise Exception
                elif temp > high:
                    temp = high
            except:
                temp = 0
            img[row][col] = temp
    return img


def computer_edges(org, w, h):
    vertical_filter = Matrix.from_string("""
            -1 0 1
            -2 0 2
            -1 0 1
            """)
    horizontal_filter = Matrix.from_string("""
            1 2 1
            0 0 0
            -1 -2 -1
            """)
    org = Matrix(org)
    lis = new(w, h)
    for y in range(h):
        for x in range(w):
            temp = []
            for yd in range(-1, 2):
                temp.append([org.get(x + a, y + yd) for a in range(-1, 2)])
            matr = Matrix(temp)
            vet = matr.dot(vertical_filter) / 8
            hor = matr.dot(horizontal_filter) / 8
            lis[y][x] = round(math.sqrt(vet ** 2 + hor ** 2))
    return lis


def mean_filter_3x3(org, w, h, border="extend"):
    lis = new(w, h)
    org = Matrix(org)
    for y in range(h):
        for x in range(w):
            temp = []
            for yd in range(-1, 2):
                temp.append(sum([org.get(x + a, y + yd) for a in range(-1, 2)]))
            lis[y][x] = round(abs(sum(temp)) / 9)
            lis[y][x] = round(lis[y][x])
    return lis


def median_filter(org, w, h, x=3, y=3, border="extend"):
    lis = new(w, h)
    org = Matrix(org)
    for y in range(h):
        for x in range(w):
            cp = [org.get(x + x1, y + y1, border) for y1 in range(-(y // 2), y // 2 + 1)
                  for x1 in range(-(x // 2), x // 2 + 1)]
            cp.sort()
            lis[y][x] = cp[int((len(cp)) / 2)]
    return lis
