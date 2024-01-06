#from sys import stdin
from collections import Counter
import re
'''
class Haunted_Solver():
    def __init__(self):
        self.pattern = []
        self.left_jumps = [-1]*1024
        self.right_jumps = [-1]*1024
        self.mapper = {}
        self.mem = [-1]*1024
        self.dst = [-1]*1024
        self.goal = -1
        
    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        self.pattern = [True if c=='L' else False for c in list(self.stdin.readline().strip())]
        self.stdin.readline().strip()
        ind = 0
        for line in self.stdin:
            line = line.strip()
            tmp = list(line)
            tmp[4] = ' '
            tmp[6] = ' '
            tmp[10] = ' '
            tmp[15] = ' '
            line = ''.join(tmp)
            line = re.sub(" +", " ", line)
            line = line.strip()
            slr = list(line.split(' '))
            for el in slr:
                if el not in self.mapper:
                    self.mapper[el] = ind
                    ind += 1
            self.left_jumps[self.mapper[slr[0]]] = self.mapper[slr[1]]
            self.right_jumps[self.mapper[slr[0]]] = self.mapper[slr[2]]
        self.stdin.close()
        self.goal = self.mapper['ZZZ']

    def fill_mem(self):
        print(self.right_jumps[self.mapper['LDS']])
        for k,v in self.mapper.items():
            pos = v
            ind = 0
            for c in self.pattern:
                if pos == self.goal:
                    print("her")
                    print(pos)
                    print(v)
                    print(k)
                    break
                if c:
                    pos = self.left_jumps[pos]
                else:
                    pos = self.right_jumps[pos]
                ind += 1
            if pos == self.goal:
                print("her")
                print(pos)
                print(ind)
                print(v)
                print(k)
            self.mem[v] = pos
            self.dst[v] = ind
    
    def solve_graph_helper(self):
        pos = self.mapper['AAA']
        ans = 0

        test = set()
        while True:
            if pos == self.goal:
                return ans
            if pos in test:
                print("loop error")
                print(pos)
                print(test)
                return
            test.add(pos)
            ans += self.dst[pos]
            pos = self.mem[pos]


    def solve_graph(self):
        """
        print(self.dst[:7])
        print(self.mem[:7])
        print(self.left_jumps[:7])
        print(self.right_jumps[:7])"""
        print(self.pattern)
        print(self.solve_graph_helper())

def main():
    obj = Haunted_Solver()
    obj.read_inputs()
    obj.fill_mem()
    obj.solve_graph()
main()
'''

class Haunted_Solver():
    def __init__(self):
        self.pattern = []
        self.zipped_lr_jumps = [-1]*2048
        self.mapper = {}
        self.mem = [-1] * 1024
        self.dst = [-1] * 1024
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
                    ind += 1
            v = self.mapper[slr[0]]
            self.zipped_lr_jumps[2*v] = self.mapper[slr[1]]
            self.zipped_lr_jumps[2*v+1] = self.mapper[slr[2]]
        self.stdin.close()

    def advance_one_step(self, position, pattern):
        return self.zipped_lr_jumps[2*position+pattern]

    def fill_goal(self):
        self.goal.add(self.mapper['ZZZ'])

    def fill_start(self):
        self.start.add(self.mapper['AAA'])

    def fill_mem(self):
        for k, v in self.mapper.items():
            pos = v
            ind = 0
            for c in self.pattern:
                if pos in self.goal:
                    break
                pos = self.advance_one_step(pos, c)
                ind += 1
            if pos in self.goal:
                print("here")
                print(pos)
                print(ind)
                print(v)
                print(k)
            self.mem[v] = pos
            self.dst[v] = ind

    def fill_data(self):
        self.fill_goal()
        self.fill_start()
        self.fill_mem()

    def solve_graph_helper(self):
        pos = list(self.start)[0]
        #print(pos)
        ans = 0
        while True:
            if pos in self.goal:
                return ans
            ans += self.dst[pos]
            pos = self.mem[pos]

    def solve_graph(self):
        """
        print(self.dst[:7])
        print(self.mem[:7])
        print(self.left_jumps[:7])
        print(self.right_jumps[:7])"""
        #print(self.pattern)
        print(self.solve_graph_helper())


def main():
    obj = Haunted_Solver()
    obj.read_inputs()
    obj.fill_data()
    obj.solve_graph()


main()

    
    