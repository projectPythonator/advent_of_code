from sys import stdin
import re

class Boat_Race_Solver():
    def __init__(self):
        self.times = []
        self.dists = []
        
    def read_inputs(self):
        line = stdin.readline().strip()
        line = line[5:]
        self.times = list(map(int, re.sub(" +", " ", line).strip().split(' ')))
        line = stdin.readline().strip()
        line = line[9:]
        self.dists = list(map(int, re.sub(" +", " ", line).strip().split(' ')))
    
    def solve_race(self, tim, dst):
        r_val = 0
        for speed in range(tim):
            result = speed*(tim-speed)
            if result>dst:
                r_val += 1
        return r_val
    
    def solve_races(self):
        ans = 1
        for i in range(len(self.times)):
            ans *= self.solve_race(self.times[i], self.dists[i])
        print(ans)


def main():
    obj = Boat_Race_Solver()
    obj.read_inputs()
    obj.solve_races()
main()
    
    
    
    