from sys import stdin
from collections import Counter
import re

MAPPING = {
    'A':'m',
    'K':'l',
    'Q':'k',
    'J':'j',
    'T':'i',
    '9':'h',
    '8':'g',
    '7':'f',
    '6':'e',
    '5':'d',
    '4':'c',
    '3':'b',
    '2':'a',
}

class Hand():
    def __init__(self):
        self.hand = ''
        self.bid = 0
        self.hand_type = 0
        
    def __eq__(self, other):
        return self.hand_type == other.hand_type and self.hand == other.hand
    
    def __lt__(self, other):
        if self.hand_type != other.hand_type:
            return self.hand_type < other.hand_type
        else:
            return self.hand < other.hand
    
    def set_bid(self, value):
        self.bid = value
    
    def set_hand_type(self):
        cnt = list(Counter(self.hand).values())
        leno = len(cnt)
        if leno==1:
            self.hand_type = 6
        elif leno==5:
            self.hand_type = 0
        elif leno==4:
            self.hand_type = 1
        elif leno==3:
            if max(cnt)==2:
                self.hand_type = 2
            else:
                self.hand_type = 3
        else:
            if max(cnt)==3:
                self.hand_type = 4
            else:
                self.hand_type = 5
    
    def set_hand(self, value):
        self.hand = ''.join([MAPPING[c] for c in value])
        self.set_hand_type()

class Camel_Poker_Solver():
    def __init__(self):
        self.players = []
        
    def read_inputs(self):
        for line in stdin:
            hand,bid= line.strip().split(' ')
            new_hand = Hand()
            new_hand.set_bid(int(bid))
            new_hand.set_hand(hand)
            self.players.append(new_hand)
    
    def solve_poker(self):
        self.players.sort()
        ans = 0
        for ind, el in enumerate(self.players):
            ans += ((ind+1)*el.bid)
        print(ans)


def main():
    obj = Camel_Poker_Solver()
    obj.read_inputs()
    obj.solve_poker()
main()
    
    
    
    