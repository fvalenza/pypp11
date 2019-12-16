# import `pybind1 extension module from subpackage and expose it
import os


#
# EXPOSE CPP MODULE
#
from pypp11.common.mec.converter.converter import str_to_bool

if (str_to_bool(os.environ['BUILD_MEC_MODULE1_CPP'])):
  import expose_mec_module1 as cpp


#
# PURE PYHTON FUNCTIONS
#
def hello_mec_module1():
    print("Hello world from mec module1 !")
