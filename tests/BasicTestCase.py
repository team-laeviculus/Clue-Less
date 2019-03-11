import unittest

def dummy_func(x):
    return x + 1


class MyBasicUnitTest(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(dummy_func(0), 1)
        self.assertEqual(dummy_func(1), 2)
        self.assertEqual(dummy_func(-1),0)
    def test_failure(self):
        # Shows what happens when a test fails
        self.assertEqual(dummy_func(-1),1)


if __name__ == "__main__":
    # Start running registered unit tests
    unittest.main()