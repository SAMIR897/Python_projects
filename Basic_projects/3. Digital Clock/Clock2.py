import tkinter as tk
import time

class DigitalClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Clock")
        self.root.geometry("400x150")
        self.root.configure(bg="black")
        
        # Make the window always stay on top
        self.root.attributes('-topmost', True)
        
        # No window decorations for a cleaner look
        self.root.overrideredirect(True)
        
        # Variables for dragging the window
        self._offset_x = 0
        self._offset_y = 0
        self.root.bind("<Button-1>", self.click_window)
        self.root.bind("<B1-Motion>", self.drag_window)
        
        # Main frame
        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack(expand=True, fill="both")
        
        # Time display
        self.time_label = tk.Label(
            self.frame,
            font=("Courier New", 64, "bold"),
            bg="black",
            fg="#00ff00"  # Bright green
        )
        self.time_label.pack(pady=10)
        
        # Date display
        self.date_label = tk.Label(
            self.frame,
            font=("Courier New", 14),
            bg="black",
            fg="#00ff00"
        )
        self.date_label.pack()
        
        # Close button (X in top-right)
        self.close_btn = tk.Label(
            self.root,
            text="×",
            font=("Arial", 12),
            fg="white",
            bg="black",
            padx=10
        )
        self.close_btn.place(relx=1.0, x=0, y=0, anchor="ne")
        self.close_btn.bind("<Button-1>", lambda e: root.destroy())
        
        self.update_time()
    
    def click_window(self, event):
        """Store initial click position for dragging"""
        self._offset_x = event.x
        self._offset_y = event.y
    
    def drag_window(self, event):
        """Move window based on drag"""
        x = self.root.winfo_pointerx() - self._offset_x
        y = self.root.winfo_pointery() - self._offset_y
        self.root.geometry(f"+{x}+{y}")
    
    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%A, %B %d, %Y")
        
        # Apply slight blink effect to the colon separators
        if int(time.time()) % 2 == 0:
            current_time = current_time.replace(":", " ")
        else:
            current_time = current_time.replace(":", ".")
        
        self.time_label.config(text=current_time)
        self.date_label.config(text=current_date)
        
        self.root.after(1000, self.update_time)

if __name__ == "__main__":
    root = tk.Tk()
    clock = DigitalClock(root)
    
    # Calculate position to center the window (optional)
    window_width = 400
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height/2 - window_height/2)
    position_right = int(screen_width/2 - window_width/2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
    
    root.mainloop()
