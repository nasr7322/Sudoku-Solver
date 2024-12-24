import copy
import queue
import random

class SudokuBoard:
    def __init__(self, size=9):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.domains = {(row, col): set(range(1, 10)) for row in range(size) for col in range(size)}
        
    def fill(self, grid, prnt=False):
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for row in range(self.size):
            for col in range(self.size):
                if grid[row][col] != 0:
                    self.move(row, col, grid[row][col], prnt)
        
    
    def is_valid_move(self, row, col, value):
        for i in range(self.size):
            if self.grid[row][i] == value or self.grid[i][col] == value:
                if i != col and i != row:
                    return False
        # checking 3 * 3 boxes
        box_start_row = (row // 3) * 3
        box_start_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.grid[box_start_row + i][box_start_col + j] == value:
                    if box_start_row + i != row and box_start_col + j != col:
                        return False

        return True

    def move(self, row, col, value, prnt=False):
        is_consistent, changed_domains = self.arc_consistency(row, col, value)
        if not is_consistent or not self.is_valid_move(row, col, value):
            print(f"Invalid move: ({row}, {col}) -> {value}")
            return False
        self.grid[row][col] = value
        if prnt:
            self.print_move(row, col, value)
            self.print_changed_domains(changed_domains)
        return True

    def arc_consistency(self, cell_row, cell_col, cell_value, alter_table=True):
        constraints_queue = queue.Queue()
        self.original_domains = copy.deepcopy(self.domains)
        self.domains[(cell_row, cell_col)] = {cell_value}
        constraints_queue.put((cell_row, cell_col))
          
        if not self.revise_neighbors(cell_row, cell_col, constraints_queue):
            self.domains = self.original_domains
            return False, {}
            
        while not constraints_queue.empty():
            row, col = constraints_queue.get()
            if not self.revise_neighbors(row, col, constraints_queue):
                self.domains = self.original_domains
                return False, {}

        if not alter_table:
            self.domains = self.original_domains
            return True, {}

        changed_domains = {cell: (self.original_domains[cell].copy(), self.domains[cell].copy()) for cell in self.domains if self.original_domains[cell] != self.domains[cell]}
        return True, changed_domains
    
    def revise_neighbors(self, cell_row, cell_col, constraints_queue):
        
        for row in range(self.size):
            if row == cell_row:
                continue
            revised_domain = self.domains[(row, cell_col)].copy()
            for value in revised_domain:
                # domain reduction when the cell has only one value
                if self.domains[(cell_row, cell_col)] == {value}:
                    self.domains[(row, cell_col)].discard(value)
                    if len(self.domains[(row, cell_col)]) == 0:
                        return False
                    constraints_queue.put((row, cell_col))
                    
        for col in range(self.size):
            if col == cell_col:
                continue
            revised_domain = self.domains[(cell_row, col)].copy()
            for value in revised_domain:
                if self.domains[(cell_row, cell_col)] == {value}:
                    self.domains[(cell_row, col)].discard(value)
                    if len(self.domains[(cell_row, col)]) == 0:
                        return False
                    constraints_queue.put((cell_row, col))
        
        box_start_row = (cell_row // 3) * 3
        box_start_col = (cell_col // 3) * 3
        
        for row in range(3):
            for col in range(3):
                if box_start_row + row == cell_row and box_start_col + col == cell_col:
                    continue
                revised_domain = self.domains[(box_start_row + row, box_start_col + col)].copy()
                for value in revised_domain:
                    if self.domains[(cell_row, cell_col)] == {value}:
                        self.domains[(box_start_row + row, box_start_col + col)].discard(value)
                        if len(self.domains[(box_start_row + row, box_start_col + col)]) == 0:
                            return False
                        constraints_queue.put((box_start_row + row, box_start_col + col))
                        
        return True
    
    def find_empty(self):
        # returns all the empty Cells
        empty_cells = []
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    empty_cells.append((row, col))
        return empty_cells
    
    def print_move(self, row, col, value):
        print(f"Move: ({row}, {col}) -> {value}")

    def print_changed_domains(self, changed_domains):
        if len(changed_domains) == 0:
            print("No changes in domains\n")
            return
        print("Changed domains:")
        for cell, (old_domain, new_domain) in changed_domains.items():
            print(f"{cell}: {old_domain} => {new_domain}")
            
    def print_domains(self):
        for cell, domain in self.domains.items():
            print(f"{cell}: {domain}")
        
    def print_board(self):
        for row in self.grid:
            print(row)
            
    def is_complete(self):
        for row in self.grid:
            for cell in row:
                if cell == 0:
                    return False
        return True
        
    ## TODO: Implement the following methods
    
    def generate_random_unique_solvable_board(self, difficulty):
        pass
    
    def has_unique_solution(self):
        pass
    
if __name__ == "__main__":
    board = SudokuBoard()
    
    solvable_board = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [9, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    board.fill(solvable_board)

    print("\nCurrent board:")

    board.print_board()
    print("\nDomains:")
    board.print_domains()
    print("\nEmpty cells:", board.find_empty())
    