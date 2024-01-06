# from sys import stdin
import heapq
from collections import deque


INF = 0

class Long_Walk_Solver():
    def __init__(self):
        self.grid = []
        self.R_base = 0
        self.C_base = 0
        self.distances = []
        self.drc = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.node_2_index = {}
        self.index_2_node = []
        self.adj_list = []
        self.beg = None
        self.seen = []
        self.longest_path = 0
        self.goal = 0
        self.calls = 0

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        for line in self.stdin:
            line = line.strip()
            a = list(line)
            for i, c in enumerate(a):
                if c != '.' and c != '#':
                    a[i] = '.'
            self.grid.append(a)
        self.stdin.close()

    def get_start(self):
        self.beg = (0, 1)

    def is_intersection(self, i, j):
        amt = 0
        for r, c in self.drc:
            if self.grid[i+r][j+c] == '.':
                amt += 1
        return amt>=3 and self.grid[i][j] == '.'

    def add_new_node(self, i, j):
        self.node_2_index[(i, j)] = len(self.index_2_node)
        self.index_2_node.append((i, j))
        self.adj_list.append({})

    def add_adj_list_u_2_v(self, u, v, d):
        if u == v:
            print('ERROR {}  {} is a self loop'.format(u, v))
            return
        if v in self.adj_list[u]:
            self.adj_list[u][v] = max(self.adj_list[u][v], d)
        else:
            self.adj_list[u][v] = d

    def fill_adj_list_for_n(self, n, node_start):
        q = deque()
        q.append((1, node_start))
        seen = set()
        seen.add(self.index_2_node[n])
        while True:
            # print(q, n, node_start)
            d, u = q.popleft()
            if u in self.node_2_index:
                self.add_adj_list_u_2_v(n, self.node_2_index[u], d)
                break
            seen.add(u)
            i, j = u
            for r, c in self.drc:
                a, b = i+r, j+c
                if self.grid[a][b] == '.' and (a, b) not in seen:
                    q.append((d+1, (a, b)))

    def fill_edge_dist_n(self, n):
        a, b = self.index_2_node[n]
        for r, c in self.drc:
            i, j = a+r, b+c
            if 0 <= i < self.R_base and 0 <= j < self.C_base and self.grid[i][j]=='.':
                self.fill_adj_list_for_n(n, (i, j))

    def handle_all_nodes_dist(self):
        for i in range(len(self.index_2_node)):
            self.fill_edge_dist_n(i)

    def init_data(self):
        self.R_base = len(self.grid)
        self.C_base = len(self.grid[0])
        self.add_new_node(0, 1)
        for i in range(1, self.R_base-1):
            for j in range(1, self.C_base-1):
                if self.is_intersection(i, j):
                    self.add_new_node(i, j)
        self.add_new_node(self.R_base-1, self.C_base-2)
        self.handle_all_nodes_dist()
        # for i, el in enumerate(self.index_2_node):
        #     print("node {} is {} below is the adj list".format(i, el))
        #     for k, v in self.adj_list[i].items():
        #         print("distance from {} to {} is {}".format(i, k, v))

    def dfs(self, d, u):
        if u == self.goal:
            self.longest_path = max(self.longest_path, d)
        else:
            for k, v in self.adj_list[u].items():
                if not self.seen[k]:
                    self.seen[k] = True
                    self.dfs(d+v, k)
                    self.seen[k] = False

    def solve_long_walk_helper(self):
        self.seen = [False]*len(self.index_2_node)
        self.goal = len(self.seen)-1
        self.seen[0] = True
        self.dfs(0, 0)

    def solve_long_walk(self):
        self.solve_long_walk_helper()
        print(self.longest_path, self.calls)


def main():
    obj = Long_Walk_Solver()
    obj.read_inputs()
    obj.init_data()
    obj.solve_long_walk()
main()






