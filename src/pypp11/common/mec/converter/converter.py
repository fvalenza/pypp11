
def str_to_bool(s):
  """Convert the string to boolean

  Parameters
  ----------
  s : string

  Returns
  -------
  Bool

  Raises
  ------
  ValueError
      If the input string is malformed
  """
  if ((s == 'True') or (s == 'TRUE')):
       return True
  elif ((s == 'False') or (s == 'FALSE')):
       return False
  else:
       raise ValueError("Cannot convert env var" + str(s) + "to boolean ( not True or False )")


__all__ = ["str_to_bool"]
