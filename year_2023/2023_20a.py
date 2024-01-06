# from sys import stdin
import heapq
from collections import deque

class Mod():
    def __init__(self):
        self.name = ''
        self.mod_type = -1
        self.on_off = False
        self.outputs = []
        self.rem = {}

    def init_data(self, line):
        nam, outs = line.split(' -> ')
        if nam == 'broadcaster':
            self.name=nam
            self.mod_type = 0
            self.outputs=list(outs.split(', '))
        elif nam[0] == '%':
            self.name = nam[1:]
            self.mod_type = 1
            self.outputs=list(outs.split(', '))
        elif nam[0] == '&':
            self.name = nam[1:]
            self.mod_type = 2
            self.outputs=list(outs.split(', '))
            #print(self.rem)
        else:
            print("input error")

    def get_dest_pulse_list(self, inp, pulse):
        if self.mod_type == 0:
            pass
        elif self.mod_type == 1:
            if pulse:
                return []
            else:
                self.on_off = not self.on_off
                pulse = self.on_off
        elif self.mod_type == 2:
            self.rem[inp] = pulse
            pulse = not all(self.rem.values())
        else:
            print('type error type was {}'.format(self.mod_type))
        r_list = []
        for el in self.outputs:
            r_list.append((el, pulse))
        return r_list

class Pulse_Solver():
    def __init__(self):
        self.mods = {}
        self.parts = []

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        for line in self.stdin:
            line = line.strip()
            new_module = Mod()
            new_module.init_data(line)
            self.mods[new_module.name] = new_module

    def init_rem_data(self):
        for k,v in self.mods.items():
            for el in v.outputs:
                if el in self.mods and self.mods[el].mod_type == 2:
                    self.mods[el].rem[k] = False

    def solve_pulse_helper(self):
        q = deque()
        q.append(('broadcaster', False, 'button'))
        while q:
            inp, pulse, f = q.popleft()
            #print("{}  -{}-> {}".format(f, pulse, inp))
            self.ans[pulse] += 1
            if inp not in self.mods:
                continue
            add_queue = self.mods[inp].get_dest_pulse_list(f, pulse)
            for d, p in add_queue:
                q.append((d, p, inp))
        #print(self.mods['inv'].rem)


    def solve_pulse(self):
        self.ans = {False: 0, True: 0}
        for _ in range(1000):
            self.solve_pulse_helper()
        low = self.ans[False]
        high = self.ans[True]

        print("low {} high {} both {} multiply {}".format(low, high, low + high, high * low))


def main():
    obj = Pulse_Solver()
    obj.read_inputs()
    obj.init_rem_data()
    obj.solve_pulse()

    #$print(sum(map(int, list('4115453233542453565373363331'))))
main()






