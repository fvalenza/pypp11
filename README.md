PYPP11: Python library with C++ code wrapped with use of pybind 11
===========
<!-- coverage master:
[![coverage master](/path/to/pypp11/commits/master/coverage.svg)](/path/to/pypp11/commits/master) -->


### Get this repo

This repository makes use of git submodules. Do not forget to clone it recursively :

```
git clone --recursive https://github.com/fvalenza/pypp11
```

---

### Install this python package

#### Sourcing `env.bashrc`

To install/compile and use this package, some environment variables must be specified. This is done through the `env.bashrc` file. Before running any command, it is mandatory to source this file first

```Bash
cd pypp11/ # Go to root of directory
source env.bashrc
```

A few commands will be presented in the next sections. The `env.bashrc` file also creates aliases to these command


#### Compile dummylib and source env.bashrc before any python related stuff

This python packages uses a C++ library `dummy_library` shipped with it. One needs first to compile and install it

```Bash
cd external_libraries/dummylib
mkdir build && cd build
cmake ..
make install
```

#### Install pypp11

This Python package uses [setuptools](https://setuptools.readthedocs.io/en/latest/) for packaging. One can install it in several ways:

Warning: When running multiple times install or tests commands, you may come with an error stating that there is a conflict with CMakeCache.txt files. It generally comes because the build/ directory is out of date. If so, you need to `rm -r build/` directory

##### i/ Local install of python package

 In case you do not have sudo rights on your machine, you can install this package locally to make it available in PYTHONPATH only for the current user

```Bash
# equivalent to  pypp_linstall
cd $PYPP11_HOME
python -m pip install --user .
```

##### ii/ Install of python package

 In the same way, you can install the package for all the users :t

```Bash
# equivalent to  pypp_install
cd $PYPP11_HOME
python -m pip install .
```
##### iii/ Development

 If you want to install the package but being able to edit it without reinstalling it, use development mode.

```Bash
# equivalent to  pypp_develop
cd $PYPP11_HOME
python -m pip install -e . --user
```

##### Uninstall pypp11

```Bash
# equivalent to  pypp_uninstall
python -m pip uninstall pypp11
```

#### Running unittest

Unittests can be found in the tests/ folder. Due to the  binding of C++ functions, they are divided in two categories, the C++ tests  and the Python ones.
The Python framework centralizes both of them in test suites. Each Python file is a test suite whereas the C++ tests are considered as one test suite (in which you can run one or many C++ test binaries)

One can decides to execute the C++ tests or not through Python by changing in env.bashrc the variable `PYPP11_PYTEST_RUN_CPP_TESTS` to `True` or `False`.

To run all the tests:

```Bash
# equivalent to  pypp_test
cd $PYPP11_HOME
python3 setup.py test
```

The different Python test suites can also be executed separately. To do so, do the following, where the path to the Test suite must be specified folder-wise (package hierachy):

```Bash
cd $PYPP11_HOME
python3 -m tests.python.packageA.subpackB.modB1.modB1_test
```

---

### Running in virtual environments

It is particularly advised to use [virtualenv](https://virtualenv.pypa.io/en/latest/) to avoid having to deal with permissions or packages versions & dependencies.

We put our virtualenvs in  `~/virtualenvs`. In this folder we can create a virtualenv which will be used for installing and running pypp11

```Bash
## Equivalent to pypp_venv
# Create virtual environment
mkdir ~/virtualenvs
virtualenv ~/virtualenvs/pypp11
# Run the virtual environment, isolated from the hosting computer
source ~/virtualenvs/pypp11/bin/activate # equivalent to pypp_activate

# Do what you want with pypp11, here we just run a python interpreter and ensure we can import the software
ipyton
import pypp11

# Exit the virtual environment
deactivate
```

---

### Create source package

Two methods are interesting to create a distribution package:

#### 1 - Create source distribution as an archive
The archive will be created in $PYPP11_HOME/dist/ folder

```Bash
#Equivalent to pypp_sdit
cd $PYPP11_HOME
python setup.py sdit
```

#### 2 - Create release package with no source
In case you don't want to make the sources available (only compiled files), you can generate an egg file with no sources attached.

```Bash
# Equivalent to pypp_bdist_nosrc
cd $PYPP11_HOME
python setup.py egg-info -Db "" sdist bdist-egg -- exclude-source-files
```

To use the generated egg file, it must be available in the PYTHONPATH:

```python
import sys
egg_path = 'path/to/file/.egg'
sys.path.append(egg_path)
import pypp11
```

---


### How and where add a new feature

To add a new feature to pypp11, one must understand how it is built:

First, pypp11 is constructed as a big python package with subpackages where functionnalities come either from python functions or from C++ functions.

These functions are gathered either in pure python modules or in mixed python/C++ modules. 

* Pure python modules are straightforward ( see for example `package1/subpack1` ), whereas C++/python modules are a bit tricky.

* The C++ functionalities can be found in C++ files ( e.g `packageA/subpackB/modB1/modB1.cpp` ). These functions are binded to python with pybind11 and compiled in an .so file ( e.g `packageA/subpackB/modB1/expose-modB1.cpp` ). Pybind will then work with this file and expose its Python API through a Python module as a subpackage ( e.g `packageA.subpackB.modB1.expose_modB1` ).
The exposed module is then accessible through the exposing module `packageA.subpackB.modB1.modB1.cpp` (in file`packageA/subpackB/modB1/modB1.py)`

#### 1 - Add a new module/subpackage

##### Add a new pure python module

Just as regular python packages work, you just have to add your .py file in a folder with an `__init__.py` and import the subpackages recursively in the parent `_init.py__` files.


##### Add a new C++/python module

The procedure to add a mixed C++/python module is 3 steps long:

1. Add the C++ module and add it in the compiling chain with CMake
2. Create the Pybind extension (= expose as python package the C++ module previously added)
3. Create the Python/C++ module and add it as a submodule of the full pypp11 package



###### Step 1: Add the C++ module and add it in the compiling chain with CMake
The purpose of this step is to create a C++ file and add it in the compiling process so that an .o file is generated

1. Create your C++ module file and put it in the right place in pypp11 file's architecture. Add the .hpp file in `include/` folder
2. At the level of the new file added, add in CMakeLists all necessary stuff to compile this C++ file. For example:

```CMake
cmake_minimum_required(VERSION 3.0)

PROJECT(modB2)

SET(CPP_MODULE ${PROJECT_NAME})


# ----------------------------------------------------
# --- C++ Sources ------------------------------------
# ----------------------------------------------------
set(SOURCES_CPP_MODULE
    ${CPP_MODULE}.cpp
    )

# ----------------------------------------------------
# --- DEPENDANCIES -----------------------------------
# ----------------------------------------------------
find_library(DUMMY_LIBRARY dummylib HINTS ${LIBS_DIR}/dummylib/lib)


# Create library of module
add_library(${CPP_MODULE}  ${SOURCES_CPP_MODULE} )

# If it needs to link against external_library
target_link_libraries(${CPP_MODULE} PRIVATE ${DUMMY_LIBRARY})
target_include_directories(${CPP_MODULE} PUBLIC ${LIBS_DIR}/dummylib/include/ )
```

3. Do not forget to add the new module in the intermediate CMakeLists with `add_subdirectory`


###### Step 2: Create the Pybind extension (= expose as python package the C++ module previously added)

In this step we will create a C++ file whose role is solely exposing our C++ module as a python module thanks to pybind:

1. Create the C++ file(e.g `expose-mec-module2.cpp`) and fill it to expose C++ functions/classes. For more informations, please refer to [pybind11 documentation](https://pybind11.readthedocs.io/en/stable/)
2. In the root CMakeLists.txt, add the newly C++ file as a pybind module:

```CMake
ADD_PYBIND_MODULE(module_name path/to/module_name "list of libs,to link" "list of include, directories of external libs")
```

3. In the file setup.py, add the new exposed module in the corresponding list (`pybind_simple_modules` for modules with no dependencies, or `pybind_linked_modules`). setuptools will then look in this list and build all these python modules.

###### Step 3: Create the Python/C++ module and add it as a submodule of the full pypp11 package

Expose the newly pybind python module through the Python module in pypp11

1. At the level of your C++ module, create a `module_name.py` file with the corresponding `__init.py__` and add the following line:
```python
import expose_module_name as cpp
```
2. You can add purely python functions too if you want in this file


**Warning: file naming convention**

The naming convention for files  must be followed or automatic packaging ( like CMake and setuptools ) won't work.

* For C++ module:
  - The C++ source file shall be `nameMod.Cpp`
  - The Pybind module exposing file shall be named `expose-nameMod.cpp` and shall expose the module with the name `expose_nameMod` (note the underscore for the module name whereas the file as hyphen in its name)
* For python:
  - The python source file shall be `nameMod.py`


#### 2 - Add a new test

##### Add cpp test suite to test cpp modules

In tests/cpp folder, one can add test suites to test C++ modules. To one module (e.g `modName.cpp` correspond one test suite `test_modName.cpp`). Once you add a new module test suite, you need to update the CMakeLists.txt to add the unit test to the list of binaries to be created. This is done with a macro - with the second argument being the list of packages the executable must link against:

```CMake
ADD_UNIT_TEST(modB2 "modB2;dummylib" )
```
The C++ test suites are using [catch](https://github.com/catchorg/Catch2) framework

##### Add python test suite to test python module/subpackage (and the binding of the cpp modules)

To add python tests, just follow any package convention and directly add the file `modName_test.py` at the good place in the hierarchy. We advise to follow the src/ folder hierarchy

##### Execute C++ test suites in Python tests

With the command `pypp_test` one can run all the test suites at one. Python will also run C++ tests (by executing c++ binaries) selected in test_main.py





