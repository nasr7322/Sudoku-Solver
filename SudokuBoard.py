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

    def move(self, row, col, value):
        self.grid[row][col] = value
        changed_domains = self.update_domain(row, col, value)
        self.print_move(row, col, value)
        self.print_changed_domains(changed_domains)

    def update_domain(self, row, col, value):
            # Dictionary to store the original and updated domains of affected cells
            affected_domains = {}
            
            # Store the original domain and update the domain of the current cell
            affected_domains[(row, col)] = (self.domains[(row, col)].copy(), {value})
            self.domains[(row, col)] = {value}
            
            # Update the domains of cells in the same row and column
            for i in range(self.size):
                # Update row
                if value in self.domains[(row, i)] and i != col:
                    if (row, i) not in affected_domains:
                        affected_domains[(row, i)] = (self.domains[(row, i)].copy(), set())
                    self.domains[(row, i)].discard(value)
                    affected_domains[(row, i)] = (affected_domains[(row, i)][0], self.domains[(row, i)].copy())
                    
                # Update column
                if value in self.domains[(i, col)] and i!= row:
                    if (i, col) not in affected_domains:
                        affected_domains[(i, col)] = (self.domains[(i, col)].copy(), set())
                    self.domains[(i, col)].discard(value)
                    affected_domains[(i, col)] = (affected_domains[(i, col)][0], self.domains[(i, col)].copy())
            
            # Calculate the starting row and column of the 3x3 box
            box_start_row = (row // 3) * 3
            box_start_col = (col // 3) * 3
            
            # Update the domains of cells in the same 3x3 box
            for i in range(3):
                for j in range(3):
                    cell = (box_start_row + i, box_start_col + j)
                    if value in self.domains[cell] and cell != (row, col):
                        if cell not in affected_domains:
                            affected_domains[cell] = (self.domains[cell].copy(), set())
                        self.domains[cell].discard(value)
                        affected_domains[cell] = (affected_domains[cell][0], self.domains[cell].copy())
                        
            return affected_domains

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
                value = self.grid[row][col]
                if value == 0:
                    continue
                if not self.is_valid_move(row, col, value):
                    return False
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
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 3, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
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
    