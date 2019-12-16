""" This module makes available different functions to treat the data chunk by chunk

"""
import numpy as np


def get_chunk_limits(chk, chunk_size, chunk_size_gmd, M, H):
  """Compute the indexes in netcdf dimensions of the start/end of chunk number chk

  Parameters
  ----------
  chk : float
      Number of chk to be processed
  chunk_size : int
      The size of the chunk in macro cycles

  Returns
  -------
  tuple : start_chunk, end_chunk, current_chunk_size, start_chunk_gmd, end_chunk_gmd, current_chunk_size_gmd
      start_chunk: index of the macro cycle corresponding to beginning of chunk
      end_chunk: index of the macro cycle corresponding to end of chunk
      current_chunk_size: size of chunk ( = end - start)
      start_chunk_gmd: index of the cycle corresponding to beginning of chunk
      end_chunk_gmd: index of the cycle corresponding to end of chunk
      current_chunk_size_gmd: size of chunk ( = end - start)
  """
  start_chunk            = np.int(chk * chunk_size)
  end_chunk              = np.int(min(M, (chk + 1) * chunk_size))
  current_chunk_size     = end_chunk - start_chunk
  start_chunk_gmd        = np.int(chk * chunk_size_gmd)
  end_chunk_gmd          = np.int(min(M * H, (chk + 1) * chunk_size_gmd))
  current_chunk_size_gmd = end_chunk_gmd - start_chunk_gmd

  return start_chunk, end_chunk, current_chunk_size, start_chunk_gmd, end_chunk_gmd, current_chunk_size_gmd


__all__ = ["get_chunk_limits"]
