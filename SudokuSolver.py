import copy

from SudokuBoard import SudokuBoard

class SudokuSolver:
    def __init__(self, board: SudokuBoard):
        self.board = board
        self.steps = []

    def backtracking_search(self):
        if self.board.is_complete():
            return True
        cell = self.select_variable()
        for value in self.order_domain_values(cell):
            original_board = copy.deepcopy(self.board)
            if self.board.move(cell[0], cell[1], value):
                if self.backtracking_search():
                    self.steps.append((cell, value))
                    return True
                self.board = original_board
        return False
    
    def select_variable(self):
        min_domain = 2 ** 31
        chosen_cell = None
        for cell in self.board.domains: ## TODO: change to self.board.find_empty
            if self.board.grid[cell[0]][cell[1]] == 0 and len(self.board.domains[cell]) < min_domain:
                min_domain = len(self.board.domains[cell])
                chosen_cell = cell
        return chosen_cell
    
    def order_domain_values(self, cell):
        values_score = {value: 0 for value in self.board.domains[cell]}
        for row in range(self.board.size):
            if row == cell[0]:
                continue
            for value in self.board.domains[(row, cell[1])]:
                if value in values_score:
                  values_score[value] += 1
        for col in range(self.board.size):
            if col == cell[1]:
                continue
            for value in self.board.domains[(cell[0], col)]:
                if value in values_score:
                  values_score[value] += 1
        for row in range(cell[0] // 3 * 3, cell[0] // 3 * 3 + 3):
            for col in range(cell[1] // 3 * 3, cell[1] // 3 * 3 + 3):
                if row == cell[0] and col == cell[1]:
                    continue
                for value in self.board.domains[(row, col)]:
                    if value in values_score:
                      values_score[value] += 1
        return sorted(self.board.domains[cell], key=lambda value: values_score[value])

    def solve(self):
        self.backtracking_search()
        return self.steps.reverse()
    
if __name__ == "__main__":
    board = SudokuBoard()
    # sudoku = [  [4, 3, 5, 2, 6, 9, 7, 8, 1],
    #             [6, 8, 2, 5, 7, 1, 4, 9, 3],
    #             [1, 9, 7, 8, 3, 4, 5, 6, 2],
    #             [8, 2, 6, 1, 9, 5, 3, 4, 7],
    #             [3, 7, 4, 6, 8, 2, 9, 1, 5],
    #             [9, 5, 1, 7, 4, 3, 6, 2, 8],
    #             [5, 1, 9, 3, 2, 6, 8, 7, 4],
    #             [2, 4, 8, 9, 5, 7, 1, 3, 6],
    #             [7, 6, 3, 4, 1, 8, 2, 5, 9]]
    sudoku = [  [0, 3, 5, 2, 6, 9, 7, 8, 1],
                [6, 8, 0, 5, 7, 1, 4, 9, 3],
                [1, 9, 7, 8, 3, 4, 5, 6, 2],
                [8, 2, 6, 1, 9, 5, 3, 4, 7],
                [3, 7, 4, 6, 8, 2, 9, 1, 5],
                [9, 5, 1, 7, 4, 3, 6, 2, 8],
                [5, 1, 9, 3, 2, 6, 8, 7, 4],
                [2, 4, 8, 9, 5, 7, 1, 3, 6],
                [7, 6, 3, 4, 1, 8, 2, 5, 9]]
    
    board.fill(sudoku)
    solver = SudokuSolver(board)
    print("############### Started Solving ###############")
    
    solver.solve()
    if len(solver.steps) > 0:
        # for step in solver.steps:
        #     print(f"Move: {step[0]} -> {step[1]}")
        print("Sudoku solved:")
        for row in board.grid:
            print(row)
    else:
        print("No solution found")