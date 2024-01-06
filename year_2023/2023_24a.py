# from sys import stdin
import heapq
import math
import re

INF = 0
EPS=1e-12
NUM_SIG=9

class pt_xy:
    def __init__(self, new_x=float(0), new_y=float(0)): self.x,self.y=round(new_x), round(new_y)
    def set_pt_xy(self, n_pt_xy): self.x, self.y = n_pt_xy.x, n_pt_xy.y
    def display(self): print(self.x, self.y)
    def __add__(self, b): return pt_xy(self.x + b.x, self.y + b.y)
    def __sub__(self, b): return pt_xy(self.x - b.x, self.y - b.y)
    def __mul__(self, c): return pt_xy(self.x * c, self.y * c)
    def __truediv__(self, c): return pt_xy(self.x / c, self.y / c)  # does this even make sense in a int based point
    def __floordiv__(self, c): return pt_xy(self.x // c, self.y // c)
    def __lt__(self, b): return (self.x, self.y) < (b.x, b.y)
    def __eq__(self, b): return (self.x == b.x) and (self.y == b.y)

    # def __lt__(self, b): return (self.x<b.x) if math.fabs(self.x-b.x)>EPS else (self.y<b.y)
    # def __eq__(self, b): return (abs(self.x-b.x)<EPS) and (abs(self.y-b.y)<EPS)

    def __str__(self): return "{} {}".format(self.x, self.y)
    def __str__(self): return "(x={},y={})".format(self.x, self.y)
    def __round__(self, n): return pt_xy(round(self.x, n), round(self.y, n))
    def __hash__(self): return hash((self.x, self.y))

class GEO_ALGOS:
    def __init__(self):
        pass

    def epscmp(self, x):
        return -1 if x < -EPS else 1 if x > EPS else 0

    def c_cmp(self, a, b): return 0 if math.isclose(a, b) else -1 if a < b else 1

    def euclidean_distance(self, a, b): return math.hypot((a - b).x, (a - b).y)

    # TODO look up and see how well the z cord translates into these functions
    def dot_product(self, a, b): return a.x * b.x + a.y * b.y  # move to point class

    def cross_product(self, a, b): return a.x * b.y - a.y * b.x

    def dist2(self, a, b): return self.dot_product(a - b, a - b)

    def is_lines_parallel(self, a, b, c, d):
        return (self.epscmp(self.cross_product(b - a, c - d)) == 0)
        # return (abs(self.cross_product(b-a, c-d))<EPS)

    def is_lines_collinear(self, a, b, c, d):  # copy paste code if its too slow this is safety from typing errors
        return (self.is_lines_parallel(a, b, c, d)
                and self.is_lines_parallel(b, a, a, c)
                and self.is_lines_parallel(d, c, c, a))

    # return if collinear to get a unique intersection or check outside the funtion before hand
    def is_segments_intersect(self, a, b, c, d):
        if self.is_lines_collinear(a, b, c, d):
            if self.dist2(a, c) < EPS or self.dist2(a, d) < EPS or self.dist2(b, c) < EPS or self.dist2(b, d) < EPS:
                return True
            return not (self.dot_product(c - a, c - b) > 0 and self.dot_product(d - a, d - b) > 0 and self.dot_product(
                c - b, d - b) > 0)
        return not ((self.cross_product(d - a, b - a) * self.cross_product(c - a, b - a) > 0)
                    or (self.cross_product(a - c, d - c) * self.cross_product(b - c, d - c) > 0))

    def pt_line_segment_intersect(self, a, b, c, d):
        y, x, cp=d.y-c.y, c.x-d.x, self.cross_product(d,c)
        u=math.fabs(y*a.x+x*a.y+cp)
        v=math.fabs(y*b.x+x*b.y+cp)
        return pt_xy((a.x*v+b.x*u)/(v+u),(a.y*v+b.y*u)/(v+u))

class The_Odds_Solver():
    def __init__(self):
        self.grid = []
        self.line_segs = []
        self.geometry = GEO_ALGOS()

    def read_inputs(self):
        tim = 2**300
        self.stdin = open('myfile.txt', 'r')
        for line in self.stdin:
            line = line.strip()
            line = re.sub(" +", "", line)
            pt,vel = line.split('@')
            x,y,z = map(int, pt.split(','))
            a,b,c = map(int, vel.split(','))
            mod = pt_xy(a*tim, b*tim)
            mod2 = pt_xy(-a * tim, -b * tim)
            pt1 = pt_xy(x, y) + mod2
            pt2 = pt_xy(x, y) + mod
            self.line_segs.append((pt1, pt2))
        self.stdin.close()

    def get_start(self):
        pass

    def init_data(self):
        pass

    def solve_the_odds_helper(self, lower, upper):
        ans = 0
        for i in range(len(self.line_segs)):
            a, b = self.line_segs[i]
            for j in range(i+1, len(self.line_segs)):
                c, d = self.line_segs[j]
                if self.geometry.is_segments_intersect(a, b, c, d):
                    intersect_point = self.geometry.pt_line_segment_intersect(a, b, c, d)
                    if self.geometry.c_cmp(intersect_point.x, lower) >= 0 >= self.geometry.c_cmp(intersect_point.x, upper) and \
                            self.geometry.c_cmp(intersect_point.y, lower) >= 0 >= self.geometry.c_cmp(intersect_point.y,
                                                                                                      upper):
                        ans += 1
        return ans

    def solve_the_odds(self):
        print(self.solve_the_odds_helper(-2**500, 2**500))
        ans = 0
        for i in range(5):
            for j in range(i+1, 5):
                ans += 1
        print(ans)
        a,b = self.line_segs[1]
        c,d = self.line_segs[2]
        print(self.geometry.is_lines_parallel(a,b,c,d))


def main():
    obj = The_Odds_Solver()
    obj.read_inputs()
    obj.init_data()
    obj.solve_the_odds()
main()






