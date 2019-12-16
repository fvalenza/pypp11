import os

#
# Module holding multiple functions
#
from . import pypp11_logger
from . import chunk_process
from . import file_copy
from . import sorting
from . import converter
from . import math
from . import tictoc
from . import clp


#
# C++/Python Modules
#
from .converter.converter import str_to_bool

if (str_to_bool(os.environ['BUILD_MEC_MODULE1_PYTHON'])):
  from .mec_module1 import mec_module1
if (str_to_bool(os.environ['BUILD_MEC_MODULE2_PYTHON'])):
  from .mec_module2 import mec_module2
if (str_to_bool(os.environ['BUILD_MEC_MODULE3_PYTHON'])):
  from .mec_module3 import mec_module3
