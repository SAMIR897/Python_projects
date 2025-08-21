import tkinter as tk
from ..security.validation import validate_dialpad

class DialpadLayer:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.counts = [0, 0, 0]
        self.frame = tk.Frame(root)
        self.frame.pack()
        for i in range(3):
            tk.Button(self.frame, text=f"Press {i+1}", command=lambda x=i: self.press(x)).grid(row=0, column=i)
        tk.Button(self.frame, text="Call", command=self.call).grid(row=1, column=1)

    def press(self, index):
        self.counts[index] += 1
        self.frame.grid_forget()
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        for i in range(3):
            tk.Button(self.frame, text=f"Press {i+1}: {self.counts[i]}", command=lambda x=i: self.press(x)).grid(row=0, column=i)
        tk.Button(self.frame, text="Call", command=self.call).grid(row=1, column=1)

    def call(self):
        if validate_dialpad(self.counts):
            self.callback()