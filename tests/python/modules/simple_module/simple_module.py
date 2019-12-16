import unittest
# import our `pybind11`-based extension module from package python_cpp_example
from pypp11.modules.simple_module import SimpleModule
import numpy as np


class MainTest(unittest.TestCase):
    def test_dummy(self):
        # dummy scenario
        self.assertEqual(1 + 1, 2)


if __name__ == '__main__':
    unittest.main()
