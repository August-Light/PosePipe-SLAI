# graph_theory.py

def connected_and_no_cycle(neighbors, S, T, num_pre_written):
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
    
    path_exists = visited[T]
    
    # Check that every single pre-written point (0 to num_pre_written - 1) was visited
    all_points_linked = all(visited[i] for i in range(num_pre_written))

    return path_exists and all_points_linked and not has_cycle