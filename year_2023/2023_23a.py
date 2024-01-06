# from sys import stdin
import heapq


INF = 0

class Long_Walk_Solver():
    def __init__(self):
        self.grid = []
        self.R_base = 0
        self.C_base = 0
        self.distances = []
        self.drc = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.cant_go_back = {}
        self.can_enter = {}
        self.moves = {}

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        for line in self.stdin:
            line = line.strip()
            self.grid.append(list(line))
        self.stdin.close()

    def get_start(self):
        self.beg = (0, 1)

    def init_data(self):
        self.R_base = len(self.grid)
        self.C_base = len(self.grid[0])
        self.distances = [[2 for _ in range(self.C_base)] for _ in range(self.R_base)]
        self.can_enter['#'] = set()
        self.can_enter['.'] = set(self.drc)
        self.moves['.'] = set(self.drc)
        self.cant_go_back[self.drc[0]] = self.drc[2]
        self.cant_go_back[self.drc[1]] = self.drc[3]
        self.cant_go_back[self.drc[2]] = self.drc[0]
        self.cant_go_back[self.drc[3]] = self.drc[1]
        for i, c in enumerate('^>v<'):
            self.can_enter[c] = {self.drc[i]}
            self.moves[c] = {self.drc[i]}


    def longest_dijkstras(self):
        self.get_start()
        beg = self.beg
        q = [(0, beg, self.drc[3])]
        self.distances[beg[0]][beg[1]] = 0
        self.R = self.R_base
        self.C = self.C_base
        while q:
            d, v, l = heapq.heappop(q)
            i, j = v
            #print(d, i, j, l)
            if d > self.distances[i][j]:
                continue

            for r, c in self.moves[self.grid[i][j]]:
                a, b = i+r, j+c
                #print(a, b)
                if 0 <= a < self.R and \
                    0 <= b < self.C and \
                    (r, c) in self.can_enter[self.grid[a][b]] and \
                        (r, c) != self.cant_go_back[l] and \
                        self.distances[a][b] > d - 1:
                    self.distances[a][b] = d - 1
                    heapq.heappush(q, (d-1, (a, b), (r, c)))
        return -self.distances[self.R-1][self.C-2]


    def solve_long_walk_helper(self):
        return self.longest_dijkstras()


    def solve_long_walk(self):
        print(self.solve_long_walk_helper())


def main():
    obj = Long_Walk_Solver()
    obj.read_inputs()
    obj.init_data()
    obj.solve_long_walk()
main()






