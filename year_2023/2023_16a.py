# from sys import stdin
from collections import deque
class Light_Solver():
    def __init__(self):
        self.grid = []
        self.drc = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.dir2code = {'N':0, 'E':1, 'S':2, 'W':3}
        self.code2dir = ['N', 'E', 'S', 'W']
        self.mirrors_forward = [1, 0, 3, 2]
        self.mirrors_backward = [3, 2, 1, 0]

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        m = 0
        for line in self.stdin:
            line = line.strip()
            self.grid.append(list(line))
        #print(len(self.grid), len(self.grid[0]))
        #self.print_out_grid()

    def print_out_grid(self):
        for line in self.grid:
            print(''.join(line))

    def bfs(self, s):
        q = deque()
        q.append((s))
        ans = set()
        seen = set()
        while q:
            state = q.popleft()
            d,i,j = state
            if state in seen or i<0 or i>=len(self.grid) or j<0 or j>=len(self.grid):
                continue
            ans.add((i,j))
            seen.add(state)
            typ = self.grid[i][j]
            if typ=='.':
                i += self.drc[d][0]
                j += self.drc[d][1]
                q.append((d,i,j))
            elif typ=='|':
                if d==0 or d==2:
                    i += self.drc[d][0]
                    j += self.drc[d][1]
                    q.append((d, i, j))
                else:
                    a,b=i+self.drc[0][0],j+self.drc[0][1]
                    q.append((0, a, b))
                    a,b=i+self.drc[2][0],j+self.drc[2][1]
                    q.append((2, a, b))
            elif typ=='-':
                if d==1 or d==3:
                    i += self.drc[d][0]
                    j += self.drc[d][1]
                    q.append((d, i, j))
                else:
                    a,b=i+self.drc[1][0],j+self.drc[1][1]
                    q.append((1, a, b))
                    a,b=i+self.drc[3][0],j+self.drc[3][1]
                    q.append((3, a, b))
            else:
                if typ=='/':
                    d = self.mirrors_forward[d]
                    i += self.drc[d][0]
                    j += self.drc[d][1]
                    q.append((d, i, j))
                else:
                    d = self.mirrors_backward[d]
                    i += self.drc[d][0]
                    j += self.drc[d][1]
                    q.append((d, i, j))
        return len(ans)

    def solve_light(self):

        print(self.bfs((1, 0, 0)))


def main():
    obj = Light_Solver()
    obj.read_inputs()
    obj.solve_light()


main()






