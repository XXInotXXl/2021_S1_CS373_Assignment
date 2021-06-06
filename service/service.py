import math

from service import config
from service.matrix import Matrix


class InvalidNeighborException(Exception):

    def __init__(self):
        self.message = "Neighbor should be either 4 or 8"
        super().__init__(self.message)


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


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


def contrast_stretching(org, w, h, g_min=0, g_max=255) -> list:
    img = new(w, h)
    org = Matrix(org)
    mini, maxi = org.min(), org.max()
    for y in range(h):
        for x in range(w):
            try:
                temp = round((org.get(x, y) - mini) * (g_max - g_min) / (maxi - mini)) + g_min
                if temp < g_min:
                    temp = g_min
                elif temp > g_max:
                    temp = g_max
            except:
                temp = 0
            img[y][x] = temp
    return img


def percentile_based_mapping(org, w, h, alpha, beta):
    img = new(w, h)
    org = Matrix(org)
    keys, count, cumulative, lut = org.matrix_histogram_calculation()
    q_alpha, q_beta = 0, 255
    small = cumulative[-1] * alpha / 100
    for q in range(len(keys)):
        if cumulative[q] > small:
            q_alpha = keys[q]
            break
    large = cumulative[-1] * beta / 100
    for q in range(len(keys) - 1, -1, -1):
        if cumulative[q] < large:
            q_beta = keys[q]
            break
    for y in range(h):
        for x in range(w):
            temp = 255 / (q_beta - q_alpha) * (org.get(x, y) - q_alpha)
            if temp < 0:
                temp = 0
            elif temp > 255:
                temp = 255
            img[y][x] = temp
    return img


def mean_filter_3x3(org, w, h, x=3, y=3, border="extend"):
    lis = new(w, h)
    org = Matrix(org)
    for r in range(h):
        for c in range(w):
            temp = [org.get(c + x1, r + y1, border) for y1 in range(-(y // 2), y // 2 + 1)
                    for x1 in range(-(x // 2), x // 2 + 1)]
            lis[r][c] = round(abs(sum(temp)) / (x * y))
    return lis


def median_filter(org, w, h, x=3, y=3, border="extend"):
    lis = new(w, h)
    org = Matrix(org)
    for r in range(h):
        for c in range(w):
            temp = [org.get(c + x1, r + y1, border) for y1 in range(-(y // 2), y // 2 + 1)
                    for x1 in range(-(x // 2), x // 2 + 1)]
            temp.sort()
            lis[r][c] = temp[int((len(temp)) / 2)]
    return lis


def computer_edges(org, w, h):
    vertical_filter = config.VERTICAL_EDGE
    horizontal_filter = config.HORIZONTAL_EDGE
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


def thresholding(org, w, h, value, mini=0, maxi=255):
    lis = new(w, h)
    for y in range(h):
        for x in range(w):
            if org[y][x] < value:
                lis[y][x] = mini
            else:
                lis[y][x] = maxi
    return lis


def adaptive_thresholding(org, w, h, mini=0, maxi=255, cycle=3):
    value = find_threshold(org, cycle)
    return thresholding(org, w, h, value, mini, maxi)


def find_threshold(org, cycle):
    org = Matrix(org)
    keys, count, cumulative, lut = org.matrix_histogram_calculation()
    theta = sum([keys[i] * count[i] for i in range(len(keys))]) / cumulative[-1]
    counter = 0
    while counter < cycle:
        nob = 0
        mid = 0
        for i in range(len(keys)):
            if keys[i] <= theta:
                nob += count[i]
                mid = i
        nbg = cumulative[-1] - nob
        qb = [keys[i] * count[i] for i in range(len(keys))]
        uob, ubg = 0, 0
        for i in range(len(keys)):
            if i <= mid:
                uob += qb[i]
            else:
                ubg += qb[i]
        uob = uob / nob
        ubg = ubg / nbg
        theta = (uob + ubg) / 2
        counter += 1
    return counter


def Erosion(org, w, h, border="extend", neighbor=4):
    if neighbor == 4:
        pattern = config.EROSION_DILATION_4
    elif neighbor == 8:
        pattern = config.EROSION_DILATION_8
    else:
        raise InvalidNeighborException
    org = Matrix(org)
    lis = new(w, h)
    for y in range(h):
        for x in range(w):
            temp = []
            for yd in range(-1, 2):
                temp.append([org.get(x + a, y + yd, border) for a in range(-1, 2)])
            matr = Matrix(temp)
            if matr.fit(pattern):
                lis[y][x] = 1
            else:
                lis[y][x] = 0
    return lis


def Dilation(org, w, h, border="extend", neighbor=4):
    if neighbor == 4:
        pattern = config.EROSION_DILATION_4
    elif neighbor == 8:
        pattern = config.EROSION_DILATION_8
    else:
        raise InvalidNeighborException
    org = Matrix(org)
    lis = new(w, h)
    for y in range(h):
        for x in range(w):
            temp = []
            for yd in range(-1, 2):
                temp.append([org.get(x + a, y + yd, border) for a in range(-1, 2)])
            matr = Matrix(temp)
            if matr.hit(pattern):
                lis[y][x] = 1
            else:
                lis[y][x] = 0
    return lis


def compute_connected_component_labeling(org, w, h):
    visit = new(w, h)
    recorder = {}
    count_label = 0
    for i in range(h):
        for j in range(w):
            if org[i][j] != 0 and visit[i][j] == 0:
                count_label += 1
                q = Queue()
                q.enqueue((i, j))
                component_number = 0
                check = new(w, h)
                check[i][j] = 1
                while q.size() > 0:
                    current_position = q.dequeue()
                    visit[current_position[0]][current_position[1]] = count_label
                    component_number += 1
                    neighbour = []
                    if current_position[1] > 0:
                        neighbour.append((current_position[0], current_position[1] - 1))
                    if current_position[1] < w - 1:
                        neighbour.append((current_position[0], current_position[1] + 1))
                    if current_position[0] > 0:
                        neighbour.append((current_position[0] - 1, current_position[1]))
                    if current_position[0] < h - 1:
                        neighbour.append((current_position[0] + 1, current_position[1]))
                    for n in neighbour:
                        if check[n[0]][n[1]] == 0 and org[n[0]][n[1]]:
                            check[n[0]][n[1]] = 1
                            q.enqueue(n)
                    recorder[count_label] = component_number
    return visit, recorder


def find_largest_connected_component(org, w, h):
    visit, recorder = compute_connected_component_labeling(org, w, h)
    temp = {k: v for k, v in sorted(recorder.items(), key=lambda item: item[-1])}
    largest = list(temp.keys())[-1]
    xl, yl = [], []
    for y in range(h):
        for x in range(w):
            if visit[y][x] == largest:
                xl.append(x)
                yl.append(y)
    x0, y0, x1, y1 = min(xl), min(yl), max(xl), max(yl)
    return x0, y0, x1, y1


def border(org, w, h, x0, y0, x1, y1, width, value):
    lis = new(w, h)
    for y in range(h):
        for x in range(w):
            if (y0 - width < y < y0 and x0 - width < x < x1 + width) or (y1 < y < y1 + width and x0 - width < x < x1 + width) or (
                    x0 - width < x < x0 and y0 - width < y < y1 + width) or (x1 < x < x1 + width and y0 - width < y < y1 + width):
                lis[y][x] = value
            else:
                lis[y][x] = org[y][x]
    return lis
