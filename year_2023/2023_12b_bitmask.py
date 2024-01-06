# from sys import stdin
from collections import deque
import re
import bisect
import cProfile
from functools import cache
from sys import setrecursionlimit


setrecursionlimit(1000000)

class Spring_Solver():
    def __init__(self):
        self.schematics = []
        self.springs = []
        self.current_springs = []
        self.current_schematic = ''
        self.current_operational = []
        self.current_damaged = []
        self.set_operational = set()
        self.set_damaged = set()
        self.len_goal = 0
        self.dp_array = []
        self.goal = 0

        self.amt_left = []

    def is_valid_placed_for_length(self, pos, length):
        return pos+length <= len(self.current_schematic)

    def is_valid_placed_for_damaged(self, pos, length):
        return pos+length not in self.set_damaged

    def is_valid_placed_for_operational(self, pos, length):
        for i in range(pos, pos+length):
            if i in self.set_operational:
                return False
        return True

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        m = 0
        for i, line in enumerate(self.stdin):
            a, b = line.strip().split(' ')
            self.schematics.append(a.strip())
            self.springs.append(list(map(int, b.split(','))))
        self.stdin.close()

    def init_schematics(self, modifier):
        for i in range(len(self.schematics)):
            tmp_str = '?'.join([self.schematics[i] for _ in range(modifier)])
            tmp_str = ''.join([' ' if c == '.' else c for c in tmp_str])
            tmp_str = re.sub(" +", " ", tmp_str)
            tmp_str = ''.join(['.' if c == ' ' else c for c in tmp_str])
            if tmp_str[0] == '.':
                tmp_str = tmp_str[1:]
            if tmp_str[-1] == '.':
                tmp_str = tmp_str[:-1]
            self.schematics[i] = tmp_str

    def init_springs(self, modifier):
        for i in range(len(self.springs)):
            leno = len(self.springs[i])
            tmp = [0] * (leno * modifier)
            for j in range(leno):
                for k in range(modifier):
                    tmp[k * leno + j] = self.springs[i][j]
            self.springs[i] = [el for el in tmp]

    def init_data(self):
        modifier = 5
        self.init_schematics(modifier)
        self.init_springs(modifier)

    def init_constants_case_n(self, n):
        self.goal = len(self.springs[n])
        self.len_goal = len(self.schematics[n])

    def init_current_damaged_for_case_n(self, n):
        self.current_damaged = [i for i in range(len(self.schematics[n])) if self.schematics[n][i] == '#']
        self.set_damaged = set(self.current_damaged)

    def init_current_operational_for_case_n(self, n):
        self.current_operational = [i for i in range(len(self.schematics[n])) if self.schematics[n][i] == '.']
        self.set_operational = set(self.current_operational)

    def init_current_springs_for_case_n(self, n):
        self.current_springs = [el for el in self.springs[n]]
        self.current_schematic = self.schematics[n]

    def init_dp_array_case_n(self, n):
        self.dp_array = [[-1 for _ in range(len(self.schematics[n])+1)] for _ in range(len(self.springs[n])+1)]

    def init_amt_left(self):
        self.amt_left = [el for el in self.current_springs]
        for i in range(self.goal-2, -1, -1):
            self.amt_left[i] += (self.amt_left[i+1]+1)

    def init_for_case_n(self, n):
        self.init_current_damaged_for_case_n(n)
        self.init_current_operational_for_case_n(n)
        self.init_current_springs_for_case_n(n)
        self.init_dp_array_case_n(n)
        self.init_constants_case_n(n)
        self.init_amt_left()

    def dynamic_programming(self, schematic_pos, cur_spring):
        if cur_spring == self.goal: # reached the end
            self.dp_array[cur_spring][schematic_pos] = 1 if len(self.current_damaged)==0 or schematic_pos>self.current_damaged[-1] else 0
            return self.dp_array[cur_spring][schematic_pos]
        cur_pos = schematic_pos
        while cur_pos<self.len_goal and self.current_schematic[cur_pos] == '.':
            cur_pos += 1
        cur_len = self.current_springs[cur_spring]
        if self.dp_array[cur_spring][cur_pos] != -1: # already seen
            return self.dp_array[cur_spring][cur_pos]
        if cur_pos+self.amt_left[cur_spring] > self.len_goal: # we don't have enough space left
            self.dp_array[cur_spring][cur_pos] = 0
            return 0
        can_place_via_ops = self.is_valid_placed_for_operational(cur_pos, cur_len)
        if cur_len+cur_pos == self.len_goal:
            self.dp_array[cur_spring][cur_pos] = 1 if can_place_via_ops else 0
            return self.dp_array[cur_spring][cur_pos]
        can_place_via_dmg = self.is_valid_placed_for_damaged(cur_pos, cur_len)
        if self.current_schematic[cur_pos] == '#':
            self.dp_array[cur_spring][cur_pos] = self.dynamic_programming(cur_pos+cur_len+1, cur_spring+1) \
                if can_place_via_dmg and can_place_via_ops else 0
            return self.dp_array[cur_spring][cur_pos]
        if can_place_via_ops and can_place_via_dmg:
            self.dp_array[cur_spring][cur_pos] = (self.dynamic_programming(cur_pos+cur_len+1, cur_spring+1) +
                                                   self.dynamic_programming(cur_pos+1, cur_spring))
        else:
            self.dp_array[cur_spring][cur_pos] = self.dynamic_programming(cur_pos + 1, cur_spring)
        return self.dp_array[cur_spring][cur_pos]

    def solve_springs_helper(self, n):
        return self.dynamic_programming(0, 0)

    def solve_springs(self):
        ans = 0
        for i in range(len(self.springs)):
            print(i)
            self.init_for_case_n(i)
            ans += self.solve_springs_helper(i)
        print("ans is {}".format(ans))



def test_func():
    obj = Spring_Solver()
    obj.read_inputs()
    obj.init_data()
    obj.solve_springs()

def main():
    cProfile.run('test_func()')


main()


