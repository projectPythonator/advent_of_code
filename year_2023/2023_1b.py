from sys import stdin
import string

def get_mapping():
    return {
        "one":"1", "two":"2", "three":"3", 
        "four":"4", "five":"5", "six":"6", 
        "seven":"7", "eight":"8", "nine":"9"} 
    
def fix_line(mapping, line):
    tmp = list(line)
    for k,v in mapping.items():
        l=line.find(k)
        r=line.rfind(k)
        if l!=-1:
            for i, c in enumerate(k):
                tmp[l+i]=v
        if r!=-1:
            for i, c in enumerate(k):
                tmp[r+i]=v
    return ''.join(tmp) 

def read_cal(mapping):
    tmp = set(list(string.digits))
    r_calibrations = []
    for line in stdin:
        aug = line
        aug = fix_line(mapping, aug)
        r_calibrations.append(''.join(c for c in aug if c in tmp))
    return r_calibrations
    #return [''.join(c for c in line if c in tmp) for line in stdin]

def get_ans(docs):
    ans = 0
    for info in docs:
        ans += int(''.join((info[0],info[-1])))
    return ans
    
def print_ans(answer):
    print(answer)

def main():
    mapping = get_mapping()
    calibrator_docs = read_cal(mapping)
    answer = get_ans(calibrator_docs)
    print_ans(answer)
main()
    