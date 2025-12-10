import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import ImageGrab
import threading
import time
from datetime import datetime
import os

class ScreenRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Recorder Pro")
        self.root.geometry("700x650")
        self.root.resizable(False, False)
        
        # Colors
        self.bg_color = "#1e1e2e"
        self.secondary_bg = "#2a2a3e"
        self.accent_color = "#00d4ff"
        self.record_color = "#ff4444"
        self.success_color = "#00ff88"
        self.text_color = "#ffffff"
        
        self.root.configure(bg=self.bg_color)
        
        # Recording variables
        self.is_recording = False
        self.is_paused = False
        self.video_writer = None
        self.output_file = None
        self.frame_count = 0
        self.start_time = None
        self.pause_time = 0
        self.recording_thread = None
        
        # Settings variables
        self.fps_var = tk.StringVar(value="30")
        self.quality_var = tk.StringVar(value="High")
        self.format_var = tk.StringVar(value="MP4")
        self.save_path_var = tk.StringVar(value=os.path.expanduser("~/Videos"))
        self.filename_var = tk.StringVar(value="")
        
        # Recording stats
        self.duration_var = tk.StringVar(value="00:00:00")
        self.frames_var = tk.StringVar(value="0")
        self.file_size_var = tk.StringVar(value="0 MB")
        
        # Create GUI
        self.create_gui()
        
        # Center window
        self.center_window()
        
        # Update timer
        self.update_timer()
        
    def create_gui(self):
        """Create the main GUI"""
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ===== HEADER =====
        header_frame = tk.Frame(main_frame, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title with icon
        title_label = tk.Label(
            header_frame,
            text="🎬 Screen Recorder Pro",
            font=("Arial", 26, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Professional Screen Recording Tool",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#888888"
        )
        subtitle_label.pack(pady=(5, 0))
        
        # ===== STATUS CARD =====
        status_card = tk.Frame(main_frame, bg=self.secondary_bg, relief=tk.FLAT)
        status_card.pack(fill=tk.X, pady=(0, 20))
        
        status_inner = tk.Frame(status_card, bg=self.secondary_bg)
        status_inner.pack(padx=20, pady=20)
        
        # Recording indicator
        self.indicator_frame = tk.Frame(status_inner, bg=self.secondary_bg)
        self.indicator_frame.pack()
        
        self.indicator_canvas = tk.Canvas(
            self.indicator_frame,
            width=20,
            height=20,
            bg=self.secondary_bg,
            highlightthickness=0
        )
        self.indicator_canvas.pack(side=tk.LEFT, padx=(0, 10))
        
        self.indicator = self.indicator_canvas.create_oval(2, 2, 18, 18, fill="#666666", outline="")
        
        self.status_label = tk.Label(
            self.indicator_frame,
            text="Ready to Record",
            font=("Arial", 14, "bold"),
            bg=self.secondary_bg,
            fg=self.text_color
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Stats frame
        stats_frame = tk.Frame(status_inner, bg=self.secondary_bg)
        stats_frame.pack(pady=(15, 0))
        
        # Duration
        self.create_stat_box(stats_frame, "⏱️ Duration", self.duration_var, 0)
        
        # Frames
        self.create_stat_box(stats_frame, "🎞️ Frames", self.frames_var, 1)
        
        # File size
        self.create_stat_box(stats_frame, "💾 Size", self.file_size_var, 2)
        
        # ===== SETTINGS SECTION =====
        settings_label = tk.Label(
            main_frame,
            text="⚙️ Recording Settings",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            anchor="w"
        )
        settings_label.pack(fill=tk.X, pady=(10, 5))
        
        settings_card = tk.Frame(main_frame, bg=self.secondary_bg, relief=tk.FLAT)
        settings_card.pack(fill=tk.X, pady=(0, 20))
        
        settings_inner = tk.Frame(settings_card, bg=self.secondary_bg)
        settings_inner.pack(padx=20, pady=15)
        
        # FPS Setting
        fps_frame = tk.Frame(settings_inner, bg=self.secondary_bg)
        fps_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            fps_frame,
            text="FPS (Frames Per Second):",
            font=("Arial", 10),
            bg=self.secondary_bg,
            fg=self.text_color,
            width=25,
            anchor="w"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        fps_combo = ttk.Combobox(
            fps_frame,
            textvariable=self.fps_var,
            values=["15", "24", "30", "60"],
            state="readonly",
            width=15,
            font=("Arial", 10)
        )
        fps_combo.pack(side=tk.LEFT)
        
        # Quality Setting
        quality_frame = tk.Frame(settings_inner, bg=self.secondary_bg)
        quality_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            quality_frame,
            text="Video Quality:",
            font=("Arial", 10),
            bg=self.secondary_bg,
            fg=self.text_color,
            width=25,
            anchor="w"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        quality_combo = ttk.Combobox(
            quality_frame,
            textvariable=self.quality_var,
            values=["Low", "Medium", "High", "Ultra"],
            state="readonly",
            width=15,
            font=("Arial", 10)
        )
        quality_combo.pack(side=tk.LEFT)
        
        # Format Setting
        format_frame = tk.Frame(settings_inner, bg=self.secondary_bg)
        format_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            format_frame,
            text="Video Format:",
            font=("Arial", 10),
            bg=self.secondary_bg,
            fg=self.text_color,
            width=25,
            anchor="w"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        format_combo = ttk.Combobox(
            format_frame,
            textvariable=self.format_var,
            values=["MP4", "AVI"],
            state="readonly",
            width=15,
            font=("Arial", 10)
        )
        format_combo.pack(side=tk.LEFT)
        
        # ===== SAVE LOCATION =====
        location_label = tk.Label(
            main_frame,
            text="📁 Save Location",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            anchor="w"
        )
        location_label.pack(fill=tk.X, pady=(10, 5))
        
        location_card = tk.Frame(main_frame, bg=self.secondary_bg, relief=tk.FLAT)
        location_card.pack(fill=tk.X, pady=(0, 20))
        
        location_inner = tk.Frame(location_card, bg=self.secondary_bg)
        location_inner.pack(padx=20, pady=15, fill=tk.X)
        
        # Path display
        path_frame = tk.Frame(location_inner, bg=self.secondary_bg)
        path_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.path_label = tk.Label(
            path_frame,
            textvariable=self.save_path_var,
            font=("Arial", 9),
            bg=self.accent_color,
            fg="#000000",
            anchor="w",
            padx=10,
            pady=8,
            relief=tk.FLAT
        )
        self.path_label.pack(fill=tk.X)
        
        # Browse button
        self.browse_button = tk.Button(
            location_inner,
            text="📂 Choose Save Location",
            command=self.choose_save_location,
            bg="#4a4a6e",
            fg=self.text_color,
            font=("Arial", 10),
            padx=15,
            pady=8,
            cursor="hand2",
            relief=tk.FLAT,
            activebackground="#5a5a7e"
        )
        self.browse_button.pack()
        
        # ===== CONTROL BUTTONS =====
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(pady=(10, 0))
        
        # Record Button
        record_btn_container = tk.Frame(button_frame, bg="#ff5555", highlightthickness=0)
        record_btn_container.pack(side=tk.LEFT, padx=5)
        
        self.record_button = tk.Button(
            record_btn_container,
            text="⏺ START RECORDING",
            command=self.toggle_recording,
            bg=self.record_color,
            fg=self.text_color,
            font=("Arial", 13, "bold"),
            padx=30,
            pady=15,
            cursor="hand2",
            relief=tk.RAISED,
            bd=3,
            activebackground="#ff5555"
        )
        self.record_button.pack(padx=2, pady=2)
        
        # Pause Button
        pause_btn_container = tk.Frame(button_frame, bg="#ffa726", highlightthickness=0)
        pause_btn_container.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = tk.Button(
            pause_btn_container,
            text="⏸ PAUSE",
            command=self.toggle_pause,
            bg="#ff9800",
            fg=self.text_color,
            font=("Arial", 13, "bold"),
            padx=30,
            pady=15,
            cursor="hand2",
            relief=tk.RAISED,
            bd=3,
            state=tk.DISABLED,
            activebackground="#ffa726"
        )
        self.pause_button.pack(padx=2, pady=2)
        
        # Stop Button
        stop_btn_container = tk.Frame(button_frame, bg="#666666", highlightthickness=0)
        stop_btn_container.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(
            stop_btn_container,
            text="⏹ STOP",
            command=self.stop_recording,
            bg="#555555",
            fg=self.text_color,
            font=("Arial", 13, "bold"),
            padx=30,
            pady=15,
            cursor="hand2",
            relief=tk.RAISED,
            bd=3,
            state=tk.DISABLED,
            activebackground="#666666"
        )
        self.stop_button.pack(padx=2, pady=2)
        
        # ===== FOOTER =====
        footer_frame = tk.Frame(main_frame, bg=self.bg_color)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        footer_label = tk.Label(
            footer_frame,
            text="💡 Tip: Close unnecessary apps before recording for best performance",
            font=("Arial", 8, "italic"),
            bg=self.bg_color,
            fg="#666666"
        )
        footer_label.pack()
        
    def create_stat_box(self, parent, label, variable, column):
        """Create a statistics display box"""
        frame = tk.Frame(parent, bg="#3a3a4e", relief=tk.FLAT)
        frame.grid(row=0, column=column, padx=10)
        
        tk.Label(
            frame,
            text=label,
            font=("Arial", 9),
            bg="#3a3a4e",
            fg="#888888",
            padx=20,
            pady=(8, 2)
        ).pack()
        
        tk.Label(
            frame,
            textvariable=variable,
            font=("Arial", 14, "bold"),
            bg="#3a3a4e",
            fg=self.success_color,
            padx=20,
            pady=(2, 8)
        ).pack()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def choose_save_location(self):
        """Choose save location"""
        if self.is_recording:
            messagebox.showwarning("Warning", "Cannot change location while recording!")
            return
            
        directory = filedialog.askdirectory(
            title="Choose Save Location",
            initialdir=self.save_path_var.get()
        )
        
        if directory:
            self.save_path_var.set(directory)
            
    def toggle_recording(self):
        """Start or resume recording"""
        if not self.is_recording:
            self.start_recording()
        elif self.is_paused:
            self.resume_recording()
            
    def start_recording(self):
        """Start screen recording"""
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screen_recording_{timestamp}.{self.format_var.get().lower()}"
        self.output_file = os.path.join(self.save_path_var.get(), filename)
        self.filename_var.set(filename)
        
        # Reset stats
        self.frame_count = 0
        self.start_time = time.time()
        self.pause_time = 0
        
        # Update UI
        self.is_recording = True
        self.is_paused = False
        self.record_button.config(text="⏺ RECORDING...", state=tk.DISABLED, bg="#666666")
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL, bg=self.record_color)
        self.browse_button.config(state=tk.DISABLED)
        
        # Update status
        self.status_label.config(text="Recording in Progress", fg=self.record_color)
        self.indicator_canvas.itemconfig(self.indicator, fill=self.record_color)
        self.blink_indicator()
        
        # Start recording thread
        self.recording_thread = threading.Thread(target=self.record_screen, daemon=True)
        self.recording_thread.start()
        
    def record_screen(self):
        """Record screen in background thread"""
        try:
            # Get screen size
            screen = ImageGrab.grab()
            screen_size = screen.size
            
            # Get FPS
            fps = int(self.fps_var.get())
            
            # Get codec based on format
            if self.format_var.get() == "MP4":
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            else:
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
            
            # Create video writer
            self.video_writer = cv2.VideoWriter(
                self.output_file,
                fourcc,
                fps,
                screen_size
            )
            
            frame_delay = 1.0 / fps
            
            while self.is_recording:
                if not self.is_paused:
                    # Capture screen
                    img = ImageGrab.grab()
                    
                    # Convert to numpy array and BGR color space
                    frame = np.array(img)
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    
                    # Write frame
                    self.video_writer.write(frame)
                    self.frame_count += 1
                    
                    # Update stats
                    self.frames_var.set(str(self.frame_count))
                    
                    # Calculate file size
                    if os.path.exists(self.output_file):
                        size_mb = os.path.getsize(self.output_file) / (1024 * 1024)
                        self.file_size_var.set(f"{size_mb:.2f} MB")
                    
                time.sleep(frame_delay)
                
        except Exception as e:
            messagebox.showerror("Recording Error", f"An error occurred:\n{str(e)}")
            self.stop_recording()
            
    def toggle_pause(self):
        """Pause or resume recording"""
        if self.is_paused:
            self.resume_recording()
        else:
            self.pause_recording()
            
    def pause_recording(self):
        """Pause recording"""
        self.is_paused = True
        self.pause_start = time.time()
        
        # Update UI
        self.pause_button.config(text="▶ RESUME", bg="#4caf50")
        self.status_label.config(text="Recording Paused", fg=self.warning_color)
        self.indicator_canvas.itemconfig(self.indicator, fill=self.warning_color)
        
    def resume_recording(self):
        """Resume recording"""
        self.is_paused = False
        self.pause_time += time.time() - self.pause_start
        
        # Update UI
        self.pause_button.config(text="⏸ PAUSE", bg="#ff9800")
        self.status_label.config(text="Recording in Progress", fg=self.record_color)
        self.indicator_canvas.itemconfig(self.indicator, fill=self.record_color)
        self.blink_indicator()
        
    def stop_recording(self):
        """Stop recording"""
        if not self.is_recording:
            return
            
        # Stop recording
        self.is_recording = False
        self.is_paused = False
        
        # Wait for thread to finish
        if self.recording_thread:
            self.recording_thread.join(timeout=2)
        
        # Release video writer
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
        
        # Update UI
        self.record_button.config(text="⏺ START RECORDING", state=tk.NORMAL, bg=self.record_color)
        self.pause_button.config(text="⏸ PAUSE", state=tk.DISABLED, bg="#ff9800")
        self.stop_button.config(state=tk.DISABLED, bg="#555555")
        self.browse_button.config(state=tk.NORMAL)
        
        # Update status
        self.status_label.config(text="Recording Saved", fg=self.success_color)
        self.indicator_canvas.itemconfig(self.indicator, fill=self.success_color)
        
        # Show completion message
        response = messagebox.askyesno(
            "Recording Complete",
            f"Recording saved successfully!\n\n"
            f"File: {self.filename_var.get()}\n"
            f"Duration: {self.duration_var.get()}\n"
            f"Frames: {self.frames_var.get()}\n"
            f"Size: {self.file_size_var.get()}\n\n"
            f"Would you like to open the folder?",
            icon='info'
        )
        
        if response:
            self.open_save_folder()
            
        # Reset after delay
        self.root.after(3000, self.reset_ui)
        
    def reset_ui(self):
        """Reset UI to ready state"""
        self.status_label.config(text="Ready to Record", fg=self.text_color)
        self.indicator_canvas.itemconfig(self.indicator, fill="#666666")
        self.duration_var.set("00:00:00")
        self.frames_var.set("0")
        self.file_size_var.set("0 MB")
        
    def open_save_folder(self):
        """Open the save folder"""
        import subprocess
        import platform
        
        path = self.save_path_var.get()
        
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", path])
        else:  # Linux
            subprocess.Popen(["xdg-open", path])
            
    def update_timer(self):
        """Update recording timer"""
        if self.is_recording and not self.is_paused:
            elapsed = time.time() - self.start_time - self.pause_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            self.duration_var.set(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        
        self.root.after(1000, self.update_timer)
        
    def blink_indicator(self):
        """Blink recording indicator"""
        if self.is_recording and not self.is_paused:
            current_color = self.indicator_canvas.itemcget(self.indicator, "fill")
            new_color = "#ff8888" if current_color == self.record_color else self.record_color
            self.indicator_canvas.itemconfig(self.indicator, fill=new_color)
            self.root.after(500, self.blink_indicator)

    # Add warning color for pause state
    warning_color = "#ffa500"

def main():
    root = tk.Tk()
    app = ScreenRecorder(root)
    
    # Handle window close
    def on_closing():
        if app.is_recording:
            response = messagebox.askyesno(
                "Recording in Progress",
                "Recording is in progress. Stop recording and exit?",
                icon='warning'
            )
            if response:
                app.stop_recording()
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()