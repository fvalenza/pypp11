import unittest

from pypp11.common.mec.sorting import sorting as psort


class MainTest(unittest.TestCase):
  def test_ssort_natural_digits(self):
    input_list = ["input.1.nc", "input.11.nc", "input.100.nc", "input.2.nc", "input.22.nc", "input.3.nc"]
    expected_output_list = ["input.1.nc", "input.2.nc", "input.3.nc", "input.11.nc", "input.22.nc", "input.100.nc"]

    output_list = psort.natural_sorting_digits(input_list)

    self.assertEqual(output_list, expected_output_list)


if __name__ == '__main__':
    unittest.main()
