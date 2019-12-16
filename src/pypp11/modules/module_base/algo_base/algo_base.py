import abc
from copy import deepcopy

import dask
from distributed import Client, wait

from pypp11.common.mec.chunk_process import chunk_process as chunkp


class AlgoBase(object):

  """Base Class for Algorithms in processing chain.
  The input data are treated chunk by chunk, and then the results are merged into one single file. This allows multicore
  processing through use of dask and distributed
  """

  __metaclass__ = abc.ABCMeta

  def __init__(self, mod, core_algo):
    self.dimensions       = self.get_dimensions(mod)
    self.parameters       = self.get_parameters(mod)
    self.input_data       = self.get_input_data(mod)
    self.output_dir       = mod.output_dir
    self.pre_core_results = {}
    self.core_algo        = core_algo

  ######################################
  #          ABSTRACT METHODS          #
  #   must be overriden by subclass    #
  ######################################
  @abc.abstractmethod
  def get_dimensions(self):
    """Retrieve all the dimensions needed to process the data and perform computations

    Returns
    -------
    dict(int)
        The dictionnary associating all the dimensions with their concrete value
    """
    raise NotImplementedError('users must define get_dimensions to use this base class')

  @abc.abstractmethod
  def get_parameters(self):
    """Retrieve all the parameters needed to process the data and perform computations

    Returns
    -------
    dict(int)
        The dictionnary associating all the parameters with their concrete value
    """
    raise NotImplementedError('users must define get_parameters to use this base class')

  @abc.abstractmethod
  def get_input_data(self):
    """"Get the input files path needed for the execution of the algorithm's computations

    Returns
    -------
    dict(strings)
        dictionnary containing the absolute path to the input files of the algorithm
    """
    raise NotImplementedError('users must define get_input_data to use this base class')

  @abc.abstractmethod
  def get_input_chunk(self, input_data, chunk_info):
    """Read from the inputfiles the data corresponding to the chunk to be processed

    Parameters
    ----------
    input_data : dict
      Dictionary of filepaths to the input files of the algorithm
    chunk_info : list
        Informations about the chunk to be processed
        [start_chunk, end_chunk, current_chunk_size, start_chunk_gmd, end_chunk_gmd, current_chunk_size_gmd]

    Returns
    -------
    input_struct : dict
        dictionnary containing the input data for the chunk
    """
    raise NotImplementedError('users must define get_input_chunk to use this base class')

  @abc.abstractmethod
  def write_output_chunk(self, output_struct, chunk_info):
    """Write the results of the callback function (processing of the input chunk data) to netCDF file

    Parameters
    ----------
    output_struct : dict
        dictionnary containing the output data of the algorithm for the chunk
    chunk_info :  list
        Informations about the chunk that have been processed
        [start_chunk, end_chunk, current_chunk_size, start_chunk_gmd, end_chunk_gmd, current_chunk_size_gmd]
    """
    raise NotImplementedError('users must define write_output_chunk to use this base class')

  @abc.abstractmethod
  def pre_core_algo(self):
    """Perform all the operations needed before executing the callback function.
    Generally computes stuff used for all chunks
    """
    raise NotImplementedError('users must define pre_core_algo to use this base class')

  @abc.abstractmethod
  def post_core_algo(self):
    """Perform all the operations once all the chunks have been processed
    """
    raise NotImplementedError('users must define post_core_algo to use this base class')

  ######################################
  #      END OF ABSTRACT METHODS       #
  ######################################

  def get_current_chunk_state_info(self, chk, chunk_size, chunk_size_gmd, M, H):
    return [chunkp.get_chunk_limits(chk, chunk_size, chunk_size_gmd, M, H)]

  def state_algo(self, current_chunk_info, input_data, dimensions, parameters, pre_core_results):
    """Save the state of the algorithm before processing a chunk.
    This is due to avoid multicore problems such as reading/writing the same shared variable in different cores

    Parameters
    ----------
    current_chunk_info : list
        Informations about the chunk that have been processed
        [start_chunk, end_chunk, current_chunk_size, start_chunk_gmd, end_chunk_gmd, current_chunk_size_gmd]
    input_data : dict
      Dictionary of filepaths to the input files of the algorithm
    dimensions : dict
      Dictionnary containing all the dimensions of the data/products needed by the algorithm
    parameters : dict
      Dictionnary containing all the parameters of the simulation needed by the algorithm
    pre_core_results : dict
      Dictionary holding results of computations needed for processing the input data. Computed once before going multi core

    Returns
    -------
    tuple
        deepcopy of the inputs of the method
    """
    state_current_chunk_info = deepcopy(current_chunk_info)
    state_input_data         = deepcopy(input_data)
    state_dimensions         = deepcopy(dimensions)
    state_parameters         = deepcopy(parameters)
    state_pre_core_results   = deepcopy(pre_core_results)

    return state_current_chunk_info, state_input_data, state_dimensions, state_parameters, state_pre_core_results

  def run_sequential(self):
    """ Process all the chunks sequentially
    This solution is better if you have low RAM on your machine. Takes more time for execution of long simulations
    """

    # Ensure chunk size is beyond limits
    M          = self.dimensions["macro_cycles"]
    H_tot      = self.dimensions["all_horns"]
    chunk_size = self.parameters["chunk_size"]

    if (chunk_size == 0 or chunk_size > M):
      chunk_size = M

    chunk_size_gmd = chunk_size * H_tot
    self.parameters["chunk_size_gmd"] = chunk_size_gmd

    # foreach chunk
    chk = 0

    while True:
      # Compute start/end index of chunk in products
      current_chunk_info                    = self.get_current_chunk_state_info(chk, chunk_size, chunk_size_gmd, M, H_tot)
      end_chunk                             = current_chunk_info[1]
      self.parameters["current_chunk_info"] = current_chunk_info
      print("chunk number / info: {} {}".format(chk, current_chunk_info))

      self.dask_fun(current_chunk_info)

      # Go to next chunk or stop if we processed last chunk
      chk += 1
      if not (end_chunk != M):
        break
    # End of foreach chunk

  def dask_fun(self, current_chunk_info):
    """Callback function for multicore processing.
    This function is added to the dask scheduler as a process for each chunk to be processed

    Parameters
    ----------
    current_chunk_info : list
        Informations about the chunk that have been processed
        [start_chunk, end_chunk, current_chunk_size, start_chunk_gmd, end_chunk_gmd, current_chunk_size_gmd]
    """
    # Get chunk of input products
    input_struct = self.get_input_chunk(self.input_data, current_chunk_info)

    # Start of processing chunk
    output_struct = self.core_algo(self.dimensions, self.parameters, self.pre_core_results, input_struct)

    # TODO - From this point, input_struct is no more needed, could be free'ed ?
    # del input_struct["l0_raw_b_re"]
    # del input_struct["l0_raw_b_im"]

    # Write chunk results in output product
    self.write_output_chunk(output_struct, current_chunk_info)

  def run_distributed(self):
    """ Process all the chunks using dask client to create the scheduling
    This solution is better than run_delayed in case for each chunk we define only one subtask.
    """

    client = Client()

    # Ensure chunk size is beyond limits
    #
    M          = self.dimensions["macro_cycles"]
    H          = self.dimensions["off_nadir_horns"]
    H_tot      = self.dimensions["all_horns"]
    chunk_size = self.parameters["chunk_size"]

    if (chunk_size == 0 or chunk_size > M):
      chunk_size = M

    chunk_size_gmd = chunk_size * H_tot
    self.parameters["chunk_size_gmd"] = chunk_size_gmd

    # foreach chunk - create a task
    chk = 0

    jobs = []

    while True:
      # Compute start/end index of chunk in products
      current_chunk_info                    = self.get_current_chunk_state_info(chk, chunk_size, chunk_size_gmd, M, H)
      end_chunk                             = current_chunk_info[1]
      self.parameters["current_chunk_info"] = current_chunk_info
      print("chunk number / info: {} {}".format(chk, current_chunk_info))

      # Submit to the task tree the task for the current chunk
      futures = client.submit(self.dask_fun, current_chunk_info)
      jobs.append(futures)

      # Go to next chunk or stop if we processed last chunk
      chk += 1
      if not (end_chunk != M):
        break
    # End of foreach chunk

    # Once the task tree is complete, start the computations. TODO - What is the diff between wait and compute ?
    wait(jobs)
    # dask.compute(jobs, scheduler='distributed')

  def run_delayed(self):
    """ Process all the chunks using dask.delayed function to create the scheduling
    This solution is better than run_distributed in case the subtasks can be executed in parallel. This is not the case at the moment
    """

    import dask.multiprocessing
    # from distributed import Client, progress

    # TODO Should we create a Client ?
    # client = Client()

    # Ensure chunk size is beyond limits
    #
    M          = self.dimensions["macro_cycles"]
    H          = self.dimensions["off_nadir_horns"]
    H_tot      = self.dimensions["all_horns"]
    chunk_size = self.parameters["chunk_size"]

    if (chunk_size == 0 or chunk_size > M):
      chunk_size = M

    chunk_size_gmd = chunk_size * H_tot
    self.parameters["chunk_size_gmd"] = chunk_size_gmd

    # foreach chunk - create a task
    #
    chk = 0

    jobs = []
    # http://docs.dask.org/en/latest/delayed-best-practices.html?highlight=compute
    state_algo_fun         = dask.delayed(self.state_algo, nout=5)
    get_input_chunk_fun    = dask.delayed(self.get_input_chunk)
    core_algo_fun          = dask.delayed(self.core_algo)
    write_output_chunk_fun = dask.delayed(self.write_output_chunk)

    while True:
      # Compute start/end index of chunk in products
      current_chunk_info                    = self.get_current_chunk_state_info(chk, chunk_size, chunk_size_gmd, M, H)
      end_chunk                             = current_chunk_info[1]
      self.parameters["current_chunk_info"] = current_chunk_info
      print("chunk number / info: {} {}".format(chk, current_chunk_info))

      state_current_chunk_info, state_input_data, state_dimensions, state_parameters, state_pre_core_results = state_algo_fun(current_chunk_info, self.input_data, self.dimensions, self.parameters, self.pre_core_results)

      # Get chunk of input products
      input_struct = get_input_chunk_fun(state_input_data, state_current_chunk_info)

      # Start of processing chunk
      output_struct = core_algo_fun(state_dimensions, state_parameters, state_pre_core_results, input_struct)

      # Write chunk results in output product
      jobs.append(write_output_chunk_fun(output_struct, state_current_chunk_info))

      # Go to next chunk or stop if we processed last chunk
      #
      chk += 1
      if not (end_chunk != M):
        break
    # End of foreach chunk

    return jobs

  def run(self):
    """ Execution of the algorithm
    Depending on the simulation configuration, it can be run:
    i / Using dask client and distributed (multi core/thread)
    ii/ Using dask delayed (multi core/thread)
    iii/ In sequential mode
    """
    # Run pre_core_algo
    self.pre_core_algo()

    if self.parameters["scheduler_mode"] == 0:
      # Use of client.submit
      # TODO - Compute the num_workers depending of available ram and task_peak_value ( hardcoded because known by developers ? ) ?
      self.run_distributed()
    elif self.parameters["scheduler_mode"] == 1:
      # Use of delayed to split subtask with chaining ( output of subtask 1 is input of subtask 2 )
      # TODO - Compute the num_workers depending of available ram and task_peak_value ( hardcoded because known by developers ? ) ?
      dask.compute(self.run_delayed(), scheduler='processes', num_workers=4)
    else:
      # No parallelism
      self.run_sequential()

    # Run post_core_algo
    return(self.post_core_algo())
