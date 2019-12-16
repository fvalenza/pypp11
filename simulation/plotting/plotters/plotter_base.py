import os
import numpy as np


# ======================================================================
# Class definition
# ======================================================================
class PlotterBase(object):
  def __init__(self, verbosity, save_plot, save_dir):
    self.verbosity    = verbosity
    self.save_plot    = save_plot and (save_dir is not None)
    self.save_dir     = save_dir

  def save_plot_func(self, plt, filename, doSave):
    if doSave is True:
        plt.savefig(filename)

  def run(self):
    pass
