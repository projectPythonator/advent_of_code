from sys import stdin
import string
import re

def read_grid():
    return [list(line.strip()) for line in stdin]

def generate_ref_nums_and_augmented_grid(grid):
    seto = set(list(string.digits))
    aug = [[-1 for _ in row] for row in grid]
    index = -1
    active = False
    for i,row in enumerate(grid):
        for j,el in enumerate(row):
            if el in seto:
                if not active:
                    active = True
                    index += 1
                aug[i][j] = index
            else:
                active = False
    grid_copy = [re.sub("\.+", ".",''.join([el if el in seto or el == '.' else '.' for el in row])).strip('.') for row in grid]
    ref_nums = [0]*(index+1)
    index = 0
    for num_line in grid_copy:
        for number in num_line.split('.'):
            if number == '':
                continue 
            ref_nums[index] = int(number)
            index+=1
    return ref_nums, aug
    
def check(i, j, ans_tmpo,ref_nums, aug):
    drc = [(1,1), (1,0), (1,-1), (-1,0), (-1,1), (-1,-1), (0,1), (0,-1)]
    tmp = set()
    for r,c in drc:
        if aug[i+r][j+c]!=-1:
            tmp.add(aug[i+r][j+c])
    if len(tmp)==2:
        ans_tmpo.append(ref_nums[list(tmp)[0]]*ref_nums[list(tmp)[-1]])

def solve_grid(grid, aug, ref_nums):
    seto = set(list(string.digits))
    seto.add('.')
    ans_tmpo = list()
    for i, row in enumerate(grid):
        for j, el in enumerate(row):
            if el not in seto:
                check(i, j, ans_tmpo,ref_nums,  aug)
    return sum(ans_tmpo)

    
def print_ans(answer):
    print(answer)

def main():
    grid = read_grid()
    ref_nums, aug = generate_ref_nums_and_augmented_grid(grid)
    answer = solve_grid(grid, aug, ref_nums)
    print_ans(answer)
main()
    