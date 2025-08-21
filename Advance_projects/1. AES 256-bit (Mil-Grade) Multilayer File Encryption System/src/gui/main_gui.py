import tkinter as tk
from .password_layer import PasswordLayer
from .encryption_ui import EncryptionUI

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AES-256 Encryption")
        self.password_layer = PasswordLayer(root, self.on_password_complete)
        self.encryption_ui = None

    def on_password_complete(self):
        self.password_layer.destroy()
        self.encryption_ui = EncryptionUI(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()