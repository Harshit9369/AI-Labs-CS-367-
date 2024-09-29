import heapq

class MarbleSolitaire:
    def __init__(self, board):
        self.board = board
        self.size = len(board)
        self.center = (self.size // 2, self.size // 2)

    def get_moves(self):
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 1:
                    for di, dj in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.size and 0 <= nj < self.size:
                            if self.board[ni][nj] == 0 and self.board[i + di // 2][j + dj // 2] == 1:
                                moves.append((i, j, ni, nj))
        return moves

    def make_move(self, move):
        fx, fy, tx, ty = move
        new_board = [row[:] for row in self.board]
        new_board[fx][fy] = 0
        new_board[tx][ty] = 1
        new_board[(fx + tx) // 2][(fy + ty) // 2] = 0
        return MarbleSolitaire(new_board)

    def is_goal(self):
        return sum(row.count(1) for row in self.board) == 1 and self.board[self.center[0]][self.center[1]] == 1

    def h1(self):
        return sum(row.count(1) for row in self.board)

    def h2(self):
        distance = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 1:
                    distance += abs(i - self.center[0]) + abs(j - self.center[1])
        return distance

    def __lt__(self, other):
        return True

    def a_star_search(self, heuristic):
        open_list = []
        heapq.heappush(open_list, (self.h1(), self, []))
        visited = set()

        while open_list:
            _, node, path = heapq.heappop(open_list)

            if tuple(map(tuple, node.board)) in visited:
                continue

            visited.add(tuple(map(tuple, node.board)))

            if node.is_goal():
                return path

            for move in node.get_moves():
                child_node = node.make_move(move)
                new_path = path + [move]
                if heuristic == 1:
                    heapq.heappush(open_list, (len(new_path) + child_node.h1(), child_node, new_path))
                else:
                    heapq.heappush(open_list, (len(new_path) + child_node.h2(), child_node, new_path))

        return None

def print_board(b):
    for row in b:
        print(" ".join(str(x) for x in row))
    print()

initial_board = [
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 0, 0]
]

game = MarbleSolitaire(initial_board)
solution_h1 = game.a_star_search(1)
solution_h2 = game.a_star_search(2)

if solution_h1:
    print("Solution found with Heuristic 1:")
    current_board = MarbleSolitaire(initial_board)
    print_board(current_board.board)

    for move in solution_h1:
        current_board = current_board.make_move(move)
        print(f"Move: {move}")
        print_board(current_board.board)
else:
    print("No solution found with Heuristic 1.")

if solution_h2:
    print("Solution found with Heuristic 2:")
    current_board = MarbleSolitaire(initial_board)
    print_board(current_board.board)

    for move in solution_h2:
        current_board = current_board.make_move(move)
        print(f"Move: {move}")
        print_board(current_board.board)
else:
    print("No solution found with Heuristic 2.")