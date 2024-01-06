# from sys import stdin
import cProfile
import heapq
from collections import deque
from sys import getsizeof


import sys
from numbers import Number
from collections import deque
from collections.abc import Set, Mapping


ZERO_DEPTH_BASES = (str, bytes, Number, range, bytearray)

INF = 2**31

def getsize(obj_0):
    """Recursively iterate to sum size of object & members."""
    _seen_ids = set()
    def inner(obj):
        obj_id = id(obj)
        if obj_id in _seen_ids:
            return 0
        _seen_ids.add(obj_id)
        size = sys.getsizeof(obj)
        if isinstance(obj, ZERO_DEPTH_BASES):
            pass # bypass remaining control flow and return
        elif isinstance(obj, (tuple, list, Set, deque)):
            size += sum(inner(i) for i in obj)
        elif isinstance(obj, Mapping) or hasattr(obj, 'items'):
            size += sum(inner(k) + inner(v) for k, v in getattr(obj, 'items')())
        # Check for custom object instances - may subclass above too
        if hasattr(obj, '__dict__'):
            size += inner(vars(obj))
        if hasattr(obj, '__slots__'): # can have __slots__ with __dict__
            size += sum(inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s))
        return size
    return inner(obj_0)

class Step_Solver():
    def __init__(self):
        self.mem = [5712, 6627, 954, 5687, 6613, 949, 5676, 6616, 961, 5701, 944, 6638]
        self.grid = []
        self.multiplier = 21
        self.R_base = 0
        self.C_base = 0
        self.R_max = 0
        self.C_max = 0
        self.distances = []
        self.drc = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        for line in self.stdin:
            line = line.strip()
            self.grid.append(list(line))
        self.stdin.close()
        self.R_base = len(self.grid)
        self.C_base = len(self.grid[0])
        self.R_max = self.R_base * self.multiplier
        self.C_max = self.C_base * self.multiplier
        print(self.R_base, self.C_base)

    def get_start(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 'S':
                    self.grid[i][j] = '.'
                    return (i, j)
        return None

    def init_data(self):
        self.beg = self.get_start()
        self.beg = (self.beg[0]+self.R_base*(self.multiplier//2), self.beg[1]+self.C_base*(self.multiplier//2))
        self.distances = [[INF for _ in range(self.C_max)] for _ in range(self.R_max)]
        tmp = [[False for _ in range(self.C_max)] for _ in range(self.R_max)]
        for i in range(self.R_base):
            for j in range(self.C_base):
                for k in range(self.multiplier):
                    for l in range(self.multiplier):
                        tmp[i+k*self.R_base][j+l*self.C_base] = True if self.grid[i][j] == '.' else False
        #self.grid = [[tmp[i][j] for j in range(self.C_max)] for i in range(self.R_max)]
        self.grid = [[tmp[i][j] for j in range(self.C_max)] for i in range(self.R_max)]
        tmp = []

        temp = [0] * self.R_max
        for i in range(self.R_max):
            val = 0
            for j in range(self.C_max):
                if self.grid[i][j]:
                    val = val | (1 << j)
            temp[i] = val
        # sum_of_rows_2d_arr = 0
        # sum_of_rows_bitmask = 0
        # for i in range(self.R_max):
        #     sum_of_rows_2d_arr += getsizeof(self.grid[i])
        #     sum_of_rows_bitmask += getsizeof(temp[i])
        # print("sum of the row sizes in 2d array {} sum of the row sizes in array of bitmasks {}".format(sum_of_rows_2d_arr, sum_of_rows_bitmask))
        # print("size of grid is {} size of bitmask array is {}".format(getsizeof(self.grid), getsizeof(temp)))
        print("size using stkoverflow 2d {} size using stkoverflow bitmask {}".format(getsize(self.grid), getsize(temp)))

    def dijkstras(self):
        beg = self.beg
        print(beg)
        # q = [(0, beg)]
        q = deque()
        q.append((0, beg))
        self.distances[beg[0]][beg[1]] = 0
        self.R = self.R_max
        self.C = self.C_max
        while q:
            # d, v = heapq.heappop(q)
            d, v = q.popleft()
            i, j = v
            if d>self.distances[i][j]:
                continue

            for r,c in self.drc:
                a,b=i+r,j+c
                if 0 <= a < self.R and 0 <= b < self.C and self.grid[a][b] and self.distances[a][b] > d + 1:
                    self.distances[a][b] = d + 1
                    # heapq.heappush(q, (d+1, (a, b)))
                    q.append((d+1, (a, b)))
                # if a < 0 or a >= self.R or b < 0 or b >= self.C:
                #     continue
                # if self.grid[a][b] == '#':
                #     continue
                # if self.distances[a][b] > d + 1:
                #     self.distances[a][b] = d + 1
                #     heapq.heappush(q, (d+1, (a, b)))
                #     #q.append((d+1, (a, b)))


    def solve_steps_helper(self, steps):
        self.dijkstras()
        ans = [[0 for _ in range(self.multiplier)] for _ in range(self.multiplier)]
        for k in range(self.multiplier):
            for l in range(self.multiplier):
                for i in range(self.R_base):
                    for j in range(self.C_base):
                        if self.distances[i+k*self.R_base][j+l*self.C_base]<=steps and self.distances[i+k*self.R_base][j+l*self.C_base]%2==1:
                            ans[k][l] += 1
                #print("ans for quad {} {} is {}".format(k, l, ans[k][l]))
        for k in range(self.multiplier):
            print(' '.join([str(el).ljust(5) for el in ans[k]]))
        print("ans of middle one is {}".format(ans[self.multiplier//2][self.multiplier//2]))
        # outer_ring = [937, 915, 926, 940]
        # second_last = [6580, 6597, 6587, 6592]
        # cross_spots = [5631, 5636, 5643, 5638]
        # rings = [7553, 7541]

        #node here refers to an entire pattern patch
        outer_ring = [954, 949, 961, 944] #outer ring minus the axis nodes
        second_last = [6627, 6613, 6616, 6638] #second last ring minus the axis nodes
        cross_spots = [5712, 5687, 5676, 5701] #the axis nodes at the very end of the each axis
        rings = [7553, 7541] #the alternating pattern of all other nodes
        r_ans = 0
        ind = 0
        mul = 1
        dist = 0
        while True:
            if dist + 131 > steps:
                # print("ind {} ind -1 {}".format(ind, ind-1))
                for el in second_last:
                    r_ans += (el * (ind - 1))
                for el in outer_ring:
                    r_ans += (el * ind)
                r_ans += sum(cross_spots)
                break
            else:
                # print(rings[ind % 2])
                r_ans += (rings[ind % 2] * mul)
                ind += 1
                mul = 4 * ind
                dist += 131
        real_ans = 0
        for el in ans:
            real_ans += sum(el)
        print(steps)
        print("real_ans {} our calculated ans {} difference {}".format(real_ans, r_ans, real_ans-r_ans))
        print("ind {} dist {} mul {} steps {}".format(ind, dist, mul, steps))
        return ans


    def solve_steps(self):
        print(getsize(self.distances))
        self.solve_steps_helper(26501365)
        print(getsize(self.distances))

def test_func():
    obj = Step_Solver()
    obj.read_inputs()
    obj.init_data()
    obj.solve_steps()


def main():
    test_func()
    #cProfile.run('test_func()')
main()






