import numpy as np


def std_computation(simu_dir, pattern, direction, wind, phi_data, std_data):

  random_array      = np.random.rand(10)

  phi_data[('12', wind, direction)] = random_array
  std_data[('12', wind, direction)] = random_array
  phi_data[('6', wind, direction)] = random_array
  std_data[('6', wind, direction)] = random_array
