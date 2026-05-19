
def reconstruct_path(parent: dict, start: str, goal: str) -> list:
    path = []
    current = goal

    # Step backwards from goal to start using the parent map
    while current is not None:
        path.append(current)
        current = parent.get(current)  # None when start is reached

    path.reverse()  # Flip to read start -> goal

    # If reconstruction didn't reach 'start', goal was unreachable
    if not path or path[0] != start:
        return []
    return path



#  Depth-first search
def dfs(graph: dict, start: str, goal: str) -> None:
    print("  DEPTH-FIRST SEARCH (DFS)")
    print(f"  Start : {start}    Goal : {goal}")

    # Initialise data structures 
    stack   = [start]        # LIFO stack seeded with the start node
    visited = set()          # Fully processed nodes (avoid reprocessing)
    parent  = {start: None}  # Maps each node -> the node that found it
    order   = []             # Visit order for display


    while stack:
        # Pop the TOP node
        current = stack.pop()

        # Skip already visited node
        if current in visited:
            continue

        visited.add(current)
        order.append(current)

 

        #Goal check
        if current == goal:
            print(f"\n  Goal '{goal}' found!\n")
            break

        #Expand neighbours 
        #Reverse so the first neighbour in the adjacency list ends up on TOP of the stack.
        for neighbour in reversed(graph[current]):
            if neighbour not in visited:
                stack.append(neighbour)              # Push onto the stack
                if neighbour not in parent:
                    parent[neighbour] = current      # Record discovery parent

    #Reconstruct and display results
    path = reconstruct_path(parent, start, goal)

    print(f"  Exploration order : {' -> '.join(order)}")
    if path:
        print(f"  Path found  : {' -> '.join(path)}")
        print(f"  Path length  : {len(path) - 1} edge(s)")
    else:
        print(f"  No path found from '{start}' to '{goal}'.")
    print()


# graph adjacency list
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

    dfs(graph, START, GOAL)