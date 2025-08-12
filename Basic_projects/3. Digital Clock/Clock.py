import tkinter as tk
import time

class DigitalClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Clock")
        self.root.geometry("300x100")
        self.root.configure(bg="black")

        self.time_label = tk.Label(self.root, font=("Helvetica", 48), bg="black", fg="white")
        self.time_label.pack(expand=True)

        self.update_time()

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)  # Update the time every second

if __name__ == "__main__":
    root = tk.Tk()
    clock = DigitalClock(root)
    root.mainloop()
