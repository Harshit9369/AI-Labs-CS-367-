from collections import deque
def dfs(state, goal_state, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []
    
    if state == goal_state:
        return path
    
    visited.add(state)
    empty_index = state.index('_')
    
    for move in [-2, -1, 1, 2]:  
        new_index = empty_index + move
        if 0 <= new_index < 7:
            new_state = list(state)
            new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]
            new_state = tuple(new_state)
            
            if new_state not in visited:
                result = dfs(new_state, goal_state, visited, path + [new_state])
                if result is not None:
                    return result
    
    return None

initial_state = ('E', 'E', 'E', '_', 'W', 'W', 'W')
goal_state = ('W', 'W', 'W', '_', 'E', 'E', 'E')

dfs_solution = dfs(initial_state, goal_state)
if dfs_solution:
    print("DFS Solution found in", len(dfs_solution), "steps.")
    for step in dfs_solution:
        print(step)
else:
    print("No solution found using DFS.")