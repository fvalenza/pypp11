#include <pybind11/pybind11.h>
//#include "tools/mec/mec_module1/mec-module1.hpp"
#include "mec-module2.hpp"
#include "dummy-module.hpp"


namespace py = pybind11;

PYBIND11_MODULE(expose_mec_module2, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: cmake_example

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc";

    m.def("sub", &sub, R"pbdoc(
        Add two numbers

        Some other explanation about the add function.
    )pbdoc");
    
    m.def("dummy_lib_disp", &dummy_lib_disp, R"pbdoc(
        link to dummy
    )pbdoc");
    
    py::class_<TOTO>(m, "TOTO")
        .def(py::init<>())
        .def("disp", &TOTO::disp);


#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
