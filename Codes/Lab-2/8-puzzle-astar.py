import heapq
import random

class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        if self.f == other.f:
            if self.g == other.g:
                return self.state < other.state
            return self.g < other.g
        return self.f < other.f

def heuristic(node, goal_state):
    h = 0
    for i in range(9):
        if node.state[i] != 0:
            goal_pos = goal_state.index(node.state[i])
            h += abs(i // 3 - goal_pos // 3) + abs(i % 3 - goal_pos % 3)
    return h

def get_successors(node):
    successors = []
    index = node.state.index(0)
    quotient = index // 3
    remainder = index % 3
    moves = []
    
    if quotient == 0:
        moves.append(3)
    if quotient == 1:
        moves.extend([-3, 3])
    if quotient == 2:
        moves.append(-3)
    if remainder == 0:
        moves.append(1)
    if remainder == 1:
        moves.extend([-1, 1])
    if remainder == 2:
        moves.append(-1)

    for move in moves:
        im = index + move
        if 0 <= im < 9:
            new_state = list(node.state)
            new_state[index], new_state[im] = new_state[im], new_state[index]
            successor = Node(new_state, node, node.g + 1)
            successors.append(successor)
    
    successors.sort(key=lambda x: x.state)
    return successors

def search_agent(start_state, goal_state):
    start_node = Node(start_state, h=heuristic(Node(start_state), goal_state))
    goal_node = Node(goal_state)
    frontier = []
    heapq.heappush(frontier, (start_node.f, start_node))
    visited = set()
    nodes_explored = 0

    while frontier:
        _, node = heapq.heappop(frontier)
        if tuple(node.state) in visited:
            continue
        visited.add(tuple(node.state))
        nodes_explored += 1

        if node.state == goal_node.state:
            path = []
            while node:
                path.append(node.state)
                node = node.parent
            print(f"Total nodes explored: {nodes_explored}")
            return path[::-1]

        for successor in get_successors(node):
            if tuple(successor.state) not in visited:
                successor.h = heuristic(successor, goal_state)
                successor.f = successor.g + successor.h
                heapq.heappush(frontier, (successor.f, successor))

    print(f"Total nodes explored: {nodes_explored}")
    return None

start_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
s_node = Node(start_state)
D = 20
d = 0

# Generating a random goal state by applying random moves
while d <= D:
    goal_state = random.choice(list(get_successors(s_node))).state
    s_node = Node(goal_state)
    d += 1

# Searching for the solution
solution = search_agent(start_state, goal_state)

# Printing the solution if found
if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found.")