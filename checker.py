cases = [
    [(1, 2), (1, 3), (3, 4)],
    [(1, 2), (2, 3), (4, 5), (5, 6)],
    [(1, 2), (2, 3), (3, 1)]
]

for e in cases:
    n = set()
    g = {}
    u = {}

    for a, b in e:
        n.add(a)
        n.add(b)

        if a not in g:
            g[a] = []
        if b not in g:
            g[b] = []
        g[a].append(b)

        if a not in u:
            u[a] = []
        if b not in u:
            u[b] = []
        u[a].append(b)
        u[b].append(a)
        
    def check_connectivity():
        s = list(n)[0]
        v = set()
        stack = [s]

        while stack:
            x = stack.pop()
            if x in v:
                continue
            v.add(x)
            for y in u[x]:
                if y not in v:
                    stack.append(y)

        return len(v) == len(n)
    def check_cycles():
        st = {}
        for x in n:
            st[x] = 0

        ok2 = True

        for s in n:
            if st[s] != 0:
                continue

            stack = [(s, 0)]
            st[s] = 1

            while stack and ok2:
                x, i = stack[-1]

                if i == len(g[x]):
                    st[x] = 2
                    stack.pop()
                else:
                    y = g[x][i]
                    stack[-1] = (x, i + 1)

                    if st[y] == 1:
                        ok2 = False
                    elif st[y] == 0:
                        st[y] = 1
                        stack.append((y, 0))

            if not ok2:
                break
        
        return ok2

    ok1 = check_connectivity()
    ok2 = check_cycles()

    if ok1 and ok2:
        print("yes")
    else:
        print("no")