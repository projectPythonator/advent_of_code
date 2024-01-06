# from sys import stdin
import heapq
from collections import deque
from sys import setrecursionlimit

setrecursionlimit(1000000)
class Lagoon_Solver():
    def __init__(self):
        self.max_n = 1000
        self.R = 0
        self.C = 0
        self.grid = []
        self.commands = []
        self.drc = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.code2dir = {'U':0, 'R':1, 'D':2, 'L':3}

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        m = 0
        n = 2**64
        for line in self.stdin:
            line = line.strip()
            a,b,c=line.split(' ')
            b = int(b)
            c = c[1:-1]
            self.commands.append((a,b,c))
            m = max(m, int(c[1:-1], 16))
            if int(c[1:-1], 16)>15:
                n = min(n, int(c[1:-1], 16))
            print(c, int(c[1:-1], 16))
        #print(len(self.grid), len(self.grid[0]))
        #self.print_out_grid()
        print(n,m, m//n)

    def apply_line(self, amt, mod, pos):
        i,j=pos
        self.grid[i][j] = '#'
        for _ in range(amt):
            i += mod[0]
            j += mod[1]
            self.grid[i][j] = '#'
        return i,j

    def init_grid(self):
        self.grid = [['.' for _ in range(self.max_n)] for _ in range(self.max_n)]

    def print_out_grid(self):
        for line in self.grid:
            print(''.join(line))

    def apply_commands(self):
        pos = (500, 500)
        for a,b,c in self.commands:
            pos = self.apply_line(b, self.drc[self.code2dir[a]], pos)

    def fix_grid(self):
        min_r = self.max_n
        min_c = self.max_n
        max_r = 0
        max_c = 0
        for r in range(self.max_n):
            for c in range(self.max_n):
                if self.grid[r][c] == '#':
                    min_r = min(min_r, r)
                    max_r = max(max_r, r)
                    min_c = min(min_c, c)
                    max_c = max(max_c, c)
        #print("min r {} max r {} min c {} max c {}".format(min_r, max_r, min_c, max_c))
        new_grid = [[self.grid[r][c] for c in range(min_c, max_c+1)] for r in range(min_r, max_r+1)]
        self.grid = [[new_grid[r][c] for c in range(len(new_grid[0]))] for r in range(len(new_grid))]
        self.R = len(self.grid)
        self.C = len(self.grid[0])

    def floodfill(self, r, c, ov, nv):
        self.grid[r][c] = nv
        for rr,cc in self.drc:
            rrr = rr + r
            ccc = cc + c
            if 0 <= rrr < self.R and 0 <= ccc < self.C:
                if self.grid[rrr][ccc] == ov:
                    self.floodfill(rrr, ccc, ov, nv)

    def get_area(self):
        ans = 0
        for i in range(self.R):
            for j in range(self.C):
                if self.grid[i][j] == '#':
                    ans += 1
        return ans

    def solve_lagoon_helper(self):
        self.apply_commands()
        self.fix_grid()
        self.print_out_grid()
        for i in range(self.C):
            if self.grid[0][i] == '#':
                self.floodfill(1, i+1, '.', '#')
                break
        #self.print_out_grid()
        return self.get_area()

    def solve_lagoon(self):
        print(self.solve_lagoon_helper())


def main():
    obj = Lagoon_Solver()
    obj.read_inputs()
    obj.init_grid()
    obj.solve_lagoon()

    #$print(sum(map(int, list('4115453233542453565373363331'))))
main()






