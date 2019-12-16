#!/usr/bin/env python

import os
import sys
import matplotlib.pyplot as plt

from scipy import *
from pylab import *
from matplotlib.pyplot import *
from matplotlib.figure import *
from matplotlib import rc

rc('font', **{'family':'serif','serif':['Times New Roman'], 'size':18})
rc('axes', **{'labelsize' : 12})
rc('legend', **{'fontsize' : 12})
rc('image', **{'cmap' : 'jet'})

from plotters.plotter_1 import Plotter1

# =======================================================================
# USER CONFIGURATION
# =======================================================================
import config
verbosity          = False
bool_display_plots = True
bool_save_plot     = True
save_dir           = "/home/fvalenza/Bureau/perfo_plots/perfo_plots_v4"


# ======================================================================
# Folder preparation
# ======================================================================
if(bool_save_plot and (save_dir is not None)):
  if not os.path.exists(save_dir):
    try:
      os.makedirs(save_dir)
    except OSError as exc:
      if exc.errno != errno.EEXIST:
        raise

# =======================================================================
# LOAD MODELS
# =======================================================================


# ======================================================================
# Local Functions
# ======================================================================
from tools import std_computation

# ======================================================================
# core
# ======================================================================


#
# Sea Moving, No current
#
phi_data_moving_nocurrent = {}
std_data_moving_nocurrent = {}

std_computation(config.simu_dir, "path/to/simu", config.directions[0], config.wind[0],  phi_data_moving_nocurrent, std_data_moving_nocurrent)
std_computation(config.simu_dir, "path/to/simu", config.directions[1], config.wind[0],  phi_data_moving_nocurrent, std_data_moving_nocurrent)
std_computation(config.simu_dir, "path/to/simu", config.directions[0], config.wind[1],  phi_data_moving_nocurrent, std_data_moving_nocurrent)
std_computation(config.simu_dir, "path/to/simu", config.directions[1], config.wind[1],  phi_data_moving_nocurrent, std_data_moving_nocurrent)
std_computation(config.simu_dir, "path/to/simu", config.directions[0], config.wind[2],  phi_data_moving_nocurrent, std_data_moving_nocurrent)
std_computation(config.simu_dir, "path/to/simu", config.directions[1], config.wind[2],  phi_data_moving_nocurrent, std_data_moving_nocurrent)


# ======================================================================
# PLOTTING
# ======================================================================

Plotter1(verbosity,
         bool_save_plot,
         save_dir, config,
         [phi_data_moving_nocurrent, std_data_moving_nocurrent]).run()



if bool_display_plots:
  plt.show()
