from sys import stdin
import string

def read_cal():
    tmp = set(list(string.digits))
    return [''.join(c for c in line if c in tmp) for line in stdin]

def get_ans(docs):
    ans = 0
    for info in docs:
        ans += int(''.join((info[0],info[-1])))
    return ans
    
def print_ans(answer):
    print(answer)

def main():
    calibrator_docs = read_cal()
    answer = get_ans(calibrator_docs)
    print_ans(answer)
main()
    