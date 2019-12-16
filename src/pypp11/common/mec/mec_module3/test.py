#!/usr/bin/env python3
import pypp11.common.mec.mec_module3 as mm3
import numpy as np


print(mm3.cpp.add(2, 3))
print(mm3.cpp.substract(2, 3))

#
#
print(mm3.cpp.modify([1, 2, 3, 4]))

#
#
print(mm3.cpp.multiply([0., 1., 2., 3., 4., 5.]))


#
#
A = [0, 1, 2, 3, 4, 5]
B = mm3.cpp.multiply(A)

print('input list = ', A)
print('output     = ', B)


#
#
A = np.arange(10)
B = mm3.cpp.multiply(A)

print('input list = ', A)
print('output     = ', B)


#
#
A = np.arange(10).reshape(5, 2)
B = mm3.cpp.length(A)

print('A = \n', A)
print('B = \n', B)

#
#
A = np.array([[1, 2, 1],
              [2, 1, 0],
              [-1, 1, 2]])

print('A = \n', A)
print('example.det(A) = \n', mm3.cpp.det(A))
print('numpy.linalg.det(A) = \n', np.linalg.det(A))
print('example.inv(A) = \n', mm3.cpp.inv(A))
print('numpy.linalg.inv(A) = \n', np.linalg.inv(A))
