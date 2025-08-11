import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
import pyperclip

# Function to generate QR Code
def generate_qr():
    text = qr_input.get()
    
    if text:
        qr = qrcode.QRCode(
            version=1, 
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10, 
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        img = qr.make_image(fill='black', back_color='white')
        
        # Convert to ImageTk for Tkinter
        img_tk = ImageTk.PhotoImage(img)
        
        # Show in label
        qr_label.config(image=img_tk)
        qr_label.image = img_tk  # Keep a reference to avoid garbage collection
        
    else:
        messagebox.showerror("Input Error", "Please enter text to generate a QR code.")

# Function to decode QR Code from image (file upload)
def decode_qr_from_file():
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    
    if file_path:
        img = Image.open(file_path)
        qr_data = decode(img)
        
        if qr_data:
            result = qr_data[0].data.decode('utf-8')
            qr_result.delete(1.0, tk.END)  # Clear previous result
            qr_result.insert(tk.END, result)
        else:
            messagebox.showerror("Decode Error", "No QR code found in the image.")
    
# Function to decode QR code from clipboard
def decode_qr_from_clipboard():
    try:
        clipboard_text = pyperclip.paste()
        img = Image.open(clipboard_text)
        qr_data = decode(img)
        
        if qr_data:
            result = qr_data[0].data.decode('utf-8')
            qr_result.delete(1.0, tk.END)  # Clear previous result
            qr_result.insert(tk.END, result)
        else:
            messagebox.showerror("Decode Error", "No QR code found in the clipboard image.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to decode from clipboard: {e}")

# Set up the Tkinter window
root = tk.Tk()
root.title("QR Code Reader & Generator")
root.geometry("500x500")

# Label for the input text for QR code generation
input_label = tk.Label(root, text="Enter text to generate QR Code:")
input_label.pack(pady=10)

# Entry widget for the QR code input
qr_input = tk.Entry(root, width=50)
qr_input.pack(pady=10)

# Button to generate QR Code
generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr)
generate_button.pack(pady=10)

# Label to display the generated QR code
qr_label = tk.Label(root)
qr_label.pack(pady=20)

# Button to decode QR code from file
file_button = tk.Button(root, text="Decode QR from File", command=decode_qr_from_file)
file_button.pack(pady=10)

# Button to decode QR code from clipboard
clipboard_button = tk.Button(root, text="Decode QR from Clipboard", command=decode_qr_from_clipboard)
clipboard_button.pack(pady=10)

# Label and Textbox to show decoded QR result
qr_result_label = tk.Label(root, text="Decoded QR Code Data:")
qr_result_label.pack(pady=10)

qr_result = tk.Text(root, height=5, width=50)
qr_result.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()
