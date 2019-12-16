""" This module makes available the different steps executed by the module simple_module
"""
from pypp11.modules.simple_module.algo import SimpleAlgo
from pypp11.common.algo import simple_algo


def simple_module_step_simple_algo(mod):
  #
  # simple_algo
  #
  salg = SimpleAlgo(mod, simple_algo)
  mod.algo_product_files["simple_algo"] = salg.run()
