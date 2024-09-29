import heapq

class MarbleSolitaire:
    def __init__(self, initial_board):
        self.board = initial_board
        self.size = len(initial_board)
        self.center_position = (self.size // 2, self.size // 2)

    def get_valid_moves(self):
        valid_moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 1:
                    for delta_row, delta_col in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                        new_row, new_col = row + delta_row, col + delta_col
                        if 0 <= new_row < self.size and 0 <= new_col < self.size:
                            if self.board[new_row][new_col] == 0 and self.board[row + delta_row // 2][col + delta_col // 2] == 1:
                                valid_moves.append((row, col, new_row, new_col))
        return valid_moves

    def apply_move(self, move):
        from_row, from_col, to_row, to_col = move
        new_board = [r[:] for r in self.board]
        new_board[from_row][from_col] = 0
        new_board[to_row][to_col] = 1
        new_board[(from_row + to_row) // 2][(from_col + to_col) // 2] = 0
        return MarbleSolitaire(new_board)

    def is_goal_state(self):
        return sum(row.count(1) for row in self.board) == 1 and self.board[self.center_position[0]][self.center_position[1]] == 1

    def calculate_h(self):
        return sum(row.count(1) for row in self.board)

    def __lt__(self, other):
        return self.calculate_h() < other.calculate_h()

    def best_first_search(self):
        open_set = []
        heapq.heappush(open_set, (self.calculate_h(), self, []))
        visited_states = set()
        visited_states.add(tuple(map(tuple, self.board)))

        while open_set:
            _, current_node, move_sequence = heapq.heappop(open_set)

            if current_node.is_goal_state():
                return move_sequence

            for move in current_node.get_valid_moves():
                child_node = current_node.apply_move(move)
                board_tuple = tuple(map(tuple, child_node.board))

                if board_tuple not in visited_states:
                    new_sequence = move_sequence + [move]
                    heapq.heappush(open_set, (child_node.calculate_h(), child_node, new_sequence))
                    visited_states.add(board_tuple)

        return None  # No solution found


def display_board(board):
    for row in board:
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

game_instance = MarbleSolitaire(initial_board)
solution_path = game_instance.best_first_search()

if solution_path:
    print("Best-First Search solution found!")
    current_game = MarbleSolitaire(initial_board)
    display_board(current_game.board)

    for move in solution_path:
        current_game = current_game.apply_move(move)
        print(f"Move: {move}")
        display_board(current_game.board)
else:
    print("No solution found.")