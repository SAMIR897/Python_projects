import unittest
from ..aes.aes_core import aes_encrypt

class TestAES(unittest.TestCase):
    def test_encrypt(self):
        key = bytes([0] * 32)  # 256-bit key
        plaintext = bytes([0] * 16)  # 128-bit block
        ciphertext = aes_encrypt(plaintext, key)
        self.assertEqual(len(ciphertext), 16)

if __name__ == '__main__':
    unittest.main()