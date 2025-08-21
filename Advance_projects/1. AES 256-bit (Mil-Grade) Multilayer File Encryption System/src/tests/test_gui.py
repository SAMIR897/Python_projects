import unittest
from ..gui.main_gui import MainGUI
import tkinter as tk

class TestGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = MainGUI(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_init(self):
        self.assertIsNotNone(self.app)

if __name__ == '__main__':
    unittest.main()