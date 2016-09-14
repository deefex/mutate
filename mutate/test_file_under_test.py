# Standard Imports
import unittest

# Local Imports
import file_under_test


class TestIt(unittest.TestCase):

    def test_something(self):
        assert file_under_test.is_leap_year(2000) == True

if __name__ == '__main__':
    unittest.main()
