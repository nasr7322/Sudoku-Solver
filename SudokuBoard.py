import random

class SudokuBoard:
    def __init__(self, size=9):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.domains = {(row, col): set(range(1, 10)) for row in range(size) for col in range(size)}
        
    def fill(self, grid):
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for row in range(self.size):
            for col in range(self.size):
                if grid[row][col] != 0:
                    self.move(row, col, grid[row][col])
        return
    
    def is_valid_move(self, row, col, value):
        # checking rows and cols
        for i in range(self.size):
            if self.grid[row][i] == value or self.grid[i][col] == value:
                return False
        # checking 3 * 3 boxes
        box_start_row = (row // 3) * 3
        box_start_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.grid[box_start_row + i][box_start_col + j] == value:
                    return False

        return True

    def move(self, row, col, value):
        self.grid[row][col] = value
        changed_domains = self.update_domain(row, col, value)
        self.print_move(row, col, value)
        self.print_changed_domains(changed_domains)

    def update_domain(self, row, col, value):
        self.domains[(row, col)] = set()
        changed_domains = {}
        for i in range(self.size):
            if value in self.domains[(row, i)]:
                if (row, i) not in changed_domains:
                    changed_domains[(row, i)] = (self.domains[(row, i)].copy(), set())
                self.domains[(row, i)].discard(value)
                # store changed domains for printing
                changed_domains[(row, i)] = (changed_domains[(row, i)][0], self.domains[(row, i)].copy())
                
            if value in self.domains[(i, col)]:
                if (i, col) not in changed_domains:
                    changed_domains[(i, col)] = (self.domains[(i, col)].copy(), set())
                self.domains[(i, col)].discard(value)
                # store changed domains for printing
                changed_domains[(i, col)] = (changed_domains[(i, col)][0], self.domains[(i, col)].copy())
        
        box_start_row = (row // 3) * 3
        box_start_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                cell = (box_start_row + i, box_start_col + j)
                if value in self.domains[cell]:
                    if cell not in changed_domains:
                        changed_domains[cell] = (self.domains[cell].copy(), set())
                    self.domains[cell].discard(value)
                    # store changed domains for printing
                    changed_domains[cell] = (changed_domains[cell][0], self.domains[cell].copy())
                    
        return changed_domains

    def is_complete(self):
        # Check if the board is completely filled
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    return False
        return True
    
    def is_valid_board(self):
        # Check if the board is valid even if not filled
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    continue
                value = self.grid[row][col]
                self.grid[row][col] = 0
                if not self.is_valid_move(row, col, value):
                    self.grid[row][col] = value
                    return False
                self.grid[row][col] = value
        return True
    
    def is_valid_solution(self):
        return self.is_complete() and self.is_valid_board()

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
        print("\n")

    def print_changed_domains(self,changed_domains):
        print("Changed domains:")
        for cell, (old_domain, new_domain) in changed_domains.items():
            print(f"{cell}: {old_domain} => {new_domain}")
        print("\n")
            
    def print_domains(self):
        for cell, domain in self.domains.items():
            print(f"{cell}: {domain}")
        print("\n")
        
    ## TODO: Implement the following methods
    
    def generate_random_unique_solvable_board(self, difficulty):
        pass
    
    def has_unique_solution(self):
        pass
    
if __name__ == "__main__":
    board = SudokuBoard()
    
    solvable_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    board.fill(solvable_board)

    print("\nCurrent board:")
    for row in board.grid:
        print(row)
        
    print("\nDomains:")
    board.print_domains()
    print("\nEmpty cells:", board.find_empty())
    print("\nIs the board complete?", board.is_complete())
    print("\nIs the board valid?", board.is_valid_board())
    