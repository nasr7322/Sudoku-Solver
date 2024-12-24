import customtkinter as ctk
from tkinter import messagebox
from SudokuBoard import SudokuBoard
from SudokuSolver import SudokuSolver
from sudoku_utils import SudokuUtils

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Main Menu")
        self.size = 500
        self.root.geometry(f"{self.size}x{self.size}")
        
        self.button_style = {
            "font": ("Helvetica", 14),
            "text_color": "white",
            "width": 200,
            "height": 40,
        }

        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1 if i in [1, 2, 3] else 7)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create buttons for the main menu
        self.random_board_button = ctk.CTkButton(
            root,
            text="Random Board AI Mode",
            command=self.random_board_ai_mode,
            **self.button_style
            )
        
        self.random_board_button.grid(row=1, column=0)

        self.enter_board_button = ctk.CTkButton(
            root,
            text="Enter Board AI Mode",
            command=self.enter_board_ai_mode,
            **self.button_style
            )
        
        self.enter_board_button.grid(row=2, column=0)

        self.player_mode_button = ctk.CTkButton(
            root,
            text="Player Mode",
            command=self.player_mode,
            **self.button_style
            )
        
        self.player_mode_button.grid(row=3, column=0)

    def random_board_ai_mode(self):
        # Create a new window for difficulty selection
        difficulty_window = ctk.CTkToplevel(self.root)
        difficulty_window.title("Select Difficulty")
        difficulty_window.geometry("300x200")
        difficulty_window.attributes('-topmost', True)


        ctk.CTkLabel(difficulty_window, text="Select Difficulty:").pack(pady=20)

        # Create a combobox for difficulty selection
        self.difficulty_var = ctk.StringVar()
        self.difficulty_var.set("Easy")
        difficulty_combobox = ctk.CTkComboBox(difficulty_window, variable=self.difficulty_var, values=['Easy', 'Medium', 'Hard'])
        difficulty_combobox.pack(pady=10)

        # Create a button to start the Random Board AI Mode with the selected difficulty
        start_button = ctk.CTkButton(difficulty_window, text="Start", command=self.start_random_board_ai_mode)
        start_button.pack(pady=10)

    def start_random_board_ai_mode(self):
        difficulty = self.difficulty_var.get()
        if difficulty:
            filled_cells = {'Easy': 60, 'Medium': 50, 'Hard': 40}[difficulty]
            puzzle = SudokuUtils.generate_sudoku(filled_cells)
            self.display_board(puzzle)
        else:
            pass
        

    def enter_board_ai_mode(self):
        # Create a new window for entering the board
        enter_board_window = ctk.CTkToplevel(self.root)
        enter_board_window.title("Enter Sudoku Board")
        enter_board_window.geometry(f"{self.size}x{self.size}")
        enter_board_window.attributes('-topmost', True)
        
        for i in range(9):
            enter_board_window.grid_rowconfigure(i+1, weight=1 if i in range(9) else 3)
            enter_board_window.grid_columnconfigure(i, weight=1)

        self.board_entries = []
        for i in range(9):
            row_entries = []
            for j in range(9):
                entry = ctk.CTkEntry(enter_board_window, width=40, height=40,justify="center",font=("Helvetica", 20), fg_color=None)
                entry.grid(row=i+1, column=j)
                row_entries.append(entry)
            self.board_entries.append(row_entries)

        submit_button = ctk.CTkButton(enter_board_window, text="Submit", command=self.submit_board)
        submit_button.grid(row=10, column=0, columnspan=9, pady=10)

    def submit_board(self):
        board = []
        for row_entries in self.board_entries:
            row = []
            for entry in row_entries:
                value = entry.get()
                row.append(int(value) if value.isdigit() else 0)
            board.append(row)

        
        test_board = board.copy()
            
        # Validate the board if solvable and if unique
        if not SudokuUtils.is_valid_board(board):
            messagebox.showerror("Invalid Board", "The entered board is not valid.")
            return

        if not SudokuUtils.is_solvable(board):
            messagebox.showerror("Invalid Board", "The entered board is not solvable.")
            return

        if not SudokuUtils.is_unique_solution(board):
            messagebox.showerror("Warning", "The entered board does not have a unique solution.")

        self.display_board(board)

    def player_mode(self):
        # Create a new window for the player mode
        player_window = ctk.CTkToplevel(self.root)
        player_window.title("Player Mode")
        player_window.geometry(f"{self.size}x{self.size}")
        player_window.attributes('-topmost', True)

        for i in range(9):
            player_window.grid_rowconfigure(i+1, weight=1 if i in range(9) else 3)
            player_window.grid_columnconfigure(i, weight=1)

        self.board_entries = []
        for i in range(9):
            row_entries = []
            for j in range(9):
                entry = ctk.CTkEntry(player_window, width=40, height=40, justify="center", font=("Helvetica", 20), fg_color=None)
                entry.grid(row=i+1, column=j)
                entry.bind("<KeyRelease>", lambda event, row=i, col=j: self.validate_move(event, row, col))
                row_entries.append(entry)
            self.board_entries.append(row_entries)

        submit_button = ctk.CTkButton(player_window, text="Submit", command=self.check_solution)
        submit_button.grid(row=10, column=0, columnspan=9, pady=10)

    def validate_move(self, event, row, col):
        value = event.widget.get()
        if value.isdigit() and 1 <= int(value) <= 9:
            board = self.get_current_board()
            if SudokuUtils.is_valid_move(board, row, col, int(value)):
                self.board_entries[row][col].configure(border_color="white")
            else:
                self.board_entries[row][col].configure(border_color="red")
        else:
            if value == '':
                self.board_entries[row][col].configure(border_color="white")
            else:
                self.board_entries[row][col].configure(border_color="red")

    def get_current_board(self):
        board = []
        for row_entries in self.board_entries:
            row = []
            for entry in row_entries:
                value = entry.get()
                row.append(int(value) if value.isdigit() else 0)
            board.append(row)
        return board

    def check_solution(self):
        board = self.get_current_board()
        if SudokuUtils.is_valid_solution(board):
            messagebox.showinfo("Congratulations", "You have solved the Sudoku puzzle!")
        else:
            messagebox.showerror("Invalid Solution", "The current board is not a valid solution.")

    def display_board(self, board):
                
        sudoku_board = SudokuBoard()
        sudoku_board.fill(board, True)
        print("########## board filled ##########")
        
        print("Initial board:")
        sudoku_board.print_board()
        
        print("Initial domains:")
        sudoku_board.print_domains()
        
        board_window = ctk.CTkToplevel(self.root)
        board_window.title("Sudoku Board")
        board_window.geometry(f"{self.size}x{self.size}")
        
        for i in range(9):
            board_window.grid_rowconfigure(i+1, weight=1 if i in range(9) else 3)
            board_window.grid_columnconfigure(i, weight=1)

        self.board_entries = []
        for i in range(9):
            row_entries = []
            for j in range(9):
                entry = ctk.CTkEntry(board_window, width=40, height=40,justify="center",font=("Helvetica", 20), fg_color="transparent")
                entry.grid(row=i+1, column=j)
                entry.insert(0, str(board[i][j]) if board[i][j] != 0 else '')
                row_entries.append(entry)
            self.board_entries.append(row_entries)

        solve_button = ctk.CTkButton(board_window, text="Solve", command=lambda: self.solve_board(board))
        solve_button.grid(row=10, column=0, columnspan=9, pady=10)

    def solve_board(self, board):
        solved_board = SudokuBoard()
        solved_board.fill(board)
        solver = SudokuSolver(solved_board)
        solver.solve()
        self.update_board(solved_board, solver.steps)

    def update_board(self,sudoku_board, steps):
        for step in steps:
            cell, value = step
            sudoku_board.move(cell[0], cell[1], value, True)
            self.board_entries[cell[0]][cell[1]].delete(0, 'end')
            self.board_entries[cell[0]][cell[1]].insert(0, str(value))
            self.board_entries[cell[0]][cell[1]].configure(border_color="lightgreen")
            self.root.update()
            self.root.after(500)
            self.board_entries[cell[0]][cell[1]].configure(border_color="black")

if __name__ == "__main__":
    root = ctk.CTk()
    app = SudokuGUI(root)
    root.mainloop()