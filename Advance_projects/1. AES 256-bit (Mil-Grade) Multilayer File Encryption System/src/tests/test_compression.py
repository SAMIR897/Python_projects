import unittest
from ..compression.compress import compress_file_or_folder
from ..compression.decompress import decompress_file
import os

class TestCompression(unittest.TestCase):
    def test_compress_decompress(self):
        test_file = "test.txt"
        with open(test_file, "w") as f:
            f.write("test")
        zip_path = compress_file_or_folder(test_file)
        decompress_file(zip_path, ".")
        self.assertTrue(os.path.exists("test.txt"))
        os.remove(test_file)
        os.remove(zip_path)

if __name__ == '__main__':
    unittest.main()