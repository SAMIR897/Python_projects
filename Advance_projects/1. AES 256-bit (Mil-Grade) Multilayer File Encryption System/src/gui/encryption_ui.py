import tkinter as tk
from .file_selector import select_file_or_folder
from ..compression.compress import compress_file_or_folder
from ..aes.aes_core import aes_encrypt

class EncryptionUI:
    def __init__(self, root):
        self.root = root
        tk.Button(root, text="Select File/Folder", command=self.select).pack()
        self.result = tk.Label(root, text="")
        self.result.pack()

    def select(self):
        path = select_file_or_folder()
        if path:
            compressed = compress_file_or_folder(path)
            with open(compressed, "rb") as f:
                data = f.read()
            encrypted = aes_encrypt(data, b"256-bit-key-here")  # Placeholder key
            with open(path + ".enc", "wb") as f:
                f.write(encrypted)
            self.result.config(text=f"Encrypted: {path}.enc")