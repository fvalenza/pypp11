""" This module makes available sorting capability for all type of structures / struff
"""
import re
import os


def natural_sorting_digits(input_list):
  """Natural sorting of input files containing number.
  This function currently expect strings to be in the format *digits*

  Parameters
  ----------
  input_list : list of string
      List of files that must be naturally sorted

  Returns
  -------
  list of string
      The list sorted in a natural way
  """
  return sorted(input_list, key=lambda x: float(re.findall("(\d+)", os.path.basename(x))[0]))


__all__ = ["natural_sorting_digits"]
