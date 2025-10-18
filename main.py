import tkinter as tk
from utils.ui_theme_utils import UIManager

def main():
    root = tk.Tk()
    root.title("Asignación de Cupos - Proyecto ADAII")
    ui = UIManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()