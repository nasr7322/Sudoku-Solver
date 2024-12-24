import customtkinter as ctk
from SudokuGUI import SudokuGUI

if __name__ == "__main__":
    root = ctk.CTk()
    app = SudokuGUI(root)
    root.mainloop()
