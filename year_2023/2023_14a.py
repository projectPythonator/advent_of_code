# from sys import stdin
from collections import deque


class Reflector_Solver():
    def __init__(self):
        self.grid = []
        self.load_level = []

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        m = 0
        cas = []
        for i, line in enumerate(self.stdin):
            line = line.strip()
            if len(line) == 0:
                continue
            self.grid.append(list(line))
        self.load_level = [i + 1 for i in range(len(self.grid))]
        self.load_level = self.load_level[::-1]

    def init_data(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 'O':
                    a = i-1
                    while a >= 0 and self.grid[a][j] == '.':
                        a -= 1

                    self.grid[i][j] = '.'
                    self.grid[a+1][j] = 'O'
        for i in range(len(self.grid)):
            print(''.join(self.grid[i]))


    def solve_reflection_helper(self):
        ans = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 'O':
                    ans += self.load_level[i]
        return ans

    def solve_reflection(self):
        print(self.solve_reflection_helper())


def main():
    obj = Reflector_Solver()
    obj.read_inputs()
    obj.init_data()
    obj.solve_reflection()


main()