""" This module makes available some mathematical statements / functions
"""
import numpy as np


def hermitian_product(a, b):
  """ Perform the hermitian product of two arrays

  Foreach i :  (a[i] * conjugate(b[i]))

  Parameters
  ----------
  a : array-like
      array
  b : array-like
      array

  Returns
  -------
  array-like
      The hermitian product of the two input's array
  """
  return np.vdot(b, a)


__all__ = ["hermitian_product"]
