
def connected_and_no_cycle(neighbors, S, T, numpre):
    n = len(neighbors)
    visited = [False] * n
    has_cycle = False

    def dfs(node, parent):
        nonlocal has_cycle  
        visited[node] = True
        
        for neighbor in neighbors[node]:
            if not visited[neighbor]:
                dfs(neighbor, node)
            elif neighbor != parent:
                has_cycle = True

    dfs(S, None)
    
    exist = visited[T]
    
    all_po = all(visited[i] for i in range(numpre))

    return exist and all_po and not has_cycle