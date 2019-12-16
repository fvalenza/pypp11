import numpy as np
import sys


def simple_algo(dimensions, parameters, pre_core_results, input_struct):
  """Callback function for ulos_estimate algo
  Process the block/chunk of data given as input

  Parameters
  ----------
  dimensions : dict
      Dictionnary containing all the dimensions of the data/products needed by the function
  parameters : dict
      Dictionnary containing all the parameters of the data/products needed by the function
  pre_core_results : dict
      Additional info needed by the function
  input_struct : dict
      Dictionnary containing the input data

  Returns
  -------
  dict
      The results of the computation
  """
  # Dimensions
  #
  dim_1     = dimensions["name_dim_1"]

  # Parameters
  #
  param_1 = parameters["name_param_1"]

  # Get Chunk input
  #
  input_1 = input_struct["name_input_1"]

  # Prepare Chunk output
  #
  output_struct = {}
  output_struct["name_output_1"]    = np.full((param_1, dim_1), fill_value=sys.float_info.max, dtype="f8")

  #
  # Process elements by chunks = subset of the input struct
  #
  for p in range(0, param_1):
    for d in range(0, dim_1):
      calc_result = p * d * input_1[p, d]
      output_struct["name_output_1"][p, d] = calc_result

  return output_struct
