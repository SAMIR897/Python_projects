import tkinter as tk
from tkinter import filedialog

def select_file_or_folder():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select File") or filedialog.askdirectory(title="Select Folder")
    root.destroy()
    return file_path