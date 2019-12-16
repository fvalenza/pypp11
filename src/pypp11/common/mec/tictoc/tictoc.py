from timeit import default_timer as timer

from pypp11.common.mec.pypp11_logger import pypp11_logger as plog


class TicToc():

    """Timer class that can hold multiple instances of tictoc timers (same as matlab tictoc)

    Attributes:
        module (string): Name of the module in which the timer is created
        msg (string): Message to be displayed when toc is called
        timers (list): stack of timers ( FILO )
    """

    class TicTocInstance():

        def __init__(self, feature):
          """Create instance of TicTocInstance class."""
          self.start   = float('nan')
          self.end     = float('nan')
          self.elapsed = float('nan')
          self.feature = feature

        def tic(self):
          self.start = timer()

        def toc(self, msg, restart=False, log_info=True):
          """
          Report time elapsed since last call to tic().

          Optional arguments:
              msg     - String to replace default message of 'Elapsed time is'
              restart - Boolean specifying whether to restart the timer
          """
          self.end     = timer()
          self.elapsed = self.end - self.start
          self.print_message(msg.format(feature=self.feature, toc=str(self.elapsed)), log_info)
          if restart:
              self.start = timer()

        def print_message(self, msg, log_info=True):
          if log_info:
            plog.info(msg)
            pass
          pass

    def __init__(self, module="NaM", msg=None):
        """Create instance of TicToc class."""
        self.timers = []  # Stack of tictocinstances
        self.module = module if module is not None else "NaM"
        self.msg = msg if msg is not None else "{feature} took {toc} seconds"

    def tic(self, feature="NaP"):
        """Start the timer."""
        t = self.TicTocInstance(feature)
        t.tic()
        self.timers.append(t)

    def toc(self, log_info=True, restart=False):
        """
        Report time elapsed since last call to tic().

        Optional arguments:
            msg     - String to replace default message of 'Elapsed time is'
            restart - Boolean specifying whether to restart the timer
        """
        t = self.timers.pop()
        t.toc(self.msg, restart=restart, log_info=log_info)

        if restart is True:
          self.timers.append(t)

    def tocvalue(self, restart=False):
        """
        Return time elapsed since last call to tic().

        Optional argument:
            restart - Boolean specifying whether to restart the timer
        """
        t = self.timers.pop()
        t.toc(restart)
        if restart is True:
          self.timers.append(t)
