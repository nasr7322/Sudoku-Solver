import time
from SudokuBoard import SudokuBoard
from SudokuSolver import SudokuSolver
from sudoku_utils import SudokuUtils

def generate_report():
    difficulties = {'Easy': 60, 'Medium': 45, 'Hard': 30}
    report = []

    for difficulty, filled_cells in difficulties.items():
        print(f"Generating {difficulty} puzzle with {filled_cells} filled cells.")
        puzzle = SudokuUtils.generate_sudoku(filled_cells)
        sudoku_board = SudokuBoard()
        sudoku_board.fill(puzzle,True)
        
        print(f"Initial {difficulty} board:")
        sudoku_board.print_board()
        
        solver = SudokuSolver(sudoku_board)
        
        start_time = time.time()
        solver.solve()
        end_time = time.time()
        
        solve_time = end_time - start_time
        report.append((difficulty, solve_time, solver.iterations))
        
        print(f"Solved {difficulty} board in {solve_time:.8f} seconds:")
        sudoku_board.print_board()
        
        print(f"Iterations taken to solve {difficulty} board:")
        print(solver.iterations)
        
        print("\n" + "#" * 50 + "\n")
    
    return report

if __name__ == "__main__":
    report = generate_report()
    for difficulty, solve_time, iterations in report:
        print(f"{difficulty} puzzle solved in {solve_time:.8f} seconds with {iterations} Iterations.")