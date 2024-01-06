from sys import stdin
import string

def read_rgb():
    mapper = {"red":'0', "green":'1', "blue":'2'}
    rgb = []
    for line in stdin:
        rgb.append([0,0,0])
        cut = line.find(':')
        line = line[cut+1:]
        line = line.strip()
        for k,v in mapper.items():
            line = line.replace(k,v)
        tmp = line.split("; ")
        for grab in tmp:
            seto = grab.split(", ")
            for cubes in seto:
                amount,index = map(int, cubes.split())
                rgb[-1][index] = max(rgb[-1][index], amount)
    return rgb

def solve_rgb(rgb):
    red = 12
    green = 13
    blue = 14
    ans = 0
    for index,game in enumerate(rgb):
        if red >= game[0] and green >= game[1] and blue >= game[2]:
            ans += (index+1)
    return ans
    
def print_ans(answer):
    print(answer)

def main():
    rgb = read_rgb()
    answer = solve_rgb(rgb)
    print_ans(answer)
main()
    