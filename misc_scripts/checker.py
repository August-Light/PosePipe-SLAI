cases = [
    [(1, 2), (1, 3), (3, 4)],
    [(1, 2), (2, 3), (4, 5), (5, 6)],
    [(1, 2), (2, 3), (3, 1)]
]

def check(e, n):
    g = [[] for _ in range(n)]
    for i, j in e:
        g[i-1].append(j-1)
        g[j-1].append(i-1)

    visited = [0] * n

    def dfs(node, parent):
        visited[node] = 1

        for i in g[node]:
            if visited[i] == 0:
                dfs(i, node)
                
            elif i != parent:
                return True 
                
    
    has_cycle = dfs(0, -1)

    is_connected = 0 not in visited

    if is_connected and not has_cycle:
        print("yes")
    else:
        print("no")
