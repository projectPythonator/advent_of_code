from sys import stdin
import string
import re

def read_cards():
    index = -1
    active = False
    cards = []
    for line in stdin:
        line = re.sub("\ +", " ", line)
        cut = line.find(':')
        line = line[cut+1:]
        line = line.strip()
        a,b = line.split(' | ')
        a=a.strip(' ')
        b=b.strip(' ')
        cards.append((set(a.split(' ')), b.split(' ')))
    return cards

def solve_cards(cards):
    cardos = [1]*len(cards)
    index = -1
    for winner, my_nums in cards:
        index += 1
        amt = 0
        for el in my_nums:
            if el in winner:
                amt += 1 
        for i in range(index+1, index+1+amt):
            cardos[i] += cardos[index]

    return sum(map(int, cardos))

    
def print_ans(answer):
    print(answer)

def main():
    cards = read_cards()
    answer = solve_cards(cards)
    print_ans(answer)
main()
    