import unittest
from ..security.validation import validate_passwords, validate_dialpad

class TestSecurity(unittest.TestCase):
    def test_validate_passwords(self):
        self.assertTrue(validate_passwords(["a", "b", "c", "d"]))

    def test_validate_dialpad(self):
        self.assertTrue(validate_dialpad([2, 3, 5]))

if __name__ == '__main__':
    unittest.main()