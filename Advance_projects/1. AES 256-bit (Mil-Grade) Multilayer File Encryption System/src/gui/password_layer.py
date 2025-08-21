import tkinter as tk
from ..security.validation import validate_passwords

class PasswordLayer:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.entries = []
        tk.Label(root, text="Enter 4 Passwords (No Save Option):").pack()
        for i in range(4):
            frame = tk.Frame(root)
            frame.pack()
            tk.Label(frame, text=f"Password {i+1}:").pack(side=tk.LEFT)
            entry = tk.Entry(frame, show="*")
            entry.pack(side=tk.LEFT)
            self.entries.append(entry)
        tk.Button(root, text="Next", command=self.next).pack()

    def next(self):
        passwords = [e.get() for e in self.entries]
        if validate_passwords(passwords):
            self.root.destroy()  # Placeholder, will transition to dialpad
            self.callback()