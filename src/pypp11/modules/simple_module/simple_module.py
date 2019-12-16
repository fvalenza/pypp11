import os

from netCDF4 import Dataset

from pypp11.modules.module_base import ModuleBase
from .step import simple_module_step as s

from pypp11.common.mec.pypp11_logger import pypp11_logger as plog


class SimpleModule(ModuleBase):
  """Simple Module  executed by sample binary

  Can execute the following algorithms:
    - Coherent average power
    - Incoherent average power
    - range doppler proc nadir
    - range doppler proc off nadir
  """
  def __init__(self, input_dirs, output_dir, global_conf_data, local_conf_data):
    self.name = self.__class__.__name__
    super().__init__(input_dirs, output_dir, global_conf_data, local_conf_data)

  def get_input_files(self):
    input_files_dic = {}
    # input_files_dic["name_input_1_file"]      = os.path.join(self.output_dir, self.get_global_data("Configuration.name_input_1_file").getStringValue())

    return input_files_dic

  def get_dimensions(self):

    dimensions = {}

    try:
      with Dataset(self.input_files["name_input_1_file"], "r") as nc_input_1:
        dimensions["name_dim_1"]    = nc_input_1.dimensions["name_dim_1"].size
    except IOError as e:
      plog.error(str(self.name) + " -- Could not open input file: " + str(e.filename), self.log_error)
      raise

    return dimensions

  def pre_module_steps(self):
    pass

  def files_merging(self):
    """Merge the result of the algorithms executed by the module into product_simple_module netCDF file
    """
    pl_obp_intermediate_files = []

    for keys in self.algo_product_files:
      pl_obp_intermediate_files.append(self.algo_product_files[keys])

    nc_time_holder = self.input_files["nc_in_pl_rac_path"]
    pl_obp_path    = os.path.join(self.output_dir, self.get_global_data("Configuration.obm_obp_filename").getStringValue())

    # Add global attribute to the netcdf: number of pulses in rac + number of nadir horns
    attributes = {}
    attributes['pulses'] = self.dimensions["pulses"]
    attributes['nadir']  = self.dimensions["nadir_horns"]

    self.file_merging_time_holder(pl_obp_intermediate_files, nc_time_holder, pl_obp_path, True, attributes=attributes)

  def post_module_steps(self):
    self.files_merging()

  def run_steps(self):
    self.algo_product_files = {}

    # Coherent average pulse pair
    s.simple_module_step_simple_algo(self)
