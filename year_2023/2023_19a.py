# from sys import stdin
import heapq
from collections import deque
from sys import setrecursionlimit

class Workflow():
    def __init__(self):
        self.name = ''
        self.condition_dest = []
        self.condition_type = []
        self.condition_var = []
        self.condition_val = []

    def init_data(self, line):
        line = line[:-1]
        nam, data = line.split('{')
        self.name = nam
        data = data.split(',')
        for condition in data:
            if ':' not in condition:
                self.condition_val.append(None)
                self.condition_var.append(None)
                self.condition_type.append(None)
                self.condition_dest.append(condition)
            else:
                cond, dest = condition.split(':')
                self.condition_dest.append(dest)
                if '<' in cond:
                    self.condition_type.append(True)
                    var, val = cond.split('<')
                    self.condition_var.append(var)
                    self.condition_val.append(int(val))
                else:
                    self.condition_type.append(False)
                    var, val = cond.split('>')
                    self.condition_var.append(var)
                    self.condition_val.append(int(val))

    def val_less_than_self(self, val, n):
        return val<self.condition_val[n]

    def val_greater_than_self(self, val, n):
        return val>self.condition_val[n]

    def check_condition_n(self, n, val):
        #print("n {} type {} var {} val {}  dest {}".format(n, self.condition_type[n], self.condition_var[n], self.condition_val[n], self.condition_dest[n]))
        if self.condition_type[n] is None:
            return True
        elif self.condition_type[n]:
            return self.val_less_than_self(val, n)
        else:
            return self.val_greater_than_self(val, n)

    def get_next_workplace(self, part_vals):
        #print("entering name {} with values {}".format(self.name, part_vals))
        for i, el in enumerate(self.condition_dest):
            #print("checking i = {} with key {} and value {}".format(i, self.condition_var[i], part_vals[self.condition_var[i]]))
            if self.check_condition_n(i, part_vals[self.condition_var[i]]):
                return el
        print('error')
        return None

class Aplenty_Solver():
    def __init__(self):
        self.workflows = {}
        self.parts = []

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        for line in self.stdin:
            line = line.strip()
            if len(line)==0:
                break
            new_workflow = Workflow()
            new_workflow.init_data(line)
            self.workflows[new_workflow.name] = new_workflow

        for line in self.stdin:
            line = line.strip()
            line = line[1:-1]
            tmp = line.split(',')
            dic = {}
            for val in tmp:
                a,b = val.split('=')
                dic[a] = int(b)
            dic[None] = 0
            self.parts.append(dic)

    def solve_lagoon_helper(self, part):
        wf = 'in'
        while wf!='A' and wf!='R':
            wf = self.workflows[wf].get_next_workplace(part)
        if wf == 'A':
            return sum(part.values())
        else:
            return 0

    def solve_aplenty(self):
        ans = 0
        for part in self.parts:
            ans += self.solve_lagoon_helper(part)
        print(ans)


def main():
    obj = Aplenty_Solver()
    obj.read_inputs()
    obj.solve_aplenty()

    #$print(sum(map(int, list('4115453233542453565373363331'))))
main()






