import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import json
import os
from datetime import datetime
import time

# Try to import speedtest module
try:
    import speedtest
except ImportError:
    speedtest = None

class InternetSpeedChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Internet Speed Checker")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Configure colors
        self.bg_color = "#1a1a2e"
        self.secondary_bg = "#16213e"
        self.accent_color = "#0f3460"
        self.highlight_color = "#00d4ff"
        self.success_color = "#00ff88"
        self.warning_color = "#ffa500"
        self.text_color = "#ffffff"
        
        self.root.configure(bg=self.bg_color)
        
        # Variables
        self.download_speed = tk.StringVar(value="0.00")
        self.upload_speed = tk.StringVar(value="0.00")
        self.ping_value = tk.StringVar(value="0")
        self.isp_name = tk.StringVar(value="Unknown")
        self.ip_address = tk.StringVar(value="0.0.0.0")
        self.server_location = tk.StringVar(value="Unknown")
        
        # Testing state
        self.is_testing = False
        
        # Queue for thread communication
        self.msg_queue = queue.Queue()
        
        # History file
        self.history_file = "speed_history.json"
        self.history = self.load_history()
        
        # Create GUI
        self.create_gui()
        
        # Center window
        self.center_window()
        
        # Check if speedtest is installed
        if speedtest is None:
            self.show_installation_dialog()
        
        # Start queue processing
        self.process_queue()
        
    def create_gui(self):
        """Create the main GUI"""
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ===== HEADER =====
        header_frame = tk.Frame(main_frame, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="⚡ Internet Speed Checker",
            font=("Arial", 28, "bold"),
            bg=self.bg_color,
            fg=self.highlight_color
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Test your internet connection speed",
            font=("Arial", 11),
            bg=self.bg_color,
            fg="#888888"
        )
        subtitle_label.pack(pady=(5, 0))
        
        # ===== CONNECTION INFO CARD =====
        info_card = tk.Frame(main_frame, bg=self.secondary_bg, relief=tk.FLAT)
        info_card.pack(fill=tk.X, pady=(0, 20))
        
        info_inner = tk.Frame(info_card, bg=self.secondary_bg)
        info_inner.pack(padx=20, pady=15)
        
        # ISP Info
        isp_frame = tk.Frame(info_inner, bg=self.secondary_bg)
        isp_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            isp_frame,
            text="🌐 ISP",
            font=("Arial", 10),
            bg=self.secondary_bg,
            fg="#888888"
        ).pack()
        
        tk.Label(
            isp_frame,
            textvariable=self.isp_name,
            font=("Arial", 12, "bold"),
            bg=self.secondary_bg,
            fg=self.text_color
        ).pack()
        
        # IP Address
        ip_frame = tk.Frame(info_inner, bg=self.secondary_bg)
        ip_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            ip_frame,
            text="📍 IP Address",
            font=("Arial", 10),
            bg=self.secondary_bg,
            fg="#888888"
        ).pack()
        
        tk.Label(
            ip_frame,
            textvariable=self.ip_address,
            font=("Arial", 12, "bold"),
            bg=self.secondary_bg,
            fg=self.text_color
        ).pack()
        
        # Server Location
        server_frame = tk.Frame(info_inner, bg=self.secondary_bg)
        server_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            server_frame,
            text="🖥️ Server",
            font=("Arial", 10),
            bg=self.secondary_bg,
            fg="#888888"
        ).pack()
        
        tk.Label(
            server_frame,
            textvariable=self.server_location,
            font=("Arial", 12, "bold"),
            bg=self.secondary_bg,
            fg=self.text_color
        ).pack()
        
        # ===== SPEED DISPLAY CARDS =====
        cards_frame = tk.Frame(main_frame, bg=self.bg_color)
        cards_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Download Card
        self.download_card = self.create_speed_card(
            cards_frame,
            "⬇️ DOWNLOAD",
            self.download_speed,
            "Mbps",
            side=tk.LEFT
        )
        
        # Ping Card
        self.ping_card = self.create_speed_card(
            cards_frame,
            "📡 PING",
            self.ping_value,
            "ms",
            side=tk.LEFT
        )
        
        # Upload Card
        self.upload_card = self.create_speed_card(
            cards_frame,
            "⬆️ UPLOAD",
            self.upload_speed,
            "Mbps",
            side=tk.LEFT
        )
        
        # ===== PROGRESS BAR =====
        progress_frame = tk.Frame(main_frame, bg=self.bg_color)
        progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.progress_label = tk.Label(
            progress_frame,
            text="Ready to test",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#888888"
        )
        self.progress_label.pack()
        
        # Custom progress bar style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=self.secondary_bg,
            background=self.highlight_color,
            bordercolor=self.bg_color,
            lightcolor=self.highlight_color,
            darkcolor=self.highlight_color
        )
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            style="Custom.Horizontal.TProgressbar",
            length=500
        )
        self.progress_bar.pack(pady=10)
        
        # ===== IMPROVED CONTROL BUTTONS =====
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(pady=(0, 20))
        
        # Start Test Button - More visible with gradient-like effect
        start_btn_container = tk.Frame(button_frame, bg="#00e5ff", highlightthickness=0)
        start_btn_container.pack(side=tk.LEFT, padx=10)
        
        self.start_button = tk.Button(
            start_btn_container,
            text="🚀 START SPEED TEST",
            command=self.start_speed_test,
            bg="#00bcd4",
            fg="#000000",  # Black text for better contrast
            font=("Arial", 14, "bold"),
            padx=35,
            pady=18,
            cursor="hand2",
            relief=tk.RAISED,
            bd=3,
            activebackground="#00e5ff",
            activeforeground="#000000"
        )
        self.start_button.pack(padx=2, pady=2)
        
        # Add hover effects
        self.start_button.bind("<Enter>", lambda e: self.on_button_hover(self.start_button, "#00e5ff", "#000000"))
        self.start_button.bind("<Leave>", lambda e: self.on_button_leave(self.start_button, "#00bcd4", "#000000"))
        
        # History Button - More visible with different color
        history_btn_container = tk.Frame(button_frame, bg="#ffa726", highlightthickness=0)
        history_btn_container.pack(side=tk.LEFT, padx=10)
        
        self.history_button = tk.Button(
            history_btn_container,
            text="📊 VIEW HISTORY",
            command=self.show_history,
            bg="#ff9800",
            fg="#000000",  # Black text for better contrast
            font=("Arial", 13, "bold"),
            padx=30,
            pady=18,
            cursor="hand2",
            relief=tk.RAISED,
            bd=3,
            activebackground="#ffa726",
            activeforeground="#000000"
        )
        self.history_button.pack(padx=2, pady=2)
        
        # Add hover effects
        self.history_button.bind("<Enter>", lambda e: self.on_button_hover(self.history_button, "#ffa726", "#000000"))
        self.history_button.bind("<Leave>", lambda e: self.on_button_leave(self.history_button, "#ff9800", "#000000"))
        
        # ===== HISTORY DISPLAY =====
        history_label = tk.Label(
            main_frame,
            text="📜 Recent Tests",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            anchor="w"
        )
        history_label.pack(fill=tk.X, pady=(10, 5))
        
        # History frame with scrollbar
        history_container = tk.Frame(main_frame, bg=self.secondary_bg, relief=tk.FLAT)
        history_container.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(history_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # History listbox
        self.history_listbox = tk.Listbox(
            history_container,
            yscrollcommand=scrollbar.set,
            bg=self.secondary_bg,
            fg=self.text_color,
            font=("Courier", 9),
            relief=tk.FLAT,
            highlightthickness=0,
            selectbackground=self.accent_color,
            selectforeground=self.text_color,
            height=6
        )
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Load history into listbox
        self.update_history_display()
        
        # ===== FOOTER =====
        footer_frame = tk.Frame(main_frame, bg=self.bg_color)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        footer_label = tk.Label(
            footer_frame,
            text="💡 Tip: Close other applications for accurate results",
            font=("Arial", 9, "italic"),
            bg=self.bg_color,
            fg="#666666"
        )
        footer_label.pack()
    
    def on_button_hover(self, button, hover_bg, hover_fg):
        """Button hover effect"""
        if button['state'] != tk.DISABLED:
            button.config(bg=hover_bg, fg=hover_fg)
    
    def on_button_leave(self, button, normal_bg, normal_fg):
        """Button leave effect"""
        if button['state'] != tk.DISABLED:
            button.config(bg=normal_bg, fg=normal_fg)
        
    def create_speed_card(self, parent, title, variable, unit, side):
        """Create a speed display card"""
        card = tk.Frame(parent, bg=self.secondary_bg, relief=tk.FLAT)
        card.pack(side=side, padx=10, fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(
            card,
            text=title,
            font=("Arial", 11, "bold"),
            bg=self.secondary_bg,
            fg="#888888"
        ).pack(pady=(15, 5))
        
        # Value frame
        value_frame = tk.Frame(card, bg=self.secondary_bg)
        value_frame.pack()
        
        # Speed value
        tk.Label(
            value_frame,
            textvariable=variable,
            font=("Arial", 36, "bold"),
            bg=self.secondary_bg,
            fg=self.success_color
        ).pack(side=tk.LEFT)
        
        # Unit
        tk.Label(
            value_frame,
            text=f" {unit}",
            font=("Arial", 16),
            bg=self.secondary_bg,
            fg="#888888"
        ).pack(side=tk.LEFT, anchor="s", pady=8)
        
        # Spacer
        tk.Label(card, text="", bg=self.secondary_bg, height=1).pack()
        
        return card
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def show_installation_dialog(self):
        """Show dialog if speedtest module is not installed"""
        response = messagebox.askyesno(
            "Module Not Found",
            "The 'speedtest-cli' module is not installed.\n\n"
            "This module is required for speed testing.\n\n"
            "Install it using:\n"
            "pip install speedtest-cli\n\n"
            "Would you like to see installation instructions?",
            icon='warning'
        )
        
        if response:
            self.show_installation_instructions()
            
    def show_installation_instructions(self):
        """Show installation instructions window"""
        inst_window = tk.Toplevel(self.root)
        inst_window.title("Installation Instructions")
        inst_window.geometry("600x400")
        inst_window.configure(bg=self.bg_color)
        inst_window.transient(self.root)
        inst_window.grab_set()
        
        # Center the window
        inst_window.update_idletasks()
        x = (inst_window.winfo_screenwidth() // 2) - 300
        y = (inst_window.winfo_screenheight() // 2) - 200
        inst_window.geometry(f'600x400+{x}+{y}')
        
        frame = tk.Frame(inst_window, bg=self.bg_color)
        frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        tk.Label(
            frame,
            text="📦 Installation Instructions",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg=self.highlight_color
        ).pack(pady=(0, 20))
        
        instructions = """
To use this application, you need to install the speedtest-cli module.

Step 1: Open your terminal/command prompt

Step 2: Run one of these commands:

    pip install speedtest-cli
    
    OR
    
    pip3 install speedtest-cli
    
    OR (if above don't work)
    
    python -m pip install speedtest-cli

Step 3: Restart this application

That's it! You're ready to test your internet speed.
"""
        
        text_widget = tk.Text(
            frame,
            font=("Courier", 10),
            bg=self.secondary_bg,
            fg=self.text_color,
            relief=tk.FLAT,
            padx=15,
            pady=15,
            wrap=tk.WORD
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert("1.0", instructions)
        text_widget.config(state=tk.DISABLED)
        
        tk.Button(
            frame,
            text="Close",
            command=inst_window.destroy,
            bg=self.accent_color,
            fg=self.text_color,
            font=("Arial", 11),
            padx=30,
            pady=10,
            cursor="hand2",
            relief=tk.FLAT
        ).pack(pady=(15, 0))
        
    def start_speed_test(self):
        """Start the speed test in a background thread"""
        if speedtest is None:
            messagebox.showerror(
                "Error",
                "speedtest-cli module is not installed!\n\n"
                "Please install it using:\n"
                "pip install speedtest-cli"
            )
            return
            
        if self.is_testing:
            messagebox.showwarning("Warning", "A speed test is already running!")
            return
            
        # Reset values
        self.download_speed.set("0.00")
        self.upload_speed.set("0.00")
        self.ping_value.set("0")
        
        # Disable button
        self.start_button.config(
            state=tk.DISABLED, 
            text="⏳ Testing...",
            bg="#607d8b",
            fg="#ffffff"
        )
        self.history_button.config(state=tk.DISABLED)
        
        # Start progress bar
        self.progress_bar.start(10)
        
        # Set testing flag
        self.is_testing = True
        
        # Start test in background thread
        thread = threading.Thread(target=self.run_speed_test, daemon=True)
        thread.start()
        
    def run_speed_test(self):
        """Run the actual speed test (in background thread)"""
        try:
            # Update status
            self.msg_queue.put(('status', 'Initializing speed test...'))
            
            # Create Speedtest object
            st = speedtest.Speedtest()
            
            # Get server info
            self.msg_queue.put(('status', 'Finding best server...'))
            st.get_best_server()
            
            server = st.results.server
            self.msg_queue.put(('server_info', {
                'location': f"{server['name']}, {server['country']}",
                'sponsor': server['sponsor']
            }))
            
            # Get ISP and IP
            self.msg_queue.put(('isp_info', {
                'isp': st.results.client['isp'],
                'ip': st.results.client['ip']
            }))
            
            # Test ping
            self.msg_queue.put(('status', 'Testing ping...'))
            ping = st.results.ping
            self.msg_queue.put(('ping', round(ping, 2)))
            
            # Test download speed
            self.msg_queue.put(('status', 'Testing download speed...'))
            download = st.download() / 1_000_000  # Convert to Mbps
            self.msg_queue.put(('download', round(download, 2)))
            
            # Test upload speed
            self.msg_queue.put(('status', 'Testing upload speed...'))
            upload = st.upload() / 1_000_000  # Convert to Mbps
            self.msg_queue.put(('upload', round(upload, 2)))
            
            # Save to history
            self.save_test_result(download, upload, ping, server)
            
            # Complete
            self.msg_queue.put(('status', 'Speed test completed!'))
            self.msg_queue.put(('complete', True))
            
        except Exception as e:
            self.msg_queue.put(('error', str(e)))
            self.msg_queue.put(('complete', False))
            
    def process_queue(self):
        """Process messages from the background thread"""
        try:
            while True:
                msg_type, msg_data = self.msg_queue.get_nowait()
                
                if msg_type == 'status':
                    self.progress_label.config(text=msg_data, fg=self.warning_color)
                    
                elif msg_type == 'server_info':
                    self.server_location.set(msg_data['location'])
                    
                elif msg_type == 'isp_info':
                    self.isp_name.set(msg_data['isp'])
                    self.ip_address.set(msg_data['ip'])
                    
                elif msg_type == 'ping':
                    self.ping_value.set(str(msg_data))
                    
                elif msg_type == 'download':
                    self.download_speed.set(f"{msg_data:.2f}")
                    
                elif msg_type == 'upload':
                    self.upload_speed.set(f"{msg_data:.2f}")
                    
                elif msg_type == 'error':
                    self.progress_label.config(text=f"Error: {msg_data}", fg="#ff4444")
                    messagebox.showerror("Speed Test Error", f"An error occurred:\n\n{msg_data}")
                    
                elif msg_type == 'complete':
                    self.is_testing = False
                    self.progress_bar.stop()
                    self.start_button.config(
                        state=tk.NORMAL, 
                        text="🚀 START SPEED TEST",
                        bg="#00bcd4",
                        fg="#000000"
                    )
                    self.history_button.config(state=tk.NORMAL)
                    
                    if msg_data:  # Success
                        self.progress_label.config(text="✓ Speed test completed successfully!", fg=self.success_color)
                        self.update_history_display()
                    else:  # Error
                        self.progress_label.config(text="✗ Speed test failed", fg="#ff4444")
                        
        except queue.Empty:
            pass
            
        # Schedule next check
        self.root.after(100, self.process_queue)
        
    def save_test_result(self, download, upload, ping, server):
        """Save test result to history"""
        result = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'download': round(download, 2),
            'upload': round(upload, 2),
            'ping': round(ping, 2),
            'server': f"{server['name']}, {server['country']}",
            'isp': self.isp_name.get()
        }
        
        self.history.insert(0, result)
        
        # Keep only last 50 results
        if len(self.history) > 50:
            self.history = self.history[:50]
            
        # Save to file
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
            
    def load_history(self):
        """Load history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
        
    def update_history_display(self):
        """Update the history listbox"""
        self.history_listbox.delete(0, tk.END)
        
        if not self.history:
            self.history_listbox.insert(tk.END, "  No tests recorded yet. Run your first speed test!")
            return
            
        for result in self.history[:10]:  # Show last 10
            text = f"  {result['timestamp']} | ⬇️ {result['download']:6.2f} Mbps | ⬆️ {result['upload']:6.2f} Mbps | 📡 {result['ping']:5.2f} ms"
            self.history_listbox.insert(tk.END, text)
            
    def show_history(self):
        """Show full history in a new window"""
        if not self.history:
            messagebox.showinfo("No History", "No speed tests have been recorded yet.")
            return
            
        # Create history window
        hist_window = tk.Toplevel(self.root)
        hist_window.title("Speed Test History")
        hist_window.geometry("900x600")
        hist_window.configure(bg=self.bg_color)
        hist_window.transient(self.root)
        
        # Center window
        hist_window.update_idletasks()
        x = (hist_window.winfo_screenwidth() // 2) - 450
        y = (hist_window.winfo_screenheight() // 2) - 300
        hist_window.geometry(f'900x600+{x}+{y}')
        
        # Header
        header = tk.Frame(hist_window, bg=self.bg_color)
        header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            header,
            text="📊 Complete Speed Test History",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg=self.highlight_color
        ).pack()
        
        # Stats frame
        stats_frame = tk.Frame(hist_window, bg=self.secondary_bg)
        stats_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        avg_download = sum(r['download'] for r in self.history) / len(self.history)
        avg_upload = sum(r['upload'] for r in self.history) / len(self.history)
        avg_ping = sum(r['ping'] for r in self.history) / len(self.history)
        
        stats_inner = tk.Frame(stats_frame, bg=self.secondary_bg)
        stats_inner.pack(pady=15)
        
        self.create_stat_item(stats_inner, "Total Tests", str(len(self.history)), "📈")
        self.create_stat_item(stats_inner, "Avg Download", f"{avg_download:.2f} Mbps", "⬇️")
        self.create_stat_item(stats_inner, "Avg Upload", f"{avg_upload:.2f} Mbps", "⬆️")
        self.create_stat_item(stats_inner, "Avg Ping", f"{avg_ping:.2f} ms", "📡")
        
        # Treeview for history
        tree_frame = tk.Frame(hist_window, bg=self.bg_color)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure treeview style
        style = ttk.Style()
        style.configure(
            "Custom.Treeview",
            background=self.secondary_bg,
            foreground=self.text_color,
            fieldbackground=self.secondary_bg,
            borderwidth=0
        )
        style.configure("Custom.Treeview.Heading", background=self.accent_color, foreground=self.text_color, font=("Arial", 10, "bold"))
        style.map('Custom.Treeview', background=[('selected', self.accent_color)])
        
        # Create treeview
        columns = ('timestamp', 'download', 'upload', 'ping', 'server', 'isp')
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set,
            style="Custom.Treeview"
        )
        
        # Define headings
        tree.heading('timestamp', text='Date & Time')
        tree.heading('download', text='Download (Mbps)')
        tree.heading('upload', text='Upload (Mbps)')
        tree.heading('ping', text='Ping (ms)')
        tree.heading('server', text='Server')
        tree.heading('isp', text='ISP')
        
        # Define column widths
        tree.column('timestamp', width=150)
        tree.column('download', width=120)
        tree.column('upload', width=120)
        tree.column('ping', width=100)
        tree.column('server', width=200)
        tree.column('isp', width=150)
        
        # Insert data
        for result in self.history:
            tree.insert('', tk.END, values=(
                result['timestamp'],
                f"{result['download']:.2f}",
                f"{result['upload']:.2f}",
                f"{result['ping']:.2f}",
                result['server'],
                result['isp']
            ))
            
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=tree.yview)
        
        # Buttons
        button_frame = tk.Frame(hist_window, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Clear History Button - More visible
        clear_btn_container = tk.Frame(button_frame, bg="#ff5252", highlightthickness=0)
        clear_btn_container.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(
            clear_btn_container,
            text="🗑️ CLEAR HISTORY",
            command=lambda: self.clear_history(hist_window),
            bg="#f44336",
            fg="#ffffff",
            font=("Arial", 11, "bold"),
            padx=25,
            pady=12,
            cursor="hand2",
            relief=tk.RAISED,
            bd=2
        )
        clear_btn.pack(padx=2, pady=2)
        clear_btn.bind("<Enter>", lambda e: clear_btn.config(bg="#ff5252"))
        clear_btn.bind("<Leave>", lambda e: clear_btn.config(bg="#f44336"))
        
        # Close Button - More visible
        close_btn_container = tk.Frame(button_frame, bg="#66bb6a", highlightthickness=0)
        close_btn_container.pack(side=tk.RIGHT, padx=5)
        
        close_btn = tk.Button(
            close_btn_container,
            text="✓ CLOSE",
            command=hist_window.destroy,
            bg="#4caf50",
            fg="#ffffff",
            font=("Arial", 11, "bold"),
            padx=35,
            pady=12,
            cursor="hand2",
            relief=tk.RAISED,
            bd=2
        )
        close_btn.pack(padx=2, pady=2)
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg="#66bb6a"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg="#4caf50"))
        
    def create_stat_item(self, parent, label, value, icon):
        """Create a statistics item"""
        frame = tk.Frame(parent, bg=self.secondary_bg)
        frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            frame,
            text=f"{icon} {label}",
            font=("Arial", 9),
            bg=self.secondary_bg,
            fg="#888888"
        ).pack()
        
        tk.Label(
            frame,
            text=value,
            font=("Arial", 14, "bold"),
            bg=self.secondary_bg,
            fg=self.success_color
        ).pack()
        
    def clear_history(self, window):
        """Clear all history"""
        response = messagebox.askyesno(
            "Clear History",
            "Are you sure you want to delete all speed test history?\n\nThis action cannot be undone.",
            icon='warning',
            parent=window
        )
        
        if response:
            self.history = []
            try:
                if os.path.exists(self.history_file):
                    os.remove(self.history_file)
            except:
                pass
            self.update_history_display()
            window.destroy()
            messagebox.showinfo("Success", "History cleared successfully!")

def main():
    root = tk.Tk()
    app = InternetSpeedChecker(root)
    root.mainloop()

if __name__ == "__main__":
    main()