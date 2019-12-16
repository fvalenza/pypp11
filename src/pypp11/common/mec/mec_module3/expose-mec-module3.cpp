#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <pybind11/eigen.h>

#include "mec-module3.hpp"


namespace py = pybind11;


// wrap C++ function multiply with NumPy array IO
py::array_t<int> py_multiply(py::array_t<double, py::array::c_style | py::array::forcecast> array)
{
  // allocate std::vector (to pass to the C++ function)
  std::vector<double> array_vec(array.size());

  // copy py::array -> std::vector
  std::memcpy(array_vec.data(),array.data(),array.size()*sizeof(double));

  // call pure C++ function
  std::vector<int> result_vec = multiply(array_vec);

  // allocate py::array (to pass the result of the C++ function to Python)
  auto result        = py::array_t<int>(array.size());
  auto result_buffer = result.request();
  int *result_ptr    = (int *) result_buffer.ptr;

  // copy std::vector -> py::array
  std::memcpy(result_ptr,result_vec.data(),result_vec.size()*sizeof(int));

  return result;
}

// wrap C++ function  length with NumPy array IO
py::array py_length(py::array_t<double, py::array::c_style | py::array::forcecast> array)
{
  // check input dimensions
  if ( array.ndim()     != 2 )
    throw std::runtime_error("Input should be 2-D NumPy array");
  if ( array.shape()[1] != 2 )
    throw std::runtime_error("Input should have size [N,2]");

  // allocate std::vector (to pass to the C++ function)
  std::vector<double> pos(array.size());

  // copy py::array -> std::vector
  std::memcpy(pos.data(),array.data(),array.size()*sizeof(double));

  // call pure C++ function
  std::vector<double> result = length(pos);

  py::ssize_t              ndim    = 2;
  std::vector<py::ssize_t> shape   = { array.shape()[0] , 3 };
  std::vector<py::ssize_t> strides = { sizeof(double)*3 , sizeof(double) };

  // return 2-D NumPy array
  return py::array(py::buffer_info(
    result.data(),                           /* data as contiguous array  */
    sizeof(double),                          /* size of one scalar        */
    py::format_descriptor<double>::format(), /* data type                 */
    ndim,                                    /* number of dimensions      */
    shape,                                   /* shape of the matrix       */
    strides                                  /* strides for each axis     */
  ));
}

PYBIND11_MODULE(expose_mec_module3, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: cmake_example

        .. autosummary::
           :toctree: _generate

           add
           substract
    )pbdoc";

    m.def("add", &add, R"pbdoc(
        Add two numbers

        Some other explanation about the add function.
    )pbdoc");

    m.def("substract", [](int i, int j) { return i - j; }, R"pbdoc(
        Subtract two numbers

        Some other explanation about the subtract function.
    )pbdoc");

    m.def("modify", &modify, "Multiply all entries of a list by 2.0");

    m.def("multiply", &py_multiply, "Convert all entries of an 1-D NumPy-array to int and multiply by 10");

    m.def("length", &py_length, "Calculate the length of an array of vectors (2D numpy array converted to cpp array of vector and length computed");

    m.def("inv", &inv);

    m.def("det", &det);

    py::class_<CustomVectorXd>(m, "CustomVectorXd")
    .def(py::init<Eigen::VectorXd>())
    .def("mul", &CustomVectorXd::mul,pybind11::arg("factor")=1.)
    .def("__repr__",
      [](const CustomVectorXd &a) {
        return "<example.CustomVectorXd>";
      }
    );

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}

