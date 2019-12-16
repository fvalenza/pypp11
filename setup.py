import os
import re
import sys
import platform
import subprocess

from shutil import copyfile, copymode
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion


_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def str_to_bool(s):
  if ((s == 'True') or (s == 'TRUE')):
       return True
  elif ((s == 'False') or (s == 'FALSE')):
       return False
  else:
       raise ValueError("Cannot convert env var" + str(s) + "to boolean ( not True or False )")


##############################################
# LIST OF C++ MODULES TO CONVERT TO PYTHON   #
##############################################

# Init of the modules' list to empty. Is filled in next section if needed.

# Simple extension modules = modules that do not requires linking
pybind_simple_modules = []

# Linked extension modules = modules that require path to lib, headers etc to compile.
# exemple: {pybind module name, include dir, lib dir, bibs to link, source file}
pybind_linked_modules = []

# name of the executables ( in add_executable in CMkaeList of tests/cpp/ ) to run from python unittest test_cpp.py
cpp_tests_executables = []


########################
#     MODIFY HERE      #
########################


# expose_mec_module1 has no dependency
if (str_to_bool(os.environ['BUILD_MEC_MODULE1_CPP'])):
    pybind_simple_modules.append("expose_mec_module1")
    cpp_tests_executables.append("mec-module1_test")


# expose_mec_module2 links to dummylib
if (str_to_bool(os.environ['BUILD_MEC_MODULE2_CPP'])):
    expose_mec_module2_mod = {
        "name": "expose_mec_module2",
        "includes": [os.path.join(_ROOT_DIR, 'external_libraries', 'dummylib', 'include')],
        "libraries": [os.path.join(_ROOT_DIR, 'external_libraries', 'dummylib', 'lib')],
        "links": ["dummylib"],
        "sources": ["expose-mec-module2.cpp"]
    }

    pybind_linked_modules.append(expose_mec_module2_mod)
    cpp_tests_executables.append("mec-module2_test")

# expose_mec_module3 has no dependency
if (str_to_bool(os.environ['BUILD_MEC_MODULE3_CPP'])):
    pybind_simple_modules.append("expose_mec_module3")
    # cpp_tests_executables.append("mec-module3_test")

########################
# END OF MODIFY HERE   #
########################

pybind_modules = pybind_simple_modules + pybind_linked_modules


class CMakeExtension(Extension):
    def __init__(self, name, include_dirs='', library_dirs='', libraries='', sources='', sourcedir=''):
        Extension.__init__(self, name, sources=[], include_dirs=include_dirs, library_dirs=library_dirs, libraries=libraries)
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)

        for cpp_test in cpp_tests_executables:
            # Copy *_test file to tests directory
            test_bin = os.path.join(self.build_temp, 'tests/cpp', cpp_test)
            self.copy_test_file(test_bin)

        print()  # Add empty line for nicer output

    def copy_test_file(self, src_file):
        '''
        Copy ``src_file`` to `tests/bin` directory, ensuring parent directory
        exists. Messages like `creating directory /path/to/package` and
        `copying directory /src/path/to/package -> path/to/package` are
        displayed on standard output. Adapted from scikit-build.
        '''
        # Create directory if needed
        dest_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'tests', 'bin')
        if dest_dir != "" and not os.path.exists(dest_dir):
            print("creating directory {}".format(dest_dir))
            os.makedirs(dest_dir)

        # Copy file
        dest_file = os.path.join(dest_dir, os.path.basename(src_file))
        print("copying {} -> {}".format(src_file, dest_file))
        copyfile(src_file, dest_file)
        copymode(src_file, dest_file)


def build_extension_modules_list():
    result = []
    for mods in pybind_modules:
        if isinstance(mods, dict):
            result.append(CMakeExtension(mods["name"],
                                         # define_macros=[('MAJOR_VERSION', '1'), ('MINOR_VERSION', '0')],
                                         include_dirs=mods["includes"],
                                         library_dirs=mods["libraries"],
                                         libraries=mods["links"],
                                         sources=mods["sources"],
                                         )
                          )
        else:
            result.append(CMakeExtension(mods))

    return result


setup(
    name='pypp11',
    version='0.0.1',
    author='Valenza Florian',
    author_email='florian.valenza@gmail.com',
    description=' Python/C++ package',
    long_description='Python library with C++ code wrapped with use of pybind 11',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    ext_modules=build_extension_modules_list(),
    test_suite='tests',
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
)
