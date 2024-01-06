#from sys import stdin
from collections import Counter
import re

from math import lcm

class Haunted_Solver():
    def __init__(self):
        self.pattern = []
        self.zipped_lr_jumps = [-1]*2048
        self.mapper = {}
        self.anti_mapper = {}
        self.mem = [-1] * 1024
        self.goal_positions = {}
        self.goal = set()
        self.start = set()

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        self.pattern = [0 if c == 'L' else 1 for c in list(self.stdin.readline().strip())]
        self.stdin.readline().strip()
        ind = 0
        for line in self.stdin:
            line = line.strip()
            tmp = list(line)
            for i in [4,6,10,15]:
                tmp[i] = ' '
            line = ''.join(tmp)
            line = re.sub(" +", " ", line)
            line = line.strip()
            slr = list(line.split(' '))
            for el in slr:
                if el not in self.mapper:
                    self.mapper[el] = ind
                    self.anti_mapper[ind] = el
                    ind += 1
            v = self.mapper[slr[0]]
            self.zipped_lr_jumps[2*v] = self.mapper[slr[1]]
            self.zipped_lr_jumps[2*v+1] = self.mapper[slr[2]]
        self.stdin.close()

    def advance_one_step(self, position, pattern):
        return self.zipped_lr_jumps[2*position+pattern]

    def fill_goal(self):
        for k,v in self.mapper.items():
            if k[2]=='Z':
                self.goal.add(v)

    def fill_start(self):
        for k,v in self.mapper.items():
            if k[2]=='A':
                self.start.add(v)

    def fill_mem(self):
        for k, v in self.mapper.items():
            self.goal_positions[v] = []
            pos = v
            ind = 0
            for ind, c in enumerate(self.pattern):
                if pos in self.goal:
                    self.goal_positions[v].append(ind)
                pos = self.advance_one_step(pos, c)
                ind += 1
            if pos in self.goal:
                self.goal_positions[v].append(ind)
            self.mem[v] = pos

    def fill_data(self):
        self.fill_goal()
        self.fill_start()
        self.fill_mem()

    def solve_graph_helper(self, beg):
        pos = beg
        mem_stk = []
        seen = set()
        while True:
            if pos in seen:
                break
            mem_stk.append(pos)
            seen.add(pos)
            pos = self.mem[pos]
        r_stk = [mem_stk[i] for i in range(mem_stk.index(pos), len(mem_stk))]
        print("listing the index the loop starts at")
        print(len(r_stk),len(mem_stk))

        return [mem_stk[i] for i in range(mem_stk.index(pos), len(mem_stk))]

    def solve_graph(self):
        """
        print(self.dst[:7])
        print(self.mem[:7])
        print(self.left_jumps[:7])
        print(self.right_jumps[:7])"""
        #print(self.pattern)
        ans = []
        for el in self.start:
            res = self.solve_graph_helper(el)
            #print("list of res")
            ans.append(len(res)*271)
            #print(len(res))
            '''
                for i in res:
                    if len(self.goal_positions[i])>0:
                        print("val {} code {}".format(i, self.anti_mapper[i]))
                        print("values of the zs hit {}".format(self.goal_positions[i]))
            '''
        print(ans)
        print(lcm(*ans))

def main():
    obj = Haunted_Solver()
    obj.read_inputs()
    obj.fill_data()
    obj.solve_graph()


main()

    
    