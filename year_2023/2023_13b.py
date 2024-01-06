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
        self.load_level = [i+1 for i in range(len(self.grid))]
        self.load_level = self.load_level[::-1]

    def init_data(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j]=='P'
    def get_info_on_mirror(self, arr, old):
        last = -1
        amount = 0
        leno = 0
        for i in range(1, len(arr)):
            if i==old:
                continue
            if arr[i] == arr[i - 1]:
                a = i
                b = i - 1
                c = 0
                while b >= 0 and a < len(arr) and arr[a] == arr[b]:
                    b -= 1
                    a += 1
                    c += 1
                if b < 0 or a >= len(arr):
                    amount += 1
                    last = i
                    leno = c
        return last, amount, leno

    def solve_cur_mirror(self, info_l, info_r):

        v_l, v_a, v_len = self.get_info_on_mirror(self.vertical, info_r)
        h_l, h_a, h_len = self.get_info_on_mirror(self.horizonatal, info_l)
        if v_a==1:
            return v_l, v_a, False
        else:
            return h_l, h_a, True

    def solve_part_b(self, typ, pos, amt):
        print("typ {} pos {} amt {}".format(typ, pos, amt))
        for i in range(len(self.horizonatal)):
            for j in range(len(self.vertical)):
                self.flip_i_j(i, j)
                new_pos, new_amt, new_typ = self.solve_cur_mirror(pos if typ else -1, pos if not typ else -1)
                if new_amt==1:
                    print(i, j, 100*new_pos if new_typ else new_pos, new_typ, new_pos)
                    return 100*new_pos if new_typ else new_pos
                self.flip_i_j(i, j)


    def solve_reflection_helper(self, pattern):
        self.init_data(pattern)
        pos, amt, typ = self.solve_cur_mirror(-1, -1)
        return self.solve_part_b(typ, pos, amt)
        print("ERROR")
        for a in pattern:
            print(a)
        print(self.vertical)
        print(self.horizonatal)
        print()
        return -1

    def solve_reflection(self):
        ans = 0
        for i, el in enumerate(self.patterns):
            ans += self.solve_mirrors_helper(el)
            # print(ans)
        print(ans)


def main():
    obj = Mirrors_Solver()
    obj.read_inputs()
    obj.solve_mirrors()


main()


