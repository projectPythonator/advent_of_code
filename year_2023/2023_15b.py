# from sys import stdin

class Hash_Solver():
    def __init__(self):
        self.input_strings = []
        self.current_value = 0
        self.HASH = [[] for _ in range(256)]
        self.MAP = [{} for i in range(256)]

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        m = 0
        line = self.stdin.readline().strip()
        self.input_strings = list(line.split(','))
        print(len(self.input_strings))

    def hash_c(self, c):
        tmp = ord(c)
        self.current_value += tmp
        self.current_value *= 17
        self.current_value %= 256

    def solve_hash_helper(self, current):
        self.current_value = 0
        a,b = '', ''
        if current[-1]=='-':
            a, b = current[:-1], ''
        else:
            tmp = current.split('=')
            a = tmp[0]
            b = int(tmp[1])
        for c in a:
            self.hash_c(c)
        if current[-1]=='-':
            if a in self.MAP[self.current_value]:
                self.MAP[self.current_value].pop(a)
                self.HASH[self.current_value].remove(a)
        else:
            if a not in self.MAP[self.current_value]:
                self.HASH[self.current_value].append(a)
                self.MAP[self.current_value][a] = b
            else:
                self.MAP[self.current_value][a] = b


    def solve_hash(self):
        ans = 0
        for el in self.input_strings:
            self.solve_hash_helper(el)
        for i, el in enumerate(self.HASH):
            for j, v in enumerate(el):
                ans += ((1+i)*(1+j)*self.MAP[i][v])
        print(ans)


def main():
    obj = Hash_Solver()
    obj.read_inputs()
    obj.solve_hash()


main()