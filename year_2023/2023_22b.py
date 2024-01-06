# from sys import stdin
import heapq
from collections import deque
import cProfile

class Sand_Slab_Solver():
    def __init__(self):
        self.plane_3d = []
        self.slabs = []
        self.below = []
        self.above = []
        self.ids = []

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        min_max_vals = [2**32] * 6
        for i in range(3, 6):
            min_max_vals[i] = 0
        for line in self.stdin:
            line = line.strip()
            a,b = line.split('~')
            x1, y1, z1 = map(int, a.split(','))
            x2, y2, z2 = map(int, b.split(','))
            tmp = [x1+1, y1+1, z1+1, x2+2, y2+2, z2+2]
            for i in range(3):
                min_max_vals[i] = min(min_max_vals[i], tmp[i])
            for i in range(3, 6):
                min_max_vals[i] = max(min_max_vals[i], tmp[i])
            self.slabs.append([tmp[2], tmp[5], tmp[1], tmp[4], tmp[0], tmp[3]])
        print(min_max_vals)
        self.max_x = min_max_vals[3]+10
        self.max_y = min_max_vals[4]+10
        self.max_z = min_max_vals[5]+10
        self.stdin.close()


    def init_data(self):
        self.plane_3d = [[[0 for _ in range(self.max_x)] for _ in range(self.max_y)] for _ in range(self.max_z)]
        for y in range(self.max_y):
            for x in range(self.max_x):
                self.plane_3d[0][y][x] = 1
        self.slabs.sort()
        self.below = [set() for _ in range(len(self.slabs))]
        self.above = [set() for _ in range(len(self.slabs))]
        self.ids = [i + 2 for i in range(len(self.slabs))]
        for i, el in enumerate(self.slabs):
            for z in range(el[0], el[1]):
                for y in range(el[2], el[3]):
                    for x in range(el[4], el[5]):
                        self.plane_3d[z][y][x] = i + 2

    def drop_1_level(self, slab):
        y1, y2 = self.slabs[slab][2], self.slabs[slab][3]
        x1, x2 = self.slabs[slab][4], self.slabs[slab][5]
        new_z, top_z = self.slabs[slab][0]-1, self.slabs[slab][1]-1
        code = self.ids[slab]
        for y in range(y1, y2):
            for x in range(x1, x2):
                self.plane_3d[top_z][y][x] = 0
                self.plane_3d[new_z][y][x] = code
        self.slabs[slab][0] -= 1
        self.slabs[slab][1] -= 1

    def can_drop_1_level(self, slab): #returns true if can drop a level more false otherwise
        y1, y2 = self.slabs[slab][2], self.slabs[slab][3]
        x1, x2 = self.slabs[slab][4], self.slabs[slab][5]
        new_z = self.slabs[slab][0] - 1
        for y in range(y1, y2):
            for x in range(x1, x2):
                if self.plane_3d[new_z][y][x] != 0:
                    return False
        return True

    def get_set_of_below(self, slab):
        y1, y2 = self.slabs[slab][2], self.slabs[slab][3]
        x1, x2 = self.slabs[slab][4], self.slabs[slab][5]
        new_z = self.slabs[slab][0] - 1
        if new_z == 0:
            return set()
        r_set = set()
        for y in range(y1, y2):
            for x in range(x1, x2):
                if self.plane_3d[new_z][y][x] > 1:
                    r_set.add(self.plane_3d[new_z][y][x]-2)
        return r_set

    def get_set_of_above(self, slab):
        y1, y2 = self.slabs[slab][2], self.slabs[slab][3]
        x1, x2 = self.slabs[slab][4], self.slabs[slab][5]
        new_z = self.slabs[slab][1]
        r_set = set()
        for y in range(y1, y2):
            for x in range(x1, x2):
                if self.plane_3d[new_z][y][x] > 1:
                    r_set.add(self.plane_3d[new_z][y][x]-2)
        return r_set

    def get_amount_that_would_fall(self, slab):
        q = deque()
        q.append(slab)
        above_copy = [set([i for i in el]) for el in self.above]
        below_copy = [set([i for i in el]) for el in self.below]
        # print(above_copy)
        # print(below_copy)
        r_set = set()
        while q:
            index = q.popleft()
            r_set.add(index)
            for el in above_copy[index]:
                below_copy[el].remove(index)
            for el in above_copy[index]:
                if len(below_copy[el]) == 0:
                    q.append(el)
        return len(r_set)-1


    def solve_sand_slabs_helper(self):
        leno = len(self.slabs)
        for i in range(leno):
            while self.can_drop_1_level(i):
                self.drop_1_level(i)
        for i in range(leno):
            self.above[i] = self.get_set_of_above(i)
            self.below[i] = self.get_set_of_below(i)
        ans = 0
        for i in range(leno):
            check = False
            for el in self.above[i]:
                if len(self.below[el])<2:
                    check = True
                    break
            if check:
                ans += self.get_amount_that_would_fall(i)
        return ans

    def solve_sand_slabs(self):
        print(self.solve_sand_slabs_helper())

def test_func():
    obj = Sand_Slab_Solver()
    obj.read_inputs()
    obj.init_data()
    obj.solve_sand_slabs()

def main():
    cProfile.run('test_func()')
main()






