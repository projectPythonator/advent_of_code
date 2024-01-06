# from sys import stdin
from collections import deque


class Reflector_Solver():
    def __init__(self):
        self.grid = []
        self.load_level = []
        self.vertical_runs = []
        self.horizontal_runs = []
        self.levels = []

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        for i, line in enumerate(self.stdin):
            line = line.strip()
            if len(line) == 0:
                continue
            self.grid.append(list(line))
        self.load_level = [i + 1 for i in range(len(self.grid))]
        self.load_level = self.load_level[::-1]

    def init_data(self):
        for j in range(len(self.grid[0])):
            i = 0
            while i<len(self.grid):
                while i<len(self.grid) and self.grid[i][j] == '#':
                    i+=1
                b = i
                while b < len(self.grid) and self.grid[b][j] != '#':
                    b += 1
                if i!=b:
                    self.vertical_runs.append((j, i, b))
                i = b
                i += 1
        for i in range(len(self.grid)):
            j = 0
            while j<len(self.grid[0]):
                while j<len(self.grid[0]) and self.grid[i][j] == '#':
                    j+=1
                b = j
                while b < len(self.grid[0]) and self.grid[i][b] != '#':
                    b += 1
                if j!=b:
                    self.horizontal_runs.append((i, j, b))
                j = b
                j += 1
        # print(self.vertical_runs)
        # print(self.horizontal_runs)
        for i in range(len(self.grid)):
            print(''.join(self.grid[i]))

    def apply_north_tilt(self):
        for j, a, b in self.vertical_runs:
            amt = 0
            for i in range(a, b):
                if self.grid[i][j] == 'O':
                    amt += 1
                self.grid[i][j] = '.'
            for i in range(a, a+amt):
                self.grid[i][j] = 'O'

    def apply_east_tilt(self):
        for i, a, b in self.horizontal_runs:
            amt = 0
            for j in range(a, b):
                if self.grid[i][j] == 'O':
                    amt += 1
                self.grid[i][j] = '.'
            for j in range(b - 1, b - 1 - amt, -1):
                self.grid[i][j] = 'O'

    def apply_south_tilt(self):
        for j, a, b in self.vertical_runs:
            amt = 0
            for i in range(a, b):
                if self.grid[i][j] == 'O':
                    amt += 1
                self.grid[i][j] = '.'
            for i in range(b-1, b-1-amt, -1):
                self.grid[i][j] = 'O'

    def apply_west_tilt(self):
        for i, a, b in self.horizontal_runs:
            amt = 0
            for j in range(a, b):
                if self.grid[i][j] == 'O':
                    amt += 1
                self.grid[i][j] = '.'
            for j in range(a, a+amt):
                self.grid[i][j] = 'O'

    def special_test(self, p, leno):
        b = p
        while b>=0:
            if self.levels[b]!=self.levels[p]:
                return False
            b-=leno
        return True

    def test_loop(self, p, leno):
        if self.levels[p] != self.levels[p-leno] or self.levels[p-leno] != self.levels[p-2*leno]:
            return False
        for i in range(1, leno):
            if self.levels[p]==self.levels[p-i]:
                return False
        for i in range(leno):
            if self.levels[p-i] != self.levels[p - leno - i] or self.levels[p - leno - i] != self.levels[p - 2 * leno - i]:
                return False
        return self.special_test(p, leno)

    def get_candidates(self):
        print("getting candidates")
        self.potential = []
        self.seen = set()
        for i in range(len(self.levels)-1, 5000, -1):
            if self.levels[i] not in self.seen:
                for leno in range(2, 300):
                    if self.test_loop(i, leno):
                        self.seen.add(self.levels[i])
                        self.potential.append(self.levels[i])
                        print(i, leno, self.levels[i])
                        break
        ans = [el for el in self.seen]
        ans.sort()
        print(ans)
        print(len(ans))

    def get_ans(self):
        ans = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 'O':
                    ans += self.load_level[i]
        return ans

    def solve_reflection_helper(self):
        a=2
        amt_a, amt_b = 0, 0
        test = {}
        pos = {}
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 'O':
                    amt_a += 1
        for i in range(9995):
            # if i%a==0:
            #     print(i)
            #     a*=2
            self.apply_north_tilt()
            self.apply_west_tilt()
            self.apply_south_tilt()
            self.apply_east_tilt()
            cur = self.get_ans()
            # if cur==64:
            #     print('hits 64 on {}'.format(i))
            # if cur>99208 and cur<99332:
            #     test.add(cur)
            self.levels.append(cur)
            if cur not in test:
                test[cur] = 1
            else:
                test[cur] += 1
            pos[cur] = i
            #print(i, cur)
        # for el in test:
        #     print(el, test[el], pos[el])
        # print(len(test))
        # bin_search = list(test)
        # bin_search.sort()
        # print(bin_search[len(bin_search)//2])
        self.get_candidates()
        print('ended on '.format(self.get_ans()))
        a = 9995

        for i in range(9995, 1000000000, 102):
            a = i
        for i in range(a, 1000000000):
            self.apply_north_tilt()
            self.apply_west_tilt()
            self.apply_south_tilt()
            self.apply_east_tilt()
        print(self.get_ans())

        # for i in range(len(self.grid)):
        #     print(''.join(self.grid[i]))
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 'O':
                    amt_b += 1
        print(amt_a, amt_b)
        return self.get_ans()


    def solve_reflection(self):
        print(self.solve_reflection_helper())


def main():
    obj = Reflector_Solver()
    obj.read_inputs()
    obj.init_data()
    obj.solve_reflection()


main()