from collections import defaultdict
import sys
def reads():
    r = []
    while True:
        s = input("INPUT: ").strip().upper()
        if s == "DONE":
            break
        if all(c in "ACGT" for c in s):
            r.append(s)
        else:
            print("Invalid! Only ACGT allowed.")
    return r

def kmers(r, k):
    out = []
    for x in r:
        for i in range(len(x) - k + 1):
            out.append(x[i:i+k])
    return out

def dbg(km):
    g = defaultdict(list)
    indeg = defaultdict(int)
    outdeg = defaultdict(int)
    for x in km:
        a, b = x[:-1], x[1:]
        g[a].append(b)
        outdeg[a] += 1
        indeg[b] += 1
    return g, indeg, outdeg

def start(g, ind, outd):
    for n in g:
        if outd[n] > ind[n]:
            return n
    return next(iter(g))

def path(g, st):
    stk = [st]
    res = []
    while stk:
        cur = stk[-1]
        if g[cur]:
            nxt = g[cur].pop()
            stk.append(nxt)
        else:
            res.append(stk.pop())
    return res[::-1]

def seq(p):
    s = p[0]
    for n in p[1:]:
        s += n[-1]
    return s

def show(g):
    print("\nGraph")
    for a in g:
        print(f"{a} -> {', '.join(g[a])}")

if __name__ == "__main__": 
    r = reads()
    if not r:
        print("No reads!")
        exit()
    try:
        k = int(input("K-mer size: "))
    except:
        print("Invalid K!")
        exit()
    if k < 2:
        print("K must be ≥ 2")
        exit()

    km = kmers(r, k)
    g, ind, outd = dbg(km)
    show(g.copy())
    st = start(g, ind, outd)
    p = path(g, st)
    s = seq(p)

    print("\nPath")
    print(" -> ".join(p))
    print("\nAssembled")
    print(s)