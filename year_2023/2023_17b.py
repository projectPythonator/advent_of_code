# from sys import stdin
import heapq
from collections import deque
class SSSP_Solver():
    def __init__(self):
        self.grid = []
        self.drc = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.dir2walks = [[0, 1, 3], [1, 0, 2], [2, 1, 3], [3, 0, 2]]

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        m = 0
        for line in self.stdin:
            line = line.strip()
            self.grid.append(list(map(int, list(line))))
        #print(len(self.grid), len(self.grid[0]))
        #self.print_out_grid()

    def print_out_grid(self):
        for line in self.grid:
            print(''.join(line))

    def dijkstras(self, s, goal):
        INF = 2**64
        q = s
        dst = {}
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                for k in range(11):
                    for l in range(len(self.drc)):
                        dst[(i, j, k, l)] = INF
        for el in s:
            dst[el] = 0
        print("starting")
        while q:
            state = heapq.heappop(q)
            h, i, j, l, d = state
            if h>dst[(i, j, l, d)]:
                continue
            if i == goal[0] and j == goal[1] and l>=4:
                return h

            for v in self.dir2walks[d]:
                r = i + self.drc[v][0]
                c = j + self.drc[v][1]
                if (v == d and l == 10) or (v != d and l < 4) or (r < 0 or c < 0 or r >= len(self.grid) or c >= len(self.grid[0])):
                    continue
                n_l = 1 if v != d else l + 1
                if dst[(r, c, n_l, v)] > h + self.grid[r][c]:
                    dst[(r, c, n_l, v)] = h + self.grid[r][c]
                    heapq.heappush(q, (h + self.grid[r][c], r, c, n_l, v))
        # print(dst)
        # for k in range(3):
        #     for l in range(len(self.drc)):
        #         ans =
        # for i in range(len(self.grid)):
        #     for j in range(len(self.grid[0])):
        #         if dst[(i,j)] == 102:
        #             print(i,j)
        # print(goal)
        # return dst[goal]

    def solve_SSSP(self):
        print(self.dijkstras([(0, 0, 0, 0, 1), (0, 0, 0, 1, 2)], (len(self.grid)-1, len(self.grid[0])-1)))


def main():
    obj = SSSP_Solver()
    obj.read_inputs()
    obj.solve_SSSP()

    #$print(sum(map(int, list('4115453233542453565373363331'))))
main()






