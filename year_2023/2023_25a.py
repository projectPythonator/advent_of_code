# from sys import stdin
import heapq
import math
import re
from sys import setrecursionlimit

INF = 2 ** 31
UNVISITED = -1
EXPLORED = -2
VISITED = -3

setrecursionlimit(1000000)

class UnionFind:
    '''
    space O(n) --> N*3 or N*2 for now
    search time α(n) -->  inverse ackerman practically constant
    insert time O(1) -->
    '''

    def __init__(self, n):
        self.parents = list(range(n))
        self.ranks = [0] * n  # optional optimzation
        self.sizes = [1] * n  # optional information
        self.num_sets = n  # optional information

    def find_set(self, u):
        u_parent = u
        u_children = []
        while u_parent != self.parents[u_parent]:
            u_children.append(u_parent)
            u_parent = self.parents[u_parent]
        for child in u_children:
            self.parents[child] = u_parent
        return u_parent

    def is_same_set(self, u, v):
        return self.find_set(u) == self.find_set(v)

    def union_set(self, u, v):
        up = self.find_set(u)
        vp = self.find_set(v)
        if up == vp:
            return
        if self.ranks[up] > self.ranks[vp]:
            up, vp = vp, up
        self.parents[up] = vp
        if self.ranks[up] == self.ranks[vp]:
            self.ranks[vp] += 1
        self.sizes[vp] += self.sizes[up]
        #     self.parents[up] = vp
        #     self.sizes[vp] = self.sizes[up]
        # elif self.ranks[vp] < self.ranks[up]:
        #     self.parents[vp] = up
        #     self.sizes[up] = self.sizes[vp]
        # else:
        #     self.parents[vp] = up
        #     self.ranks[up] += 1
        #     self.sizes[up] += self.sizes[vp]
        self.num_sets -= 1

    def size_of_u(self, u):  # optional information
        return self.sizes[self.find_set(u)]

class Snowverload_Solver():

    def __init__(self):
        self.code2ind = {}
        self.ind2code = []
        self.adj_list = []
        self.edge_set = set()
        self.edge_list = []
        self.num_edges = 0
        self.num_nodes = 0

        self.dfs_counter = 0
        self.dfs_root = 0
        self.root_children = 0
        self.parent = []
        self.visited = []
        self.low_values = []
        self.articulation_points = []
        self.bridges = set()

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        for line in self.stdin:
            line = line.strip()
            u, vs = line.split(': ')
            v_set = vs.split(' ')
            for v in v_set:
                self.add_edge_a_b(u, v)
        self.stdin.close()

    def get_index_from_code(self, a):
        if a not in self.code2ind:
            self.code2ind[a] = len(self.ind2code)
            self.ind2code.append(a)
            self.adj_list.append(set())
        return self.code2ind[a]

    def add_edge_a_b(self, a, b):
        u = self.get_index_from_code(a)
        v = self.get_index_from_code(b)
        self.adj_list[u].add(v)
        self.adj_list[v].add(u)
        self.edge_set.add((min(u, v), max(u, v)))

    def add_edge(self, u, v):
        self.adj_list[u].add(v)
        self.adj_list[v].add(u)

    def remove_edge(self, u, v):
        self.adj_list[u].remove(v)
        self.adj_list[v].remove(u)

    def init_data(self):
        self.edge_list = list(self.edge_set)
        self.num_edges = len(self.edge_set)
        self.num_nodes = len(self.adj_list)

    def init_structures(self):
        self.dfs_counter = 0
        self.dfs_root = 0
        self.root_children = 0

        self.parent = [-1] * self.num_nodes
        self.visited = [UNVISITED]*self.num_nodes
        self.low_values = [0] * self.num_nodes
        # self.articulation_points = [0] * self.num_nodes
        self.bridges = set()



    def dfs_articulation_point_and_bridge_helper(self, u):
        # need to rego over this and test it *** not as confident as the other code atm since have not really
        # used it to solve a problem
        self.visited[u] = self.dfs_counter
        self.low_values[u] = self.visited[u]
        self.dfs_counter += 1
        for v in self.adj_list[u]:
            if self.visited[v] == UNVISITED:
                self.parent[v] = u
                if u == self.dfs_root:
                    self.root_children += 1
                self.dfs_articulation_point_and_bridge_helper(v)
                # if self.low_values[v] >= self.visited[u]:
                #     self.articulation_points[u] = 1
                if self.low_values[v] > self.visited[u]:
                    print("found {} {} coded {} {}".format(u, v, self.ind2code[u], self.ind2code[v]))
                    self.bridges.add((min(u, v), max(u, v)))
                self.low_values[u] = min(self.low_values[u], self.low_values[v])
            elif v != self.parent[u]:
                self.low_values[u] = min(self.low_values[u], self.visited[v])

    def dfs_articulation_point_and_bridge(self):
        self.init_structures()
        self.dfs_counter = 0
        for u in range(self.num_nodes):
            if self.visited[u] == UNVISITED:
                self.dfs_root = u
                self.root_children = 0
                self.dfs_articulation_point_and_bridge_helper(u)
                # self.articulation_points[self.dfs_root] = (self.root_children > 1)

    def solve_snowverload_helper(self):
        test = []
        for i in range(521, self.num_edges):
            print(i)
            a = self.edge_list[i]
            seen = 0
            self.remove_edge(a[0], a[1])
            for j in range(i+1, self.num_edges):
                b = self.edge_list[j]
                # self.edge_set.remove(b)
                # union_find = UnionFind(self.num_nodes)
                # for k, (u, v) in enumerate(self.edge_list):
                #     if k == i or k == j:
                #         continue
                #     union_find.union_set(u, v)
                # if union_find.num_sets == 1:
                #     seen += 1
                self.remove_edge(b[0], b[1])
                self.dfs_articulation_point_and_bridge()
                if len(self.bridges) >= 1:
                    ans = list(self.bridges)
                    r_ans = i, j, self.edge_list.index(ans[0])
                    self.add_edge(b[0], b[1])
                    self.add_edge(a[0], a[1])
                    return r_ans
                self.add_edge(b[0], b[1])
            # if seen!=self.num_edges-i-1:
            #     print("error {} {}".format(i, seen))
            #     self.edge_set.add(b)
            # self.edge_set.add(a)
            test.append(seen)
            self.add_edge(a[0], a[1])
        return None, None, None

    def solve_snowverload(self):
        a,b,c =  self.solve_snowverload_helper()
        if a is not None and b is not None and c is not None:
            u1, v1 = self.edge_list[a]
            u2, v2 = self.edge_list[b]
            u3, v3 = self.edge_list[c]
            print("found {} {} coded {} {}".format(u1, v1, self.ind2code[u1], self.ind2code[v1]))
            print("found {} {} coded {} {}".format(u2, v2, self.ind2code[u2], self.ind2code[v2]))
            print("found {} {} coded {} {}".format(u3, v3, self.ind2code[u3], self.ind2code[v3]))

            union_find = UnionFind(self.num_nodes)
            for i, (u, v) in enumerate(self.edge_list):
                if i == a or i == b or i == c:
                    continue
                union_find.union_set(u, v)
            size1, size2 = union_find.size_of_u(u1), union_find.size_of_u(v1)
            print(union_find.num_sets)
            print(size1, size2, size1*size2)
        else:
            print('didnt find 3 edges via method used')


def main():
    obj = Snowverload_Solver()
    obj.read_inputs()
    obj.init_data()
    obj.solve_snowverload()
main()






