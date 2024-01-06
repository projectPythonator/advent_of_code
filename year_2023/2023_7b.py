from sys import stdin
from collections import Counter
import re

MAPPING = {
    'A':'m',
    'K':'l',
    'Q':'k',
    'T':'j',
    '9':'i',
    '8':'h',
    '7':'g',
    '6':'f',
    '5':'e',
    '4':'d',
    '3':'c',
    '2':'b',
    'J':'a',
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
        stats = Counter(self.hand)
        if 'a' in stats:
            amt = stats['a']
            if amt==5:
                pass
            elif amt==4:
                self.hand_type=6
                return
            elif amt==3:
                if len(stats)==2:
                    self.hand_type=6
                    return
                else:
                    self.hand_type=5
                    return
            elif amt==2:
                if len(stats)==2:
                    self.hand_type=6
                    return
                elif len(stats)==3:
                    self.hand_type=5
                    return
                else:
                    self.hand_type=3
                    return
            else:
                if len(stats)==2:
                    self.hand_type=6
                    return
                elif len(stats)==3:
                    if max(list(stats.values()))==3:
                        self.hand_type=5
                        return
                    else:
                        self.hand_type=4
                        return
                elif len(stats)==4:
                    self.hand_type=3
                    return
                else:
                    self.hand_type=1
                    return
        cnt = list(stats.values())
        cnt.sort()
        leno = len(cnt)
        if leno==1:
            self.hand_type = 6
        elif leno==5:
            self.hand_type = 0
        elif leno==4:
            self.hand_type = 1
        elif leno==3:
            if cnt[-1]==2:
                self.hand_type = 2
            else:
                self.hand_type = 3
        else:
            if cnt[-1]==3:
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
    
    
    
    