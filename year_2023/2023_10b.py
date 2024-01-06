#from sys import stdin
from collections import deque

DIRS = ['N','E','S','W']

# N E outer bend are True S W and inner bend are False
MAPPING = {
    '-': {False: [(-1, 0)],True:[(1, 0)]},
    '|': {True: [(0, -1)],False:[(0, 1)]},
    '7': {False: [(-1, 0), (-1, 1), (0, 1)], True:[(1, -1)]},
    'J': {False: [(1, 0), (1, 1), (0, 1)], True:[(-1, -1)]},
    'L': {False: [(1, 0), (1, -1), (0, -1)], True:[(-1, 1)]},
    'F': {False: [(-1, 0), (-1, -1), (0, -1)], True:[(1, 1)]},
}


class Maze_Solver():
    def __init__(self):
        self.grid = []
        self.list_path = []
        self.list_nodes = []
        self.direction = 'E'

        self.set_path = set()

        self.edge_node = None

        self.corners = {}

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

    def get_first_edge_pipe(self):
        for v,p in self.list_path:
            r,c = p
            if r==0 or c==0:
                self.edge_node = (v,p)
                return

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
            for v in self.key_mapping[self.grid[r][c]]:
                r2,c2 = v[0]+r,v[1]+c
                if self.dst[(r2,c2)] > self.dst[u]+1:
                    self.dst[(r2,c2)] = self.dst[u]+1
                    q.append((r2,c2))

    def build_path(self):
        tmp_info = []
        for k,v in self.dst.items():
            if v < 2**63:
                tmp_info.append((v, k))
        tmp_info.sort()
        self.list_nodes = [False for el in tmp_info]
        self.list_path = [el for el in tmp_info]

    #N E outer bend are True S W and inner bend are False
    def mark_path(self):
        index = self.edge_node[0]
        beg = index
        while True:
            pip_typ = self.grid[self.list_path[index][1][0]][self.list_path[index][1][1]]
            if self.direction == 'N':
                if pip_typ=='7':
                    self.list_nodes[index] = True
                    self.direction = 'E'
                elif pip_typ=='-':
                    self.list_nodes[index] = True
                elif pip_typ=='F':
                    self.list_nodes[index] = True
                    self.direction = 'W'
                elif pip_typ=='L':
                    self.list_nodes[index] = False
                    self.direction = 'E'
                elif pip_typ=='J':
                    self.list_nodes[index] = False
                    self.direction = 'W'
            elif self.direction == 'E':
                if pip_typ=='7':
                    self.list_nodes[index] = True
                    self.direction = 'N'
                elif pip_typ=='|':
                    self.list_nodes[index] = True
                elif pip_typ=='F':
                    self.list_nodes[index] = False
                    self.direction = 'S'
                elif pip_typ=='L':
                    self.list_nodes[index] = False
                    self.direction = 'N'
                elif pip_typ=='J':
                    self.list_nodes[index] = True
                    self.direction = 'S'
            elif self.direction == 'S':
                if pip_typ=='7':
                    self.list_nodes[index] = False
                    self.direction = 'W'
                elif pip_typ == '-':
                    self.list_nodes[index] = False
                elif pip_typ == 'F':
                    self.list_nodes[index] = False
                    self.direction = 'E'
                elif pip_typ=='L':
                    self.list_nodes[index] = True
                    self.direction = 'W'
                elif pip_typ=='J':
                    self.list_nodes[index] = True
                    self.direction = 'E'
            else:
                if pip_typ=='7':
                    self.list_nodes[index] = False
                    self.direction = 'S'
                elif pip_typ=='|':
                    self.list_nodes[index] = False
                elif pip_typ=='F':
                    self.list_nodes[index] = True
                    self.direction = 'N'
                elif pip_typ=='L':
                    self.list_nodes[index] = True
                    self.direction = 'S'
                elif pip_typ=='J':
                    self.list_nodes[index] = False
                    self.direction = 'N'
            index+=1
            index%=len(self.list_path)
            if index==beg:
                break

    def mark_nodes(self):
        for v,p in self.list_path:
            r,c = p
            pip_typ = self.grid[r][c]
            tf = self.list_nodes[v]
            for rr,cc in MAPPING[pip_typ][tf]:
                rrr,ccc=r+rr,c+cc
                #print(r,c,rr,cc,pip_typ,tf,v)
                if self.grid[rrr][ccc]=='.':
                    self.grid[rrr][ccc] = 'I'

    def floodfill(self, row, col, old, new):
        self.grid[row][col] = new
        for r,c in [(-1,0),(1,0),(0,1),(0,-1)]:
            if self.grid[r+row][c+col]==old:
                self.floodfill(r+row, c+col, old, new)

    def solve_maze(self):
        self.dst = {}
        for i,el in enumerate(self.grid):
            for j,val in enumerate(el):
                self.dst[(i,j)] = 2**63
        ans = 0
        self.dst[self.start_node] = 0
        for node in self.connected:
            self.solve_maze_helper(node)
            break
        self.build_path()
        self.set_path = set([p for v,p in self.list_path])
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if (i,j) not in self.set_path:
                    self.grid[i][j] = '.'
        self.get_first_edge_pipe()
        self.grid[self.start_node[0]][self.start_node[1]] = 'F'
        self.mark_path()
        self.mark_nodes()
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.grid[i][j]=='I':
                    self.floodfill(i,j,'.','I')
        for i,el in enumerate(self.grid):
            for j,v in enumerate(el):
                if v=='I':
                    ans+=1
        print(ans)
        print(self.dst[(0,56)])
        print(self.dst[(0, 55)])


        '''
        print("here")
        print(len(self.dst))
        print(len(self.grid[0]))
        print(len(self.grid))
        print(ans)
        '''

def main():
    obj = Maze_Solver()
    obj.read_inputs()
    obj.fill_data()
    obj.solve_maze()


main()

    
    