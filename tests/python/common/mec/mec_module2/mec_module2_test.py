import unittest
import os


from pypp11.common.mec.converter.converter import str_to_bool


is_python_module_built = str_to_bool(os.environ["BUILD_MEC_MODULE2_PYTHON"])
is_cpp_module_built = str_to_bool(os.environ["BUILD_MEC_MODULE2_CPP"])

if(is_python_module_built):
  from pypp11.common.mec import mec_module2


class MainTest(unittest.TestCase):
  if(is_python_module_built):

    if(is_cpp_module_built):
      def test_sub(self):
        self.assertEqual(mec_module2.cpp.sub(3, 1), 2)


if __name__ == '__main__':
    unittest.main()
