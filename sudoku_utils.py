import numpy as np
import random

class SudokuUtils:

    @staticmethod
    def is_valid_move(board, row, col, value):
        if not 1 <= int(value) <= 9:
            return False
        # checking rows and cols
        for i in range(9):
            if i != col and board[row][i] == value or i != row and board[i][col] == value:
                return False
        # checking 3 * 3 boxes
        box_start_row = (row // 3) * 3
        box_start_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if box_start_col+j != col and box_start_row+i !=row and board[box_start_row + i][box_start_col + j] == value:
                    return False
        return True


    @staticmethod
    def solve_sudoku(board, cnt=[], check_uniqueness=False):

        if check_uniqueness and cnt[0] > 1:
            return
        
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    for num in numbers:
                        if SudokuUtils.is_valid_move(board, row, col, num):
                            board[row][col] = num
                            solved = SudokuUtils.solve_sudoku(board, cnt, check_uniqueness)
                            if solved and not check_uniqueness:
                                return True
                            board[row][col] = 0
                    return False
                
        if not check_uniqueness:
            return True
        
        cnt[0] += 1


    @staticmethod
    def generate_complete_board():
        board = np.zeros((9, 9), dtype=int)
        SudokuUtils.solve_sudoku(board)
        return board

    @staticmethod
    def remove_cells(board, non_empty_cells):
        puzzle = board.copy()
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)

        for row, col in cells:
            temp = puzzle[row][col]
            puzzle[row][col] = 0
            if not SudokuUtils.is_unique_solution(puzzle.copy()):
                puzzle[row][col] = temp

            if np.count_nonzero(puzzle) <= non_empty_cells:
                break
        return puzzle
    

    @staticmethod
    def is_unique_solution(board):
        cnt = [0]
        SudokuUtils.solve_sudoku(board, cnt, check_uniqueness=True)
        return cnt[0] == 1


    @staticmethod
    def generate_sudoku(non_empty_cells=30):
        complete_board = SudokuUtils.generate_complete_board()
        puzzle = SudokuUtils.remove_cells(complete_board, non_empty_cells)
        return puzzle


    @staticmethod
    def is_solvable(board):
        return SudokuUtils.solve_sudoku(board.copy())

    @staticmethod
    def is_complete(board):
        # Check if the board is completely filled
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    return False
        return True
    
    @staticmethod
    def is_valid_board(board):
        # Check if the board is valid even if not filled
        for row in range(9):
            for col in range(9):
                value = board[row][col]
                if value == 0:
                    continue
                if not SudokuUtils.is_valid_move(board, row, col, value):
                    return False
        return True
    
    @staticmethod
    def is_valid_solution(board):
        return SudokuUtils.is_complete(board) and SudokuUtils.is_valid_board(board)
    
    @staticmethod
    def print_board(board):
        for row in board:
            print(row)


if __name__ == "__main__":
    puzzle = SudokuUtils.generate_sudoku(non_empty_cells=50)
    print("Generated Sudoku Puzzle:")
    print(puzzle)
    print(np.count_nonzero(puzzle))
    print(SudokuUtils.is_solvable(puzzle))

