from collections import deque

#reconstruct path from parent dictionary

def reconstruct_path(parent: dict, start: str, goal: str) -> list:
    path = []
    current = goal

    # Step backwards from goal to start using the parent map
    while current is not None:
        path.append(current)
        current = parent.get(current)  # None when start is reached

    path.reverse()  # Flip to read start → goal

    # If reconstruction didn't reach 'start', goal was unreachable
    if not path or path[0] != start:
        return []
    return path

#  Breadth-first search
def bfs(graph: dict, start: str, goal: str) -> None:
    print("  BREADTH-FIRST SEARCH (BFS) ")
    print(f"  Start : {start}    Goal : {goal}")

 
    queue   = deque([start])  # FIFO queue seeded with the start node
    visited = {start}         # Nodes already discovered (avoid revisits)
    parent  = {start: None}   # Maps each node → the node that found it
    order   = []              # Visit order for display


    while queue:
        # Remove the FRONT node
        current = queue.popleft()
        order.append(current)

        # Goal check 
        if current == goal:
            print(f"\n  Goal '{goal}' found!\n")
            break

        # Explore the neighbours 
        for neighbour in graph[current]:
            if neighbour not in visited:
                visited.add(neighbour)        # Mark as discovered
                parent[neighbour] = current   # Record how we got here
                queue.append(neighbour)       # Enqueue for later processing

    # Reconstruct and display results
    path = reconstruct_path(parent, start, goal)

    print(f"  Exploration order : {' -> '.join(order)}")
    if path:
        print(f"  Shortest path     : {' -> '.join(path)}")
        print(f"  Path length       : {len(path) - 1} edge(s)")
    else:
        print(f"  No path found from '{start}' to '{goal}'.")
    print()


#  Graph adjacency list - undirected
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'G'],
    'F': ['C'],
    'G': ['E'],
}


if __name__ == "__main__":
    START = 'A'   # Initial node
    GOAL  = 'G'   # Target node

    bfs(graph, START, GOAL)