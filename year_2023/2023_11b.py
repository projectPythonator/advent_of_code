# from sys import stdin
from collections import deque


class Galaxy_Solver():
    def __init__(self):
        self.grid = []
        self.aug_grid = []
        self.coords = []

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        for i, line in enumerate(self.stdin):
            line = line.strip()
            self.grid.append(list(line))

    def init_aug_grid(self):
        self.aug_grid = [['.' for _ in range(2 * len(self.grid)) for _ in range(2 * len(self.grid))]]
        row_empty = [True] * len(self.grid)
        col_empty = [True] * len(self.grid)

        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.grid[i][j] == '#':
                    row_empty[i] = False
                    col_empty[j] = False
        push_down = set()
        print(self.grid)
        for i in range(len(self.grid)):
            push_right = set()
            for j in range(len(self.grid)):
                if row_empty[i]:
                    push_down.add(i)
                if col_empty[j]:
                    push_right.add(j)
                if self.grid[i][j] == '#':
                    self.coords.append((i + len(push_down) * 999999, j + len(push_right) * 999999,))

    def get_dst(self, a1, b1, a2, b2):
        return abs(a1 - a2) + abs(b1 - b2)

    def solve_galaxy_helper(self):
        ans = 0
        print(self.coords)
        for i in range(len(self.coords)):
            for j in range(i + 1, len(self.coords)):
                ans += self.get_dst(self.coords[i][0], self.coords[i][1], self.coords[j][0], self.coords[j][1])
        return ans

    def solve_galaxy(self):
        print(self.solve_galaxy_helper())


def main():
    obj = Galaxy_Solver()
    obj.read_inputs()
    obj.init_aug_grid()
    obj.solve_galaxy()


main()


