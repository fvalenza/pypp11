import os
import shutil
import errno


def force_copy(src, dst):
    """Copy the input file

    Parameters
    ----------
    src : string
        The path to the source file
    dst : string
        The path to the destination file
    """
    try:
      shutil.copy2(src, dst)
    except shutil.Error:
      os.remove(dst)
      shutil.copy2(src, dst)


def force_symlink(src, dst):
  """Create a symbolic link of the input file

  Parameters
  ----------
  src : string
      The path to the source file
  dst : string
      The path to the destination file
  """
  try:
    os.symlink(src, dst)
  except OSError as e:
    if e.errno == errno.EEXIST:
      os.remove(dst)
      os.symlink(src, dst)


__all__ = ["force_copy", "force_symlink"]
