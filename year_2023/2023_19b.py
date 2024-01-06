# from sys import stdin
from collections import deque
from sys import setrecursionlimit

cat_to_code = {'x': 0, 'm': 2, 'a': 4, 's': 6}

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
        elif self.condition_type[n]:  #a < b >=
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

    def get_lists(self, n, ranges):
        a = [el for el in ranges]
        b = [el for el in ranges]
        if self.condition_type[n] is None:
            return (a, b)
        elif self.condition_type[n]:
            ind = cat_to_code[self.condition_var[n]]
            a[ind + 1] = min(a[ind + 1], self.condition_val[n])
            b[ind] = max(b[ind], self.condition_val[n])
            return (a, b)
        else:
            ind = cat_to_code[self.condition_var[n]]
            a[ind] = max(a[ind], self.condition_val[n] + 1)
            b[ind + 1] = min(b[ind + 1], self.condition_val[n]+1)
            return (a, b)

    def gen_list_of_nodes(self, ranges, v):
        r_list = []
        tmp = [el for el in ranges]
        for i, el in enumerate(self.condition_dest):
            a, b = self.get_lists(i, tmp)
            r_list.append((el, a))
            tmp = [j for j in b]
        return r_list


class Aplenty_Solver():
    def __init__(self):
        self.workflows = {}
        self.parts = []
        self.overlaps = {}

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

    def get_contained(self, lis):
        ans = set()
        for i, el in enumerate(lis):
            for j in range(0, len(lis)):
                if j==i:
                    continue
                t = 0
                diff = 0
                for k in range(0, 8, 2):
                    if lis[j][k] <= el[k] and el[k+1] <= lis[j][k+1]:
                        t += 1
                    else:
                        diff = k
                if t==4:
                    # print(i, el, lis[j])
                    ans.add((i, j))
        # print(len(ans))
        return ans

    def get_mergable(self, lis):
        ans = set()
        for i, el in enumerate(lis):
            for j in range(i+1, len(lis)):
                t = 0
                diff = 0
                for k in range(0, 8, 2):
                    if lis[j][k] == el[k] and el[k+1] == lis[j][k+1]:
                        t += 1
                    else:
                        diff = k
                if t==3:
                    if lis[j][diff] == el[diff+1] or lis[j][diff+1] == el[diff]:
                        # print(i, el, lis[j])
                        ans.add((i, j))
        # print(len(ans))
        return ans

    def merge(self, lis, mergables):
        exclude = set()
        for a,b in mergables:
            exclude.add(a)
            exclude.add(b)
        r_list = [el for i,el in enumerate(lis) if i not in exclude]
        for a,b in mergables:
            c = [0]*8
            for i in range(0, 8, 2):
                c[i] = min(lis[a][i], lis[b][i])
                c[i+1] = max(lis[a][i+1], lis[b][i+1])
            r_list.append(c)
        return r_list

    def get_set_size(self, lis):
        ans = 1
        for k in range(0, 8, 2):
            ans *= (lis[k + 1] - lis[k])
        return ans

    def get_overlaps_2(self, lis, lis2):
        ans = 0
        r_list = []
        for i, uv in enumerate(lis):
            s, el = uv
            for j, al in enumerate(lis2):
                if j<=i or j in s:
                    continue
                count = 0
                for k in range(0, 8, 2):
                    if al[k] <= el[k] < al[k+1] or al[k] < el[k+1] < al[k+1]:
                        count += 1
                if count == 4:
                    c = [0] * 8
                    for k in range(0, 8, 2):
                        c[k] = max(el[k], al[k])
                        c[k + 1] = min(el[k+1], al[k+1])
                    r_list.append((s.union(set([j])), c))
                    ans += 1
        print("triple size is {}".format(ans))
        return r_list

    def get_overlaps_1(self, lis):
        ans = 0
        r_list = []
        for i, el in enumerate(lis):
            for j, al in enumerate(lis):
                if j<=i:
                    continue
                count = 0
                for k in range(0, 8, 2):
                    if al[k] <= el[k] < al[k+1] or al[k] < el[k+1] < al[k+1]:
                        count += 1
                if count == 4:
                    c = [0] * 8
                    for k in range(0, 8, 2):
                        c[k] = max(el[k], al[k])
                        c[k + 1] = min(el[k+1], al[k+1])
                    r_list.append((set([i, j]), c))
                    ans += 1
        print("double size is {}".format(ans))
        return r_list


    def bfs_walk(self, beg):
        q = deque()
        q.append((beg, [1, 4001, 1, 4001, 1, 4001, 1, 4001]))
        sets = list()
        while q:
            v, r = q.popleft()
            if v == 'R':
                continue
            if v == 'A':
                sets.append(r)
                continue
            u_set = self.workflows[v].gen_list_of_nodes(r, v)
            for u, s in u_set:
                works = True
                for i in range(0, 8, 2):
                    if s[i]>=s[i+1]:
                        works=False
                        break
                if works:
                    q.append((u, s))
        print(len(sets))
        tmp = set([tuple(el) for el in sets])
        sets = [list(el) for el in tmp]
        sets.sort()
        # for el in sets:
        #     print(el)
        while True:
            mergables = self.get_mergable(sets)
            if len(mergables)==0:
                break
            mergables = list(mergables)
            mergables.sort()
            # for a,b in mergables:
            #     print(a,b)
            sets = self.merge(sets, mergables)
        # print("len of sets is {}".format(len(sets)))
        while True:
            mergables = self.get_contained(sets)
            if len(mergables) == 0:
                break
            mergables = list(mergables)
            mergables.sort()
            # for a,b in mergables:
            #     print(a,b)
            sets = self.merge(sets, mergables)
        print("len of sets is {}".format(len(sets)))
        sets.sort()
        r_lis = self.get_overlaps_1(sets)
        for el in r_lis:
            print("values {} first set {} second set {}".format(el, sets[list(el[0])[0]], sets[list(el[0])[1]]))
        tmpo = [b for a,b in r_lis]
        r_lis_1 = self.get_overlaps_2(r_lis, sets)
        sumo = 0
        mino = 0
        for i, el in enumerate(sets):
            sumo += self.get_set_size(el)
        for i, el in enumerate(r_lis):
            mino += self.get_set_size(el[1])
        print(sumo-mino)

        for el in r_lis_1:
            print(el)


    def solve_lagoon_helper(self):
        self.bfs_walk('in')

    def solve_aplenty(self):
        ans = 0
        self.solve_lagoon_helper()
        print(ans)


def main():
    obj = Aplenty_Solver()
    obj.read_inputs()
    obj.solve_aplenty()

    #$print(sum(map(int, list('4115453233542453565373363331'))))
main()






