# from sys import stdin

class Hash_Solver():
    def __init__(self):
        self.input_strings = []
        self.current_value = 0

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
        for c in current:
            self.hash_c(c)
        return self.current_value

    def solve_hash(self):
        ans = 0
        for el in self.input_strings:
            ans += self.solve_hash_helper(el)
        print(ans)


def main():
    obj = Hash_Solver()
    obj.read_inputs()
    obj.solve_hash()


main()