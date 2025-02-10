import json

def find_hamiltonian_path(adj):
    """
    Determines if the directed graph specified by adjacency matrix 'adj' contains a Hamiltonian path.
    If one exists, returns (True, path), where path is the list of vertices in order.
    Otherwise, returns (False, []).
    
    Uses a dynamic programming approach with bitmasking.
    
    Parameters:
        adj (List[List[int]]): n x n adjacency matrix. For vertices u and v, an edge (u, v) exists
                               if adj[u][v] is nonzero/True.
                               
    Returns:
        tuple: (existence, path), where existence is True if a Hamiltonian path exists and path is the list 
               of vertices constituting the Hamiltonian path.
    """
    n = len(adj)
    full_mask = (1 << n) - 1
    
    # dp[mask][u] is True if there is a path which visits exactly the vertices in 'mask' and ends at vertex u.
    dp = [[False] * n for _ in range(1 << n)]
    # parent[mask][u] stores the previous vertex leading to u in the path corresponding to state (mask, u)
    parent = [[-1] * n for _ in range(1 << n)]
    
    # Base case: one-vertex paths.
    for v in range(n):
        dp[1 << v][v] = True
        parent[1 << v][v] = -1  # no predecessor
        
    # Build paths by increasing the number of vertices in the set.
    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u]:
                # Try to extend the path ending at u by any vertex v not in mask
                for v in range(n):
                    if (mask & (1 << v)) == 0 and adj[u][v]:
                        next_mask = mask | (1 << v)
                        # Only update if not already reached
                        if not dp[next_mask][v]:
                            dp[next_mask][v] = True
                            parent[next_mask][v] = u
    
    # Check for any state (full_mask, v) that indicates we've visited all vertices.
    for v in range(n):
        if dp[full_mask][v]:
            # Reconstruct the path from v backwards using parent pointers.
            path = []
            cur_mask = full_mask
            cur_v = v
            while cur_v != -1:
                path.append(cur_v)
                prev = parent[cur_mask][cur_v]
                if prev == -1:
                    break
                # Remove current vertex from mask.
                cur_mask = cur_mask ^ (1 << cur_v)
                cur_v = prev
            path.reverse()
            return True, path
    return False, []

def run(input_data, solver_params=None, extra_arguments=None):
    """
    Main function to run the Hamiltonian path detection.

    Parameters:
    - input_data: dict, expected to contain:
        'adjacency_matrix' (n x n adjacency matrix of the graph).
    - solver_params: dict, (optional) parameters for the solver, not used here.
    - extra_arguments: dict, (optional) any extra arguments needed, not used here.

    Returns:
    - dict: Output in the format:
        {
            "optimal_solution": list(best_solution),
            "existence": int()
        }
        where existence is 1 if a Hamiltonian path exists, 0 otherwise.
    """
    adjacency_matrix = input_data["adjacency_matrix"]
    
    # Run the Hamiltonian path dp algorithm.
    exists, best_solution = find_hamiltonian_path(adjacency_matrix)
    
    # Prepare the result in the Qcentroid JSON-like format.
    return {
        "optimal_solution": best_solution,
        "existence": int(exists)
    }