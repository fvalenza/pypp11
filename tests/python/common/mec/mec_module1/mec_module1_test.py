import unittest
import os

from pypp11.common.mec.converter.converter import str_to_bool


is_python_module_built = str_to_bool(os.environ["BUILD_MEC_MODULE1_PYTHON"])
is_cpp_module_built = str_to_bool(os.environ["BUILD_MEC_MODULE1_CPP"])

if(is_python_module_built):
  from pypp11.common.mec import mec_module1


class MainTest(unittest.TestCase):
  if(is_python_module_built):
    def test_python_mec1(self):
      # test that 1 + 1 = 2
      self.assertEqual(1 + 1, 2)

    if(is_cpp_module_built):
      def test_add(self):
        # test that 1 + 1 = 2
        self.assertEqual(mec_module1.cpp.add(1, 1), 2)


if __name__ == '__main__':
    unittest.main()
