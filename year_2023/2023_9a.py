#from sys import stdin
from collections import Counter
import re


class History_Solver():
    def __init__(self):
        self.top_rows = []
        self.grid = []

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        for line in self.stdin:
            self.top_rows.append(list(map(int, line.strip().split(' '))))

    def init_grid(self, current):
        self.grid = [[0 for _ in range(len(self.top_rows[current])+1)] for _ in range(len(self.top_rows[current])+1)]

    def fill_grid_top(self, current):
        for i,el in enumerate(self.top_rows[current]):
            self.grid[0][i] = el

    def fill_data(self, current):
        self.init_grid(current)
        self.fill_grid_top(current)

    def find_zero_row(self, working_row, leno):
        amt = 0
        for i in range(leno):
            self.grid[working_row][i] = self.grid[working_row-1][i+1]-self.grid[working_row-1][i]
        for i in range(leno):
            if self.grid[working_row][i]!=0:
                amt+=1
        if amt>0:
            return self.find_zero_row(working_row+1, leno-1)
        else:
            return working_row, leno

    def build_right_row(self, last_row, last_leno):
        last_row -= 1
        while last_row>-1:
            self.grid[last_row][last_leno+1] = self.grid[last_row][last_leno]+self.grid[last_row+1][last_leno]
            last_leno+=1
            last_row-=1

    def solve_history_helper(self, current):
        self.fill_data(current)
        last_row, leno = self.find_zero_row(1, len(self.grid[0])-2)
        self.build_right_row(last_row, leno)
        return self.grid[0][-1]


    def solve_history(self):
        ans = 0
        for i in range(len(self.top_rows)):
            ans += self.solve_history_helper(i)
        print(ans)


def main():
    obj = History_Solver()
    obj.read_inputs()
    obj.solve_history()


main()

    
    