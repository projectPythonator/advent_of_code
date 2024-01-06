# from sys import stdin
import heapq
from collections import deque
from sys import setrecursionlimit

setrecursionlimit(1000000)

INF = 2**100


class pt_xy:
    def __init__(self, a,b):self.x,self.y=a,b
    def __add__(self, b): return pt_xy(self.x+b.x, self.y+b.y)
    def __sub__(self, b): return pt_xy(self.x-b.x, self.y-b.y)
    def __mul__(self, c): return pt_xy(self.x*c, self.y*c)
    def __truediv__(self, c): return pt_xy(self.x/c, self.y/c)
    def __floordiv__(self, c): return pt_xy(self.x//c, self.y//c)
    def __lt__(self, b): return ((self.y, self.x)<(b.y, b.x))
    def __eq__(self, b): return ((self.x,self.y)==(b.x,b.y))
    def __str__(self): return "x={}, y={}".format(self.x, self.y)
    def __round__(self, n): return pt_xy(round(self.x,n),round(self.y,n))
    def __hash__(self):return hash((self.x,self.y))
    def get_tup(self): return (self.x, self.y)

class GEO_ALGOS:
  def __init__(self): pass


class Lagoon_Solver():
    def __init__(self):
        self.point_to_index = {}
        self.index_to_point = []
        self.horizontal_lines = []
        self.horizontal_labels = []
        self.vertical_lines = []
        self.vertical_labels = []
        self.polygon = []
        self.R = 0
        self.C = 0
        self.commands = []
        self.drc = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.code2dir = {'U':0, 'R':1, 'D':2, 'L':3}
        self.code2dir2 = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        m = 0
        n = 2**64
        for line in self.stdin:
            line = line.strip()
            a,b,c=line.split(' ')
            c = c[1:-1]
            b = int(c[1:-1], 16)
            a = self.code2dir2[c[-1]]
            self.commands.append((a,b,c))
            m = max(m, int(c[1:-1], 16))
            # if int(c[1:-1], 16)>15:
            #     n = min(n, int(c[1:-1], 16))
            print(c, int(c[1:-1], 16))
        #print(len(self.grid), len(self.grid[0]))
        #self.print_out_grid()
        print(n,m, m//n)

    def area_by_shoelace(self, x, y):
        "Assumes x,y points go around the polygon in one direction"
        return abs(sum(x[i-1]*y[i]-x[i]*y[i-1] for i in range(len(x)))) / 2.


    def test_if_a_b_intersect_right(self, a, b, c):
        return (a.x >= c.x and a.y < c.y < b.y)

    def test_if_a_b_intersect_bottom(self, a, b, c):
        return (a.y >= c.y and a.x < c.x < b.x)

    def is_right_side_wall(self, a): # return true if right wall false otherwise only works if it is a vertical wall
        mid = a.y + 0.5
        test_point = pt_xy(a.x, mid)
        hit = 0
        for line_a, line_b in self.vertical_lines:
            min_line = min(self.index_to_point[line_a], self.index_to_point[line_b])
            max_line = max(self.index_to_point[line_a], self.index_to_point[line_b])
            if self.test_if_a_b_intersect_right(min_line, max_line, test_point):
                hit += 1
        return (hit%2 == 1)

    def is_bottom_side_wall(self, a): # return true if right wall false otherwise only works if it is a vertical wall
        mid = a.x + 0.5
        test_point = pt_xy(mid, a.y)
        hit = 0
        for line_a, line_b in self.horizontal_lines:
            min_point = min(self.index_to_point[line_a], self.index_to_point[line_b])
            max_point = max(self.index_to_point[line_a], self.index_to_point[line_b])
            if self.test_if_a_b_intersect_bottom(min_point, max_point, test_point):
                hit += 1
        return (hit%2 == 1)

    def label_lines(self):
        print(self.polygon, )
        for line_a, line_b in self.vertical_lines:
            min_point = min(self.index_to_point[line_a], self.index_to_point[line_b])
            # print("using {} to test {} to {}".format(str(min_point), str(self.index_to_point[line_a]), self.index_to_point[line_b]))
            self.vertical_labels.append(self.is_right_side_wall(min_point))
        #     print()
        # print()

        for line_a, line_b in self.horizontal_lines:
            min_point = min(self.index_to_point[line_a], self.index_to_point[line_b])
            # print("using {} to test {} to {}".format(str(min_point), str(self.index_to_point[line_a]),
            #                                          self.index_to_point[line_b]))
            self.horizontal_labels.append(self.is_bottom_side_wall(min_point))

        #print("printing sides")
        for i, ab in enumerate(self.vertical_lines):
            a,b = self.index_to_point[ab[0]], self.index_to_point[ab[1]]
        #     print("line from {} to {} is a {} wall".format(str(a), str(b), "right side" if self.vertical_labels[i] else "left side"))
        # print()
        # print(self.horizontal_labels)
        for i, ab in enumerate(self.horizontal_lines):
            a,b = self.index_to_point[ab[0]], self.index_to_point[ab[1]]
            #print("line from {} to {} is a {} wall".format(str(a), str(b), "bottom side" if self.horizontal_labels[i] else "top side"))

    def fix_lines(self):
        for i, ab in enumerate(self.vertical_lines):
            a,b = self.index_to_point[ab[0]], self.index_to_point[ab[1]]
            if self.vertical_labels[i]:
                a.x += 1
                b.x += 1

        for i, ab in enumerate(self.horizontal_lines):
            a, b = self.index_to_point[ab[0]], self.index_to_point[ab[1]]
            if self.horizontal_labels[i]:
                a.y += 1
                b.y += 1
        print('ours  [({})]'.format('), ('.join([str(self.index_to_point[el]) for el in self.polygon])))
        tmp = [(0, 0), (0, 7), (6,7), (6, 5), (7, 5), (7, 7), (10, 7), (10, 1), (8, 1), (8, 0), (5, 0), (5, 2), (3, 2), (3, 0), (0, 0)]
        test = [pt_xy(y,x) for x,y in tmp]
        print('demos [({})]'.format('), ('.join([str(el) for el in test])))
        test_poly = [(el.x, el.y) for el in self.index_to_point]
        y, x = zip(*test_poly)
        print(self.area_by_shoelace(x, y))




    def build_lines(self):
        for i in range(1, len(self.polygon)):
            b = self.index_to_point[self.polygon[i]]
            a = self.index_to_point[self.polygon[i-1]]
            if a.x == b.x:
                self.vertical_lines.append((self.polygon[i-1], self.polygon[i]))
            else:
                self.horizontal_lines.append((self.polygon[i-1], self.polygon[i]))

    def apply_commands(self):
        p = 0
        index = 0
        pos = (0, 0)
        new_point = pt_xy(pos[0], pos[1])
        if new_point not in self.point_to_index:
            self.point_to_index[new_point] = index
            self.index_to_point.append(new_point)
            index += 1
        self.polygon.append(self.point_to_index[new_point])
        for a,b,c in self.commands:
            r, c = self.drc[self.code2dir[a]]
            pos = (pos[0]+r*b, pos[1]+c*b)
            new_point = pt_xy(pos[1], pos[0])
            if new_point not in self.point_to_index:
                self.point_to_index[new_point] = index
                self.index_to_point.append(new_point)
                index += 1
            self.polygon.append(self.point_to_index[new_point])
        print('ours  [({})]'.format('), ('.join([str(self.index_to_point[el]) for el in self.polygon])))
        y, x = zip(*[self.index_to_point[el].get_tup() for el in self.polygon])
        #print(p, self.area_by_shoelace(x, y), self.polygon)
        tmp = [(0, 0), (0, 7), (6,7), (6, 5), (7, 5), (7, 7), (10, 7), (10, 1), (8, 1), (8, 0), (5, 0), (5, 2), (3, 2), (3, 0), (0, 0)]
        test = [pt_xy(y,x) for x,y in tmp]
        print('demos [({})]'.format('), ('.join([str(el) for el in test])))
        #print('demos {}'.format(self.polygon))
        y, x = zip(*tmp)
        print(p, self.area_by_shoelace(x, y))

    def init_data(self):
        self.apply_commands()
        self.build_lines()
        self.label_lines()
        self.fix_lines()

    def fix_grid(self):
        pass
        # min_r = self.max_n
        # min_c = self.max_n
        # max_r = 0
        # max_c = 0
        # for r in range(self.max_n):
        #     for c in range(self.max_n):
        #         if self.grid[r][c] == '#':
        #             min_r = min(min_r, r)
        #             max_r = max(max_r, r)
        #             min_c = min(min_c, c)
        #             max_c = max(max_c, c)
        # #print("min r {} max r {} min c {} max c {}".format(min_r, max_r, min_c, max_c))
        # new_grid = [[self.grid[r][c] for c in range(min_c, max_c+1)] for r in range(min_r, max_r+1)]
        # self.grid = [[new_grid[r][c] for c in range(len(new_grid[0]))] for r in range(len(new_grid))]
        # self.polygon = [(el[0]-min_r, el[1]-min_c) for el in self.polygon]
        #
        # self.R = len(self.grid)
        # self.C = len(self.grid[0])

    def solve_lagoon_helper(self):
        print(self.polygon)


    def solve_lagoon(self):
        self.solve_lagoon_helper()


def main():
    obj = Lagoon_Solver()
    obj.read_inputs()
    obj.init_data()
    obj.solve_lagoon()

    #$print(sum(map(int, list('4115453233542453565373363331'))))
main()






