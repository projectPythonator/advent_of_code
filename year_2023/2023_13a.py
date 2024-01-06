#from sys import stdin
from collections import deque

class Mirrors_Solver():
    def __init__(self):
        self.horizonatal = []
        self.vertical = []
        self.patterns = []

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        m = 0
        cas = []
        for i, line in enumerate(self.stdin):
            line = line.strip()
            if len(line)==0:
                self.patterns.append([el for el in cas])
                cas = []
            else:
                cas.append(line)
        self.patterns.append([el for el in cas])
        self.stdin.close()

    def init_data(self, cur):
        self.horizonatal = []
        self.vertical = []
        for i in range(len(cur)):
            num = 0
            for j in range(len(cur[0])):
                if cur[i][j] == '#':
                    num = num|(1<<j)
            self.horizonatal.append(num)

        for i in range(len(cur[0])):
            num = 0
            for j in range(len(cur)):
                if cur[j][i] == '#':
                    num = num | (1 << j)
            self.vertical.append(num)

    def get_info_on_mirror(self, arr):
        last = -1
        amount = 0
        for i in range(1, len(arr)):
            if arr[i]==arr[i-1]:
                a=i
                b=i-1
                while b>=0 and a<len(arr) and arr[a]==arr[b]:
                    b-=1
                    a+=1
                if b<0 or a>=len(arr):
                    amount += 1
                    last = i
        return last, amount


    def solve_mirrors_helper(self, pattern):
        self.init_data(pattern)
        verts = 0
        verts_best = 0
        horis = 0
        horis_best = 0
        v_l, v_a = self.get_info_on_mirror(self.vertical)
        h_l, h_a = self.get_info_on_mirror(self.horizonatal)
        if v_a+h_a==1:
            return v_l if h_l==-1 else h_l*100
        print("ERROR")
        for a in pattern:
            print(a)
        print(self.vertical)
        print(self.horizonatal)
        print()
        return -1

    def solve_mirrors(self):
        ans = 0
        for i, el in enumerate(self.patterns):
            ans += self.solve_mirrors_helper(el)
            #print(ans)
        print(ans)


def main():
    obj = Mirrors_Solver()
    obj.read_inputs()
    obj.solve_mirrors()


main()

    
    