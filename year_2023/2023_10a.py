#from sys import stdin
from collections import deque

class Maze_Solver():
    def __init__(self):
        self.grid = []
        self.start_node = (0,0)
        self.key_mapping = {
            '|':[(1,0),(-1,0)],
            '-': [(0,-1),(0,1)],
            'L': [(-1,0),(0,1)],
            'J': [(-1,0),(0,-1)],
            '7': [(1,0),(0,-1)],
            'F': [(1,0),(0,1)],
            '.': [],
            'S': []
        }

        self.possible = {
            (-1,0): set(list('|7F')),
            (1, 0): set(list('|LJ')),
            (0, 1): set(list('-7J')),
            (0,-1): set(list('-LF'))
        }

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        for line in self.stdin:
            self.grid.append(list(line.strip()))

    def get_start_cord(self):
        for i,el in enumerate(self.grid):
            for j,val in enumerate(el):
                if val=='S':
                    return (i,j)

    def init_start(self):
        self.start_node = self.get_start_cord()
        r_queue = []
        s_r,s_c = self.start_node
        for r,c in [(-1,0),(1,0),(0,1),(0,-1)]:
            if self.grid[r+s_r][c+s_c] in self.possible[(r,c)]:
                r_queue.append((r+s_r, c+s_c))
        return r_queue

    def fill_data(self):
        self.connected = self.init_start()

    def solve_maze_helper(self, start):
        q = deque()
        q.append(start)
        self.dst[start] = 1
        while q:
            u = q.popleft()
            r,c=u
            if r ==0 or c==0 or r==len(self.grid)-1 or c==len(self.grid)-1:
                print("edge touched")
                print(self.grid[r][c])
                print(r,c)
            for v in self.key_mapping[self.grid[r][c]]:
                r2,c2 = v[0]+r,v[1]+c
                if self.dst[(r2,c2)] > self.dst[u]+1:
                    self.dst[(r2,c2)] = self.dst[u]+1
                    q.append((r2,c2))

    def solve_maze(self):
        self.dst = {}
        for i,el in enumerate(self.grid):
            for j,val in enumerate(el):
                self.dst[(i,j)] = 2**63
        ans = 0
        self.dst[self.start_node] = 0
        for node in self.connected:
            self.solve_maze_helper(node)
        for val in self.dst.values():
            if val < 2**63:
                ans = max(ans, val)
        print("here")
        print(ans)


def main():
    obj = Maze_Solver()
    obj.read_inputs()
    obj.fill_data()
    obj.solve_maze()


main()

    
    