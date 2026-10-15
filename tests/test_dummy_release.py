"""Standard-library tests for the synthetic package."""

import unittest

from dummy_release import greet


class GreetingTests(unittest.TestCase):
    def test_named_greeting(self):
        self.assertEqual(greet("Ada"), "Hello, Ada!")

    def test_empty_name(self):
        self.assertEqual(greet(""), "Hello, !")

    def test_optional_emphasis(self):
        self.assertEqual(greet("Ada", excited=True), "Hello, Ada!!")


if __name__ == "__main__":
    unittest.main()
