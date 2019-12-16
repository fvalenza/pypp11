import sys
import os
import glob
import numpy as np

import xarray as xr
from netCDF4 import Dataset

from pypp11.modules.module_base.algo_base import AlgoBase
from pypp11.common.mec.pypp11_logger import pypp11_logger as plog
from pypp11.common.mec.sorting import sorting as psort


class SimpleAlgo (AlgoBase):
  """Algorithm simple algo executed by module simple module
  """

  def __init__(self, proc, core_algo):
    self.name = self.__class__.__name__
    super().__init__(proc, core_algo)

  def get_dimensions(self, proc):
    dimensions = {}
    dimensions["name_dim_1"]    = 1
    dimensions["name_dim_2"]    = proc.dimensions["name_dim_2"]

    return dimensions

  def get_parameters(self, proc):
    parameters = {}
    parameters["name_param_1"]      = 1
    parameters["name_param_2"]      = proc.get_global_data("Configuration.name_param_2").getIntValue()      # Mandatory in all algo

    return parameters

  def get_input_data(self, proc):
    input_data = {}
    input_data["input_file_1"]      = proc.input_files["input_file_1"]
    return input_data

  def get_input_chunk(self, input_data, chunk_info):
    # start_chunk        = chunk_info[0]
    # end_chunk          = chunk_info[1]
    # current_chunk_size = chunk_info[2]
    # start_chunk_gmd    = chunk_info[3]
    # end_chunk_gmd      = chunk_info[4]

    # Take from input_data (the list of files containing the input products) the actual data that must be processed ( only the chunk necessary)
    input_struct = {}

    return input_struct

  def create_outfile_simple_algo_chk(self, chk_number, chunk_size):
    """Create the outptfile pl_obp_avg_pp.nc for current chunk

    Parameters
    ----------
    chk_number : int
      number of the chunk processed
    chunk_size : list
      size of the chunk in term of number of macro cycle

    Returns
    -------
    netCDF Dataset
        The netCDF Dataset that will holds pl_obp_avg_pp datas for current chunk
    """
    obp_avg_pp_chk_filename = os.path.join(self.output_dir, "product_simple_algo." + str(chk_number) + ".nc")

    try:
      product_file_simple_algo = Dataset(obp_avg_pp_chk_filename, "w")
    except IOError:
      plog.error(str(self.name) + " -- Could not create chunk netcdf output: " + str(obp_avg_pp_chk_filename), self.log_error)
      raise

    product_file_simple_algo.createDimension('name_dim_1', 2)

    return product_file_simple_algo

  def write_output_chunk(self, output_struct, chunk_info):
    chk_size   = chunk_info[2]
    # chk_size   = output_struct["l0_rac_b_re"].shape[0]
    chk_number = chunk_info[6]

    product_file_simple_algo = self.create_outfile_simple_algo_chk(chk_number, chk_size)

    # product_file_simple_algo.variables["product_1"][:] = output_struct["product_1"][:]
    product_file_simple_algo.close()

  def pre_core_algo(self):
    # self.parameters["nc_in_ob_geometry_path"] = self.input_data["nc_in_ob_geometry_path"]
    pass

  def post_core_algo(self):

    # Merge all chunk files into one
    try:
      simple_algo_interm_files_pattern = os.path.join(self.output_dir, "product_simple_algo*.nc")
      simple_algo_interm_files_list    = glob.glob(simple_algo_interm_files_pattern)

      simple_algo_interm_files_list_sorted = psort.natural_sorting_digits(simple_algo_interm_files_list)

      with xr.open_mfdataset(simple_algo_interm_files_list_sorted, concat_dim="m") as DS:
        DS.to_netcdf(os.path.join(self.output_dir, "product_simple_algo.nc"), mode="w")

      # Remove interm. results
      for file in simple_algo_interm_files_list_sorted:
        try:
          os.remove(file)
        except OSError as e:
          plog.warning("Could not remove all intermediate files of product_simple_algo. Delete them manually before reruning a simulation")

    except Exception as e:
      raise e

    return os.path.join(self.output_dir, "product_simple_algo.nc")
