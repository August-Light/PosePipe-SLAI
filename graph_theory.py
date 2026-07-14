from collections import deque


def valid_water_flow(neighbors, S, T):
    UNVISITED = 0
    VISITED = 1
    PROCESSED = 2

    print(neighbors, S, T)
    n = len(neighbors)
    state = [UNVISITED] * n
    flows = []

    queue = deque([S])
    while queue:
        current = queue.popleft()
        #print("current:", current, "state:", state, "queue:", list(queue))
        if current == T:
            state[current] = VISITED
            continue

        state[current] = PROCESSED

        has_unprocessed_neighbor = False
        for neighbor in neighbors[current]:
            if state[neighbor] != PROCESSED:
                has_unprocessed_neighbor = True
                flows.append((current, neighbor))
                if state[neighbor] == UNVISITED:
                    state[neighbor] = VISITED
                    queue.append(neighbor)

        if not has_unprocessed_neighbor:
            return False, None

    return True, flows


if __name__ == "__main__":
    neighbors3 = [[1, 2], [0, 6], [0, 3], [2, 4, 5], [3], [3, 6], [1, 5]]
    print(valid_water_flow(neighbors3, 0, 4))