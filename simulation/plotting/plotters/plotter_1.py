import os
import numpy as np
import matplotlib.pyplot as plt
from plotter_base import PlotterBase


color_ = {
  "3": "darkorange",
  "7": "seagreen",
  "14": "slateblue",
  "ref": "darkviolet"
}

marker_ = {
  "3": "o",
  "7": "*",
  "14": "+",
  "ref": "+"
}

markersize_ = {
  "3": 7,
  "7": 10,
  "14": 10,
  "ref": 7
}

markeredgewidth_ = {
  "3": 1,
  "7": 1,
  "14": 1,
  "ref": 2
}

markerfacecolor_ = {
  "3": "none",
  "7": "none",
  "14": "none",
  "ref": color_["ref"]
}


# ======================================================================
# Class definition
# ======================================================================
class Plotter1(PlotterBase):
  def __init__(self, verbosity, save_plot, save_dir, config, data_moving_nocurrent):
    # super().__init__(verbosity, save_plot, save_dir)  # Python3
    super(Plotter1, self).__init__(verbosity, save_plot, save_dir)  # Python2
    self.config = config
    self.data_moving_nocurrent = data_moving_nocurrent

    self.key_tuples = []
    # self.key_tuples.append((self.config.incidence[j], wind, self.config.directions[i]))
    self.availability = self.check_data_availability(data_moving_nocurrent)

  def check_data_availability(self, data_moving_nocurrent):
    avail = True
    # for key in self.key_tuples:
    #   if key not in data_moving_nocurrent[0]:
    #     avail = False

    return avail

  def run(self):

    if (self.availability):
      # ======================================================================
      # PRINTING
      # ======================================================================
      if (self.verbosity):
        print "Hello there"
        pass

      # ======================================================================
      # PLOTTING
      # ======================================================================

      #
      # Fig 1. moving sea, no current, no swell, 3vs7vs14
      #
      phi_data_moving_nocurrent = self.data_moving_nocurrent[0]
      std_data_moving_nocurrent = self.data_moving_nocurrent[1]

      fig, ax = plt.subplots(2, 2, figsize=(14, 14), sharey='row')
      plt.subplots_adjust(left=0.1, right=0.97, wspace=0.05, bottom=0.25)

      for i in range(np.size(self.config.directions)):
        dirctn = self.config.directions[i]

        for j in range(np.size(self.config.incidence)):
          inc = self.config.incidence[j]

          for wind in self.config.wind:
              (ax[i, j].plot(-phi_data_moving_nocurrent[(inc, wind, dirctn)] + phi_data_moving_nocurrent[(inc, wind, dirctn)][0], std_data_moving_nocurrent[(inc, wind, dirctn)] * 1.e2,
                             marker=marker_[wind],
                             linestyle='None',
                             fillstyle='none',
                             markersize=markersize_[wind],
                             markeredgewidth=markeredgewidth_[wind],
                             markerfacecolor=markerfacecolor_[wind],
                             markeredgecolor=color_[wind],
                             label="Label of what the plot represents"))

          ax[0, j].set_title("Title top of column [dim]", fontsize=18)
          ax[1, j].set_xlabel("xlabel [dim]", fontsize=20)

          # ax[i, j].set_xticks([0, 45, 90, 135, 180, 225, 270, 315, 360])
          # ax[i, j].set_xlim(-1., 181.)

          ax[i, j].grid()
          ax[i, 0].set_ylabel("title at left of column [dim]", fontsize=20)

          # ax[1, j].set_ylim(-1., 50)

      ax[0, 0].legend(fontsize=18, loc="upper center", bbox_to_anchor=(1., -1.4), ncol=2).draggable()

      plt.suptitle("title at top of window", fontsize=18)

      self.save_plot_func(plt, os.path.join(self.save_dir, "title_fig_saved.png"), self.save_plot)

    else:
      pass
