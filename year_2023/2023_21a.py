# from sys import stdin
import heapq


INF = 2**32

class Step_Solver():
    def __init__(self):
        self.grid = []
        self.R_base = 0
        self.C_base = 0
        self.distances = []
        self.drc = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        for line in self.stdin:
            line = line.strip()
            self.grid.append(list(line))

        self.stdin.close()

    def get_start(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 'S':
                    return (i, j)
        return None

    def init_data(self):
        self.distances = [[INF for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]

    def dijkstras(self):
        beg = self.get_start()
        q = [(0, beg)]
        self.distances[beg[0]][beg[1]] = 0
        self.R = len(self.grid)
        self.C = len(self.grid[0])
        while q:
            d, v = heapq.heappop(q)
            i, j = v
            if d>self.distances[i][j]:
                continue

            for r,c in self.drc:
                a,b=i+r,j+c
                if a < 0 or a >= self.R or b < 0 or b >= self.C:
                    continue
                if self.grid[a][b] == '#':
                    continue
                if self.distances[a][b] > d + 1:
                    self.distances[a][b] = d + 1
                    heapq.heappush(q, (d+1, (a, b)))


    def solve_steps_helper(self, steps):
        self.dijkstras()
        ans = 0
        for i in range(len(self.distances)):
            for j in range(len(self.distances[0])):
                if self.distances[i][j]<=steps and steps%2 == self.distances[i][j]%2:
                    ans += 1
        return ans


    def solve_steps(self):
        print(self.solve_steps_helper(64))


def main():
    obj = Step_Solver()
    obj.read_inputs()
    obj.init_data()
    obj.solve_steps()
main()






