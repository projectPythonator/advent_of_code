# from sys import stdin
import heapq
from collections import deque
from sys import setrecursionlimit
import math

import sys
from numbers import Number
from collections import deque
from collections.abc import Set, Mapping


ZERO_DEPTH_BASES = (str, bytes, Number, range, bytearray)


def getsize(obj_0):
    """Recursively iterate to sum size of object & members."""
    _seen_ids = set()
    def inner(obj):
        obj_id = id(obj)
        if obj_id in _seen_ids:
            return 0
        _seen_ids.add(obj_id)
        size = sys.getsizeof(obj)
        if isinstance(obj, ZERO_DEPTH_BASES):
            pass # bypass remaining control flow and return
        elif isinstance(obj, (tuple, list, Set, deque)):
            size += sum(inner(i) for i in obj)
        elif isinstance(obj, Mapping) or hasattr(obj, 'items'):
            size += sum(inner(k) + inner(v) for k, v in getattr(obj, 'items')())
        # Check for custom object instances - may subclass above too
        if hasattr(obj, '__dict__'):
            size += inner(vars(obj))
        if hasattr(obj, '__slots__'): # can have __slots__ with __dict__
            size += sum(inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s))
        return size
    return inner(obj_0)

class Pulse_Solver():
    def __init__(self):
        self.cycle_begin_index = None
        self.cycle = None
        self.counts = None
        self.beg_inds = None
        self.state_mapping = None
        self.needed = None
        self.begin_value = None
        self.iterations = None
        self.circle_queue = []
        self.write_idx = 0
        self.read_idx = 0
        self.queue_size = 1024

        self.adj_dict = {}
        self.adj_list = []  # will be list of lists [[] [] for _ in range(V)] were left list is low pulse right is high
        self.code2index = {}
        self.index2code = []

        self.conjunction_masks = []  # i is last pulse mask i+1 is low pulse send mask
        self.flip_flop_mask = 0
        self.flip_flop_state = 0
        self.visited = 0

        self.goal = 0
        self.sink = 0

        self.num_paths_hit_goal = 0
        self.num_paths_total = 0
        self.num_visits = 0
        self.num_loops = 0

    @staticmethod
    def get_bit(val, n):
        return val & (1 << n)

    @staticmethod
    def get_normalized_bit(val, n):
        return (val >> n) & 1

    @staticmethod
    def set_bit(val, n):
        return val | (1 << n)

    @staticmethod
    def clear_bit(val, n):
        return val & ~(1 << n)

    @staticmethod
    def toggle_bit(val, n):
        return val ^ (1 << n)

    def push_idx(self):
        self.write_idx = (self.write_idx + 1) % self.queue_size

    def pop_idx(self):
        self.read_idx = (self.read_idx + 1) % self.queue_size

    def add_edge(self, a, b):
        if a not in self.code2index:
            self.code2index[a] = len(self.index2code)
            self.index2code.append(a)
        if b not in self.code2index:
            self.code2index[b] = len(self.index2code)
            self.index2code.append(b)
        u = self.code2index[a]
        v = self.code2index[b]
        if u not in self.adj_dict:
            self.adj_dict[u] = []
        self.adj_dict[u].append(v)

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        for line in self.stdin:
            line = line.strip()
            first_char = line[0]
            if first_char != 'b':
                line = line[1:]
            u, vs = line.split(' -> ')
            for v in vs.split(', '):
                self.add_edge(u, v)
            if first_char == '%':
                self.flip_flop_mask = Pulse_Solver.set_bit(self.flip_flop_mask, self.code2index[u])

    def init_constants(self):
        self.goal = self.code2index['rx']
        self.sink = self.code2index['broadcaster']

    def init_adj_list(self):
        self.adj_list = [[[], []] for _ in range(len(self.index2code))]
        for i in range(len(self.adj_list)):
            if i != self.goal:
                self.adj_list[i][0] = [u for u in self.adj_dict[i]]
                if i != self.sink:
                    self.adj_list[i][1] = [u for u in self.adj_dict[i]
                                           if not Pulse_Solver.get_normalized_bit(self.flip_flop_mask, u)]

    def init_conjunction_masks(self):
        self.conjunction_masks = [0]*(2*len(self.adj_list))
        for i in range(len(self.adj_list)):
            for j in self.adj_list[i][1]:
                if j != self.goal:
                    self.conjunction_masks[2*j+1] = Pulse_Solver.set_bit(self.conjunction_masks[2*j+1], i)

    def init_circle_queue(self):
        self.circle_queue = [None]*self.queue_size

    def init_data(self):
        self.init_constants()
        self.init_adj_list()
        self.init_conjunction_masks()
        self.init_circle_queue()

    def get_next_pulse(self, pulse, oput, iput):
        if Pulse_Solver.get_normalized_bit(self.flip_flop_mask, oput):
            self.flip_flop_state = Pulse_Solver.toggle_bit(self.flip_flop_state, oput)
            return Pulse_Solver.get_normalized_bit(self.flip_flop_state, oput)
        else:
            if pulse:
                self.conjunction_masks[2 * oput] = Pulse_Solver.set_bit(self.conjunction_masks[2 * oput], iput)
                return self.conjunction_masks[2*oput] != self.conjunction_masks[2*oput+1]
            else:
                self.conjunction_masks[2 * oput] = Pulse_Solver.clear_bit(self.conjunction_masks[2 * oput], iput)
                return True

    def load_broadcaster(self):
        for u in self.adj_list[self.sink][0]:
            self.circle_queue[self.write_idx] = False, u, self.sink
            self.push_idx()

    def solve_pulse_helper(self, num):
        self.visited = 0
        self.write_idx = 0
        self.read_idx = 0
        self.load_broadcaster()
        while self.read_idx != self.write_idx:
            pulse, oput, iput = self.circle_queue[self.read_idx]
            self.pop_idx()
            self.last_sent[iput] = pulse or self.last_sent[iput]
            self.visited = Pulse_Solver.set_bit(self.visited, oput)
            if oput == self.goal:
                if pulse:
                    continue
                else:
                    return True
            next_pulse = self.get_next_pulse(pulse, oput, iput)
            idx = 0 if not next_pulse else 1
            for v in self.adj_list[oput][idx]:
                self.circle_queue[self.write_idx] = next_pulse, v, oput
                self.push_idx()
        return False

    def gen_dependancy(self):
        ans = []
        q = deque()
        q.append(([self.goal], self.goal, 0))
        while q:
            path, u, d = q.popleft()
            if d==3:
                ans.append((path, self.index2code[u], u, d))
                continue
            for k, vs in self.adj_dict.items():
                if u in vs:
                    path.append(k)
                    q.append(([el for el in path], k, d+1))
                    path.pop()
        ans.sort()
        p = []
        for el in ans:
            print(el)
            p.append(el[2])
        print(len(ans))
        p.sort()
        print("[{}]".format(','.join(map(str, p))))

    def print_info(self, i):
        print("cycles done  {:12} flipflop state {} visited {}".format(i + 1,
                                                                       ''.join(['#' if Pulse_Solver.get_normalized_bit(
                                                                           self.flip_flop_state, j) else '.' for j in
                                                                                self.needed]),
                                                                       ''.join(['#' if Pulse_Solver.get_normalized_bit(
                                                                           self.visited, j) else '.' for j in
                                                                                range(64)])))

    def init_begins(self):
        self.beg_inds = [0]*len(self.needed)
        for i, k in enumerate(self.needed):
            for j in range(self.begin_value, self.iterations):
                if self.state_mapping[i][j]:
                    self.beg_inds[i] = j
                    break

    def init_counts(self):
        self.counts = [[] for _ in range(len(self.needed))]
        for i, k in enumerate(self.needed):
            state = True
            amt = 0
            for j in range(self.beg_inds[i], self.iterations):
                if state != self.state_mapping[i][j]:
                    state = self.state_mapping[i][j]
                    self.counts[i].append(amt)
                    amt = 1
                else:
                    amt += 1
            self.counts[i].append(amt)
        for j, el in enumerate(self.counts):
            tmp_set = set(el[:-1])
            tmp = [0]*20
            for i in range(20):
                tmp[i] = el[i]
            print("i {:3} len is {:10} arr is {} set is {}".format(j, len(el), ','.join(map(str, tmp)), ','.join(map(str, tmp_set))))
        for i in range(4):
            print()

    def get_actual_cycle(self):
        pow_2 = set([2**n for n in range(2, 16)])
        self.cycle = [[] for _ in range(len(self.needed))]
        self.cycle_begin_index = [0]*len(self.needed)
        for i in range(len(self.needed)):
            ind = 0
            for k, j in enumerate(self.counts[i]):
                if k < 2:
                    continue
                if j != self.counts[i][k-1] and j != self.counts[i][k+1]:
                    if k%2!=0:
                        print("error starting from an off block {} {} {}".format(i, k, j))
                    ind = k
                    self.cycle[i].append(j)
                    self.cycle_begin_index[i] = k
                    break
            for j in range(ind+1, len(self.counts[i])):
                if self.counts[i][j] == self.cycle[i][0]:
                    break
                self.cycle[i].append(self.counts[i][j])
        for i in range(len(self.needed)):
            if self.cycle[i][0] == 2:  # 3910, 3916, 3928, 3792
                self.cycle[i][0], self.cycle[i][-1] = self.cycle[i][-1], self.cycle[i][0]
                self.cycle_begin_index[i] += 2
        for k, el in enumerate(self.cycle):
            tmp = [0] * min(50, len(el))
            for i in range(min(50, len(el))):
                tmp[i] = el[i]
            print("i {:3} len of the cycle is {:5} sum len is {:8} first {:4} elements are {}".format(k, len(el), sum(el), len(tmp), ','.join(map(str, tmp))))

    def test_cycles(self):
        for i, el in enumerate(self.cycle):
            leno = len(el)
            for j in range(self.cycle_begin_index[i], len(self.counts), leno):
                for k in range(leno):
                    if self.counts[i][j+k] != el[k]:
                        print("error cycle broken", i, j, k, el[:40])

    def solve_pulse(self):
        self.gen_dependancy()
        self.iterations = 100000
        self.begin_value = 4094
        print("adj_list is {} in nodes".format(len(self.adj_list)))
        print("total number of modules {} ".format(len(self.index2code)))
        print("paths that hit goal {}".format(self.num_paths_hit_goal))
        print("paths total {}".format(self.num_paths_total))
        print("paths that end in loop {}".format(self.num_loops))
        print("number total visits {}".format(self.num_visits))
        # print(len(self.mods))
        ans = 0
        e = 2
        self.needed = [1,2,4,5,7,8,10,13,14,17,18,20,23,26,30,32,33,34,35,37,38,40,41,43,44,46,48,49,54,56,57]
        self.printo = [24, 28, 50, 55]
        self.last_sent = [False]*64
        self.seeno = [[] for _ in range(4)]
        diff = []
        # self.state_mapping = [[False]*self.iterations for _ in range(len(self.needed))]
        print(getsize(self.state_mapping))

        print('starting ')
        for i in range(self.iterations):
            if self.solve_pulse_helper(i):
                print('Goal', i)
            for k, j in enumerate(self.printo):
                if self.last_sent[j]:
                    self.seeno[k].append(i)
                    self.last_sent[j] = False
            if i&e:
                self.print_info(i)
                e *= 2

        for i in range(4):
            diff.append(self.seeno[i][1]-self.seeno[i][0])
            print(diff)
        ans = 1
        for i in range(4):
            ans = math.lcm(ans, diff[i])
        print(ans)
        for i in range(4):
            tmp = [self.seeno[i][j]-self.seeno[i][j-1] for j in range(1, len(self.seeno[i]))]
            print(set(tmp))
        # self.init_begins()
        # self.init_counts()
        # self.get_actual_cycle()
        # self.test_cycles()

        # for k, j in enumerate(needed):
        #     print("ind {:5} val {:5} seen {:10} lens {:10} tally {:20}".format(k, j, ','.join(map(str,seen[k])), ','.join(map(str, lenos[k])), ','.join(map(str, tally[k].items()))))
        # while True:
        #     if ans&e:
        #         print("cycles done  {:20} flipflop state {}".format(ans, ''.join(['#' if Pulse_Solver.get_normalized_bit(self.flip_flop_state, i) else '.' for i in range(64)])))
        #         e *= 2
        #     if self.solve_pulse_helper():
        #         print(ans)
        #         return
        #     ans += 1

        # low = self.ans[False]
        # high = self.ans[True]
        #
        # print("low {} high {} both {} multiply {}".format(low, high, low + high, high * low))


def main():
    obj = Pulse_Solver()
    obj.read_inputs()
    obj.init_data()
    obj.solve_pulse()

    #$print(sum(map(int, list('4115453233542453565373363331'))))
main()






