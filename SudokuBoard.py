import random

class SudokuBoard:
        
    def __init__(self, size=9):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        # domains is a dictionary that maps each of the 9 * 9 cells to a set of possible values
        self.domains = {(row, col): set(range(1, 10)) for row in range(size) for col in range(size)}
        

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

    # make a move in row, col and update the domains of all other cells
    def move(self, row, col, value):
        self.grid[row][col] = value
        self.domains[(row, col)] = set()
        for i in range(self.size):
            self.domains[(row, i)].discard(value)
            self.domains[(i, col)].discard(value)
        
        box_start_row = (row // 3) * 3
        box_start_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                self.domains[(box_start_row + i, box_start_col + j)].discard(value)

    def is_complete(self):
        # Check if the board is completely filled
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    return 0 # board not filled yet

        # Check rows for validity
        for row in range(self.size):
            if not self.is_valid_group(self.grid[row]):
                return -1 # board filled but invalid

        # Check columns for validity
        for col in range(self.size):
            if not self.is_valid_group([self.grid[row][col] for row in range(self.size)]):
                return -1 # board filled but invalid

        # Check 3x3 subgrids for validity
        subgrid_size = int(self.size ** 0.5)
        for row in range(0, self.size, subgrid_size):
            for col in range(0, self.size, subgrid_size):
                if not self.is_valid_subgrid(row, col, subgrid_size):
                    return -1 # board filled but invalid

        return 1 # board filled and valid

    def is_valid_group(self, group):
        # Checks if a row or column contains unique numbers from 1 to size.
        return len(group) == len(set(group)) and all(1 <= num <= self.size for num in group)

    def is_valid_subgrid(self, start_row, start_col, subgrid_size):
        # Checks if a 3x3 subgrid contains unique numbers from 1 to size.
        nums = []
        for row in range(start_row, start_row + subgrid_size):
            for col in range(start_col, start_col + subgrid_size):
                nums.append(self.grid[row][col])
        return self.is_valid_group(nums)

    def find_empty(self):
        # returns all the empty Cells
        empty_cells = []
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    empty_cells.append((row, col))
        return empty_cells
    

if __name__ == "__main__":
    board = SudokuBoard()
    # Example of filling the board with some values and checking its status
    for _ in range(40):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        value = random.randint(1, 9)
        if board.is_valid_move(row, col, value):
            board.move(row, col, value)

    print("Current board:")
    for row in board.grid:
        print(row)
        
    print("\n\nDomains:", board.domains)

    print("\n\nEmpty cells:", board.find_empty())
    print("\n\nIs the board complete?", board.is_complete())