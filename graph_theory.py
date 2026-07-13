def connected_and_no_cycle(neighbors, S):
    n = len(neighbors)
    visited = [False] * n

    has_cycle = False

    def dfs(node, parent):
        global has_cycle
        visited[node] = True
        for neighbor in neighbors[node]:
            if not visited[neighbor]:
                dfs(neighbor, node)
            elif neighbor != parent:
                has_cycle = True

    dfs(S, None)
    is_connected = False not in visited

    return is_connected and not has_cycle