import unittest
import subprocess
import os

from pypp11.common.mec.converter.converter import str_to_bool


is_cpp_module1_built = str_to_bool(os.environ["BUILD_MEC_MODULE1_CPP"])
is_cpp_module2_built = str_to_bool(os.environ["BUILD_MEC_MODULE2_CPP"])
run_pure_cpp_tests = str_to_bool(os.environ["PYPP11_PYTEST_RUN_CPP_TESTS"])


def CPP_TEST_MODULE(mod):
  subprocess.check_call(os.path.join(os.path.dirname(
      os.path.relpath(__file__)), 'bin', mod))


if(run_pure_cpp_tests):
  class MainTest(unittest.TestCase):
      def test_cpp(self):
          if(is_cpp_module1_built):
            CPP_TEST_MODULE('mec-module1_test')
          if(is_cpp_module2_built):
            CPP_TEST_MODULE('mec-module2_test')


if __name__ == '__main__':
    unittest.main()
