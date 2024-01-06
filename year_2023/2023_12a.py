#from sys import stdin
from collections import deque

class Spring_Solver():
    def __init__(self):
        self.schematics = []
        self.springs = []

        self.next_unknown = []
        self.positions = []
        self.cur_num_springs = 0
        self.schematic_len = 0

        self.current_springs = []
        self.line_masks = []
        self.spring_mask = 0
        self.empty_mask = 0

    def read_inputs(self):
        self.stdin = open('myfile.txt', 'r')
        m = 0
        for i, line in enumerate(self.stdin):
            a,b = line.strip().split(' ')
            self.schematics.append(a.strip())
            self.springs.append(list(map(int, b.split(','))))
        self.stdin.close()

    def print_mask(self, mask):
        print("mask is {}".format(''.join(['1' if mask&(1<<i)else '0' for i in range(self.schematic_len)])))

    def set_next_unknown(self, current_case):
        last = len(current_case)
        self.next_unknown = [len(current_case)] * len(current_case)
        self.positions = []
        for i, c in enumerate(current_case):
            nex = len(current_case)
            for j in range(i, len(current_case)):
                if current_case[j] == '?' or current_case[j]=='#':
                    nex = j
                    break
            self.next_unknown[i] = nex
        for i, c in enumerate(current_case):
            if i==0:
                continue
            if c=='#' and current_case[i-1]=='#':
                nex = len(current_case)
                for j in range(i+1, len(current_case)):
                    if current_case[j] == '?' or current_case[j] == '#' and current_case[j-1]!='#':
                        nex = j
                        break
                self.next_unknown[i] = nex
        for i,el in enumerate(self.next_unknown):
            if el==i:
                self.positions.append(i)

    def build_spring_masks(self, current_case):
        self.spring_mask = 0
        for i, c in enumerate(current_case):
            if c == '#':
                self.spring_mask = (self.spring_mask|1<<(i))

    def build_empty_mask(self, current_case):
        self.empty_mask = 0
        for i, c in enumerate(current_case):
            if c == '.':
                self.empty_mask = (self.empty_mask|1<<(i))

    def build_line_masks(self):
        mask = 0
        self.line_masks = [0]
        for i in range(32):
            mask = (mask|1<<(i))
            self.line_masks.append(mask)

    def set_up_data(self, current_case, sizes):
        self.set_next_unknown(current_case)
        self.build_spring_masks(current_case)
        self.build_empty_mask(current_case)
        self.cur_num_springs = len(sizes)
        self.schematic_len = len(current_case)
        self.current_springs = sizes

    def solve_springs_helper_2(self, current_spring, pos_ind, current_position, current_mask):
        self.cycles += 1
        #self.print_mask(current_mask)
        if self.cur_num_springs==current_spring:
            if (current_mask & self.spring_mask) == self.spring_mask and (current_position <= self.schematic_len + 1):
                self.print_mask(current_mask)
            #print("spring mask")
            #self.print_mask(self.spring_mask)

            # print("current mask")
            # self.print_mask(current_mask)
            # # print("empty mask")
            # self.print_mask(self.empty_mask)
            # print(self.positions)
            # if (current_mask&self.spring_mask)==self.spring_mask :
            #     print('herherhehrehrhehrehrhehrheasdfjaskl;dfjasdkl;dfgjasgkl;jasl;kfjskl;jdfl;kdasjfkl;asjfdl;kjasdfkl;jaskl;dfj')
            return 1 if (current_mask&self.spring_mask)==self.spring_mask and (current_position<=self.schematic_len+1) else 0
        if current_position>=self.schematic_len:
            return 0
        r_ans = 0
        #print(current_position, self.schematic_len)
        while pos_ind<len(self.positions) and current_position>self.positions[pos_ind]:
            #print(self.positions[pos_ind])
            pos_ind += 1
        #print("entering loop with this cur pos {} and using {} from {} next unknowns are {}".format(current_position, self.current_springs[current_spring], self.current_springs, self.next_unknown))
        for i in range(pos_ind, len(self.positions)):
            current_position = self.positions[i]
            #print(self.current_springs)
                # print("hereherehereherehereherehereherehereherehereherehereherehereherehereherehereherehereherehereherehereherehereherehereherehereherehereherehereherehere")
            new_mask = current_mask | (self.line_masks[self.current_springs[current_spring]]<<current_position)
            #self.print_mask((self.line_masks[self.current_springs[current_spring]]<<current_position))
            new_position = current_position + self.current_springs[current_spring] + 1 # fix the index out of bound error
            # print('here is the new mask each time')
            # self.print_mask(new_mask)

            if 0==(new_mask&self.empty_mask):
                r_ans += self.solve_springs_helper_2(current_spring+1, i, new_position, new_mask)
        return r_ans

    def solve_springs_helper_1(self, schematic, sizes):
        if '?' not in schematic:
            return 1
        self.set_up_data(schematic, sizes)
        ans = self.solve_springs_helper_2(0, 0, 0, 0)
        #print(schematic,sizes, ans)
        return ans


    def solve_springs(self):
        self.cycles = 0
        self.build_line_masks()
        ans = 0
        for i, el in enumerate(self.schematics):
            print(el, self.springs[i])
            ans += self.solve_springs_helper_1(el, self.springs[i])
        print(ans)
        print(self.cycles)


def main():
    obj = Spring_Solver()
    obj.read_inputs()
    obj.solve_springs()


main()

    
    