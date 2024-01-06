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
        self.check_limit = 5

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
        self.time_hit = []
        self.tim_max = 2**60
        self.point_velocity = []
        self.check_limit = 4
        self.geometry = GEO_ALGOS()

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        for line in self.stdin:
            line = line.strip()
            line = re.sub(" +", "", line)
            pt,vel = line.split('@')
            x,y,z = map(int, pt.split(','))
            a,b,c = map(int, vel.split(','))
            self.point_velocity.append((x, y, z, a, b, c))
        self.stdin.close()

    def get_start(self):
        pass

    def init_data(self):
        pass

    @staticmethod
    def is_over_lap_1d(xi1, xi2, xj1, xj2):
        return xi2 >= xj1 and xj2 >= xi1

    def check_1d(self, x):
        tmp = [(min(xi, xi+(vxi-x)*self.tim_max), max(xi, xi+(vxi-x)*self.tim_max)) for xi,_,_,vxi,_,_  in self.point_velocity[:self.check_limit]]
        for i in range(self.check_limit):
            for j in range(i+1, self.check_limit):
                if not The_Odds_Solver.is_over_lap_1d(tmp[i][0], tmp[i][1], tmp[j][0], tmp[j][1]):
                    return False
        return True

    def check_2d_(self, dx, dy):
        line_segment = []
        for x,y,_,vx,vy,_ in self.point_velocity[:self.check_limit]:
            pt1 = pt_xy(x, y)
            pt2 = pt_xy(x+(vx-dx)*self.tim_max, y+(vy-dy)*self.tim_max)
            line_segment.append((pt1, pt2))
        if self.geometry.is_segments_intersect(line_segment[0][0], line_segment[0][1], line_segment[1][0], line_segment[1][1]) and \
                self.geometry.is_segments_intersect(line_segment[2][0], line_segment[2][1], line_segment[3][0], line_segment[3][1]):
            pt1 = self.geometry.pt_line_segment_intersect(line_segment[0][0], line_segment[0][1], line_segment[1][0], line_segment[1][1])
            pt2 = self.geometry.pt_line_segment_intersect(line_segment[2][0], line_segment[2][1], line_segment[3][0], line_segment[3][1])
            if self.geometry.c_cmp(pt1.x, pt2.x) == 0 and self.geometry.c_cmp(pt1.y, pt2.y) == 0:
                self.fill_times(dx, dy, pt1)
                return True
        return False

    def fill_times(self, x, y, pt):

        for i in range(self.check_limit):
            diff = pt - pt_xy(self.point_velocity[i][0], self.point_velocity[i][1])
            dx = self.point_velocity[i][3] - x
            dy = self.point_velocity[i][4] - y
            val_x = int(round(diff.x))
            val_y = int(round(diff.y))
            if val_x == 0 and val_y == 0:
                print("error x and y was 0")
                while True:
                    a = 1
            if val_x:
                self.time_hit[i] = abs(val_x//dx)
            else:
                self.time_hit[i] = abs(val_y//dy)

    def check_3d(self, dz):
        seen = set()
        seen.add(self.point_velocity[0][2]+((self.point_velocity[0][5]-dz)*self.time_hit[0]))
        for i in range(1, self.check_limit):
            z = self.point_velocity[i][2]+((self.point_velocity[i][5]-dz)*self.time_hit[i])
            if z not in seen:
                return False
        return True

    def get_ans(self, dx, dy, dz):
        x = self.point_velocity[0][0] + (self.time_hit[0] * (self.point_velocity[0][3] - dx))
        y = self.point_velocity[0][1] + (self.time_hit[0] * (self.point_velocity[0][4] - dy))
        z = self.point_velocity[0][2] + (self.time_hit[0] * (self.point_velocity[0][5] - dz))
        print(x, y, z)
        print(sum([x,y,z]))
        print(dx, dy, dz)

    def solve_the_odds_helper(self):
        self.time_hit = [0 for _ in range(self.check_limit)]
        lower = -1000
        upper = 1000
        for x in range(lower, upper):
            if self.check_1d(x):
                for y in range(lower, upper):
                    if self.check_2d_(x, y):
                        print(self.time_hit)
                        for z in range(lower, upper):
                            if self.check_3d(z):
                                self.get_ans(x, y, z)
                                return


    def solve_the_odds(self):
        self.solve_the_odds_helper()


def main():
    obj = The_Odds_Solver()
    obj.read_inputs()
    obj.init_data()
    obj.solve_the_odds()
main()






