import os
import errno
import abc

import xarray as xr


class ModuleBase(object):
  """Base Class for module of processing chain

  """
  __metaclass__ = abc.ABCMeta

  def __init__(self, input_dirs, output_dir):

    self.input_dirs       = input_dirs
    self.output_dir       = output_dir

    self.input_files = self.get_input_files()
    self.dimensions  = self.get_dimensions()
    self.output_dir  = self.create_output_dir(output_dir)

  ######################################
  #          ABSTRACT METHODS          #
  #   must be overriden by subclass    #
  ######################################
  @abc.abstractmethod
  def get_input_files(self):
    """"Get the input files path needed for the execution of the module's computations

    Returns
    -------
    dict(strings)
        dictionnary containing the absolute path to the input files of the module
    """
    raise NotImplementedError('users must define get_input_files to use this base class method')

  @abc.abstractmethod
  def get_dimensions(self):
    """Retrieve all the dimensions needed to process the data and perform computations

    Returns
    -------
    dict(int)
        The dictionnary associating all the dimensions with their concrete value
    """
    raise NotImplementedError('users must define get_dimensions to use this base class method')

  @abc.abstractmethod
  def pre_module_steps(self):
    """Perform all the operations needed before executing the steps (Algorithms).
    Generally computes stuff used by several steps
    """
    raise NotImplementedError('users must define pre_module_steps to use this base class method')

  @abc.abstractmethod
  def post_module_steps(self):
    """Perform all the operations once all the steps executions are finished
    Generally uses stuff from several steps
    """
    raise NotImplementedError('users must define post_module_steps to use this base class method')

  @abc.abstractmethod
  def run_steps(self):
    """Schedules the different steps of the module, ordonancing the Algorithms
    """
    raise NotImplementedError('users must define run_steps to use this base class method')

  ######################################
  #      END OF ABSTRACT METHODS       #
  ######################################

  def create_output_dir(self, output_dir):
    """Create the output directory

    Parameters
    ----------
    output_dir : string
        absolute path of the directory in which the output files of the module will be created

    Returns
    -------
    output_dir : string
        absolute path of the directory in which the output files of the module will be created

    Raises
    ----------------
    OSError
        If directory creation fails
    """
    if not os.path.exists(output_dir):
      try:
        os.makedirs(output_dir)
      except OSError as exc:
        print(str(self.name) + " -- output dir already existing. bypassed creation of directory : " + str(output_dir))
        if exc.errno != errno.EEXIST:
          print(str(self.name) + " -- Could not create output directory: " + str(output_dir))
          raise

    return output_dir

  def delete_intermediate_files(self, intermediate_files):
    """Delete the list of intermediate files given as argument

    Parameters
    ----------
    intermediate_files : list of string
        The list of files to delete

    Raises
    ------
    OSError
        If the file deletion has failed
    """
    for file in intermediate_files:
      try:
        os.remove(file)
      except OSError as e:
        print("Could not remove all intermediate files of " + self.name  + ". Delete them manually before reruning a simulation")
        raise e

  def file_merging(self, inputs, output, delete_intermediate_files=True):
    """Merge a list of input files (netCDF) into one single output file.
    Optional: delete the input files when done

    Parameters
    ----------
    inputs : list(string)
        List of filepaths. Must be pointing to valid netCDF files
    output : string
        Name of the outputfile to be created during the merge
    delete_intermediate_files : bool, optional
        If the input files must be deleted from hard drive

    Raises
    ------
    Exception
        If the merge is not possible or if some input files are not valid netCDF files
    """
    nc_proc_product_path = output

    try:
      intermediate_files = inputs

      with xr.open_mfdataset(inputs) as nc_proc_product:
        nc_proc_product.to_netcdf(nc_proc_product_path, mode="w", format='NETCDF3_64BIT')

      # Remove interm. results
      if delete_intermediate_files:
        self.delete_intermediate_files(intermediate_files)

    except Exception as e:
      raise e

  def run(self):
    """Runs the module's main computations
    """
    print(str(self.name) + " -- Executing " + str(self.name))

    self.pre_module_steps()

    self.run_steps()

    self.post_module_steps()

    print(str(self.name) + " -- Ending " + str(self.name))
