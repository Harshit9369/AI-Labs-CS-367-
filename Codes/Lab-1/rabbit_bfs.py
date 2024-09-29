from collections import deque 

def get_successors(state):
    successors = []
    empty_index = state.index('_')
    for move in [-2, -1, 1, 2]:
        new_index = empty_index + move
        if 0 <= new_index < 7:
            new_state = list(state)
            new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]
            new_state = tuple(new_state)
            successors.append(new_state)
            
    return successors

def bfs (start_state, goal_state):
    queue = deque([(start_state, [])])
    visited = set()
    path = []
    
    while queue:
        (state, path) = queue.popleft()
        if state in visited:
            continue
        visited.add(state)
        path = path + [state]
        if state == goal_state:
            return path
        for successor in get_successors(state):
            queue.append((successor, path))
            
    return None
    
n = 3

initial_state = []
goal_state = []

for i in range(n): 
    initial_state.append('E')
    goal_state.append('W')

initial_state.append('_')
goal_state.append('_')

for i in range(n):
    initial_state.append('W')
    goal_state.append('E')

solution = bfs(tuple(initial_state), tuple(goal_state))
if solution:
    print("BFS Solution found in", len(solution), "steps.")
    for step in solution:
        print(step)
else:
    print("No solution found using BFS.")