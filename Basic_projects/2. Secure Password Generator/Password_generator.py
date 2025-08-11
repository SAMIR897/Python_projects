import random
import string
from tkinter import *
from tkinter.ttk import Combobox
import pyperclip

# Initialize Window
root = Tk()
root.title("Ultimate Password Generator")
root.geometry("550x750")
root.minsize(500, 700)
root.config(bg="#f5f7fa")

# Color Palette
PRIMARY = "#6C63FF"  # Vibrant purple
SECONDARY = "#4A90E2"  # Nice blue
ACCENT = "#FF6584"
LIGHT_BG = "#f5f7fa"
DARK_TEXT = "#2d3436"
BUTTON_HOVER = "#5A4FCF"  # Darker purple for hover

# Variables
output_pass = StringVar()
use_upper = BooleanVar(value=True)
use_lower = BooleanVar(value=True)
use_digits = BooleanVar(value=True)
use_special = BooleanVar(value=True)
pass_len = IntVar(value=16)

# Validation for positive integers
def validate_positive_int_input(P):
    if P == "" or (P.isdigit() and int(P) > 0):
        return True
    else:
        return False

# Register the validation function
vcmd = root.register(validate_positive_int_input)

def generate_password():
    # Validate the password length
    if pass_len.get() <= 0:
        output_pass.set("Error: Password length must be a positive integer!")
        return
    if not isinstance(pass_len.get(), int):
        output_pass.set("Error: Invalid input. Please enter a valid integer.")
        return

    # Selected character types
    selected = []
    if use_upper.get():
        selected.append(string.ascii_uppercase)
    if use_lower.get():
        selected.append(string.ascii_lowercase)
    if use_digits.get():
        selected.append(string.digits)
    if use_special.get():
        selected.append(string.punctuation)

    if not selected:
        output_pass.set("Please select at least one character type")
        return

    password = []
    for charset in selected:
        password.append(random.choice(charset))
    
    remaining_length = pass_len.get() - len(selected)
    for _ in range(remaining_length):
        charset = random.choice(selected)
        password.append(random.choice(charset))
    
    random.shuffle(password)
    output_pass.set(''.join(password))

def copy_to_clipboard():
    pyperclip.copy(output_pass.get())

def on_enter(e):
    e.widget.config(background=BUTTON_HOVER)

def on_leave(e):
    e.widget.config(background=PRIMARY)

# Main Frame
main_frame = Frame(root, bg=LIGHT_BG)
main_frame.pack(expand=True, fill=BOTH, padx=20, pady=20)

# Header Section
header_frame = Frame(main_frame, bg=LIGHT_BG)
header_frame.pack(fill=X)

canvas = Canvas(header_frame, width=60, height=60, bg=LIGHT_BG, highlightthickness=0)
canvas.pack(side=LEFT, padx=(0,10))
# Draw padlock icon
canvas.create_oval(10,10,50,50, fill=PRIMARY, outline="")
canvas.create_rectangle(25,20,35,50, fill=LIGHT_BG, outline="")
canvas.create_rectangle(15,30,45,40, fill=LIGHT_BG, outline="")

Label(header_frame, text="ULTIMATE\nPASSWORD GENERATOR", 
      font=("Segoe UI", 16, "bold"), bg=LIGHT_BG, fg=DARK_TEXT,
      justify=LEFT).pack(side=LEFT)

# Length Control
length_frame = Frame(main_frame, bg=LIGHT_BG)
length_frame.pack(fill=X, pady=15)

Label(length_frame, text="Password Length:", bg=LIGHT_BG,
     font=("Segoe UI", 12), fg=DARK_TEXT).pack(side=LEFT)

# Create ComboBox for password length (1-100)
length_combobox = Combobox(length_frame, width=10, state="normal", 
                            font=("Segoe UI", 12), validate="key", 
                            validatecommand=(vcmd, '%P'))

# Populate Combobox with values from 1 to 100
length_combobox['values'] = [str(i) for i in range(1, 101)]
length_combobox.set("16")  # Default to 16
length_combobox.pack(side=LEFT, padx=10)

# Update the pass_len variable when combobox or input changes
def on_combobox_change(event):
    try:
        pass_len.set(int(length_combobox.get()))
    except ValueError:
        pass_len.set(16)  # Default to 16 if the input is invalid

# Bind the event for selecting from the dropdown
length_combobox.bind("<<ComboboxSelected>>", on_combobox_change)

# Bind the event for manual input changes (typing in the combobox)
length_combobox.bind("<KeyRelease>", on_combobox_change)

# Character Options
options_frame = LabelFrame(main_frame, text=" CHARACTER TYPES ", 
                         font=("Segoe UI", 12, "bold"), fg=PRIMARY,
                         bg=LIGHT_BG, bd=2, relief="groove",
                         padx=15, pady=10)
options_frame.pack(fill=X, pady=10)

def create_option_checkbox(parent, text, variable, color):
    return Checkbutton(parent, text=text, variable=variable,
                      font=("Segoe UI", 11), bg=LIGHT_BG, fg=DARK_TEXT,
                      activebackground=LIGHT_BG, activeforeground=DARK_TEXT,
                      selectcolor=color)

create_option_checkbox(options_frame, "Uppercase Letters (A-Z)", use_upper, "#FF9AA2").pack(anchor='w', pady=3)
create_option_checkbox(options_frame, "Lowercase Letters (a-z)", use_lower, "#FFB7B2").pack(anchor='w', pady=3)
create_option_checkbox(options_frame, "Digits (0-9)", use_digits, "#FFDAC1").pack(anchor='w', pady=3)
create_option_checkbox(options_frame, "Special Characters (!@#$)", use_special, "#E2F0CB").pack(anchor='w', pady=3)

# Generate Button (PURPLE)
generate_btn = Button(main_frame, text="GENERATE PASSWORD", command=generate_password,
                    font=("Segoe UI", 12, "bold"), bg=PRIMARY, fg="white",
                    activebackground=BUTTON_HOVER, activeforeground="white",
                    padx=30, pady=10, bd=0, highlightthickness=0)
generate_btn.pack(pady=20)
generate_btn.bind("<Enter>", on_enter)
generate_btn.bind("<Leave>", on_leave)

# Password Display
output_frame = Frame(main_frame, bg=LIGHT_BG)
output_frame.pack(fill=X, pady=10)

Label(output_frame, text="Your Password:", bg=LIGHT_BG,
     font=("Segoe UI", 11), fg=DARK_TEXT).pack()

output_entry = Entry(output_frame, textvariable=output_pass,
                    font=("Consolas", 14), bd=2, relief="solid",
                    width=40, justify='center', state='readonly',
                    readonlybackground="white", fg=PRIMARY)
output_entry.pack(pady=10, ipady=8)

# Copy Button (PURPLE)
copy_btn = Button(main_frame, text="COPY TO CLIPBOARD", command=copy_to_clipboard,
                font=("Segoe UI", 12, "bold"), bg=PRIMARY, fg="white",
                activebackground=BUTTON_HOVER, activeforeground="white",
                padx=30, pady=10, bd=0, highlightthickness=0)
copy_btn.pack(pady=15)
copy_btn.bind("<Enter>", lambda e: copy_btn.config(background=BUTTON_HOVER))
copy_btn.bind("<Leave>", lambda e: copy_btn.config(background=PRIMARY))

root.mainloop()
