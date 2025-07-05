from collections import defaultdict
import sys
def reads():
    print("Enter reads :")
    r = []
    while True:
        s = input("Read: ").strip().upper()
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
    for x in km:
        a, b = x[:-1], x[1:]
        g[a].append(b)
    return g

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
    g = dbg(km)
    show(g)