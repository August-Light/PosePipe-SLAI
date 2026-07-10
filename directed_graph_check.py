cases = [
    [(1, 2), (1, 3), (3, 4)],
    [(1, 2), (2, 3), (4, 5), (5, 6)],
    [(1, 2), (2, 3), (3, 1)]
]

names = [
    "connected and no cycle",
    "not connected",
    "has cycle"
]

for i in range(len(cases)):
    e = cases[i]
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

    s = list(n)[0]
    v = {s}
    q = [s]

    while q:
        x = q.pop(0)
        for y in u[x]:
            if y not in v:
                v.add(y)
                q.append(y)

    ok1 = len(v) == len(n)

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
            x, k = stack[-1]

            if k < len(g[x]):
                y = g[x][k]
                stack[-1] = (x, k + 1)

                if st[y] == 1:
                    ok2 = False
                elif st[y] == 0:
                    st[y] = 1
                    stack.append((y, 0))
            else:
                st[x] = 2
                stack.pop()

        if not ok2:
            break

    print(names[i], e, ok1 and ok2)
