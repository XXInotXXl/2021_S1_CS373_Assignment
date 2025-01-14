class Matrix:
    matrix: list

    def __init__(self, lis=[]):
        self.matrix = lis

    @staticmethod
    def from_string(st: str = ""):
        temp = st.splitlines()
        temp = [x for x in temp if x != ""]
        lis = []
        for i in temp:
            lis.append([x for x in i.split()])
        for row in range(len(lis)):
            for col in range(len(lis[row])):
                obj = lis[row][col]
                if obj.find("/") != -1:
                    lis[row][col] = int(obj[:obj.find("/")]) / int(obj[obj.find("/") + 1:])
                else:
                    lis[row][col] = int(obj)
        return Matrix(lis)

    @staticmethod
    def format_list(lis):
        return ["{:>5s}".format(str(i)) for i in lis]

    @staticmethod
    def print_list(lis):
        for i in lis:
            print(i, end="")
        print()

    @staticmethod
    def new(image_width, image_height):
        return [[0 for i in range(image_width)] for i in range(image_height)]

    def print(self):
        for row in self.matrix:
            Matrix.print_list(Matrix.format_list(row))

    def w(self):
        return len(self.matrix[0])

    def h(self):
        return len(self.matrix)

    def same_size(self, other):
        return self.w() == other.w() and self.h() == other.h()

    def min(self):
        return min([min(x) for x in self.matrix])

    def max(self):
        return max([max(x) for x in self.matrix])

    def dot(self, other):
        sum = 0
        for r in range(len(self.matrix)):
            for c in range(len(self.matrix[r])):
                sum += (self.matrix[r][c] * other.matrix[r][c])
        return sum

    def matrix_histogram_calculation(self):
        # count
        dic = {}
        for row in self.matrix:
            for col in row:
                if col in dic:
                    dic[col] += 1
                else:
                    dic[col] = 1
        count = [dic[key] for key in sorted(dic)]
        cumulative = list(count)
        for i in range(1, len(cumulative)):
            cumulative[i] = cumulative[i - 1] + cumulative[i]
        keys = sorted(dic)
        lut = [round(255 / (cumulative[-1] - cumulative[0]) * (x - cumulative[0]))
               for x in cumulative]
        return keys, count, cumulative, lut

    def matrix_histogram_report(self):
        keys, count, cumulative, lut = self.matrix_histogram_calculation()
        print("{:>8s}".format("q"), end="")
        Matrix.print_list(Matrix.format_list(keys))
        print("{:>8s}".format("H[q]"), end="")
        Matrix.print_list(Matrix.format_list(count))
        print("{:>8s}".format("C[q]"), end="")
        Matrix.print_list(Matrix.format_list(cumulative))
        print("{:>8s}".format("T[q]"), end="")
        Matrix.print_list(Matrix.format_list(lut))

    def get(self, x, y, border="extend"):
        if border in ["extend", "extended"]:
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            try:
                return self.matrix[y][x]
            except:
                try:
                    return self.matrix[y - 1][x]
                except:
                    try:
                        return self.matrix[y][x - 1]
                    except:
                        try:
                            return self.matrix[y - 1][x - 1]
                        except:
                            return self.get(x - 1, y - 1)
        elif type(border) is int or float:
            try:
                if x < 0 or y < 0:
                    return border
                return self.matrix[y][x]
            except:
                return border
        else:
            raise TypeError("Invalid border value")

    @staticmethod
    def rel(pix, medium=0):
        if pix > medium:
            return 1
        return 0

    def fit(self, other, medium=0):
        # self.matrix and param matrix are considered to be the same size

        for row in range(self.h()):
            for col in range(self.w()):
                if not ((other.get(col, row) == 1 and Matrix.rel(self.get(col, row),medium) == 1) or other.get(col,row) == 0):
                    return False
        return True

    def hit(self, other, medium=0):
        # self.matrix and param matrix are considered to be the same size
        hit_count = 0
        for row in range(self.h()):
            for col in range(self.w()):
                if other.get(col, row) == 1 and Matrix.rel(self.get(col, row),medium) == 1:
                    hit_count += 1
        return hit_count >= 1
