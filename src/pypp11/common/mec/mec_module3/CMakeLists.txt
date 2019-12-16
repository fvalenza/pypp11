cmake_minimum_required(VERSION 3.0)

PROJECT(mec-module3)

SET(CPP_MODULE ${PROJECT_NAME})


# ----------------------------------------------------
# --- C++ Sources ------------------------------------
# ----------------------------------------------------
set(SOURCES_CPP_MODULE
    ${CPP_MODULE}.cpp
    )

find_package( PkgConfig )
pkg_check_modules( EIGEN3 REQUIRED eigen3 )
# include_directories( ${EIGEN3_INCLUDE_DIRS} )
# message(${EIGEN3_INCLUDE_DIRS})

# Create library of module
add_library(${CPP_MODULE} ${SOURCES_CPP_MODULE} )

# As we create a static librayr, and we link it to another static library, need use of Position Independent Code flag
target_compile_options(${CPP_MODULE} PRIVATE -fPIC)

# target_include_directories(${CPP_MODULE} PUBLIC /usr/include/eigen3)
target_include_directories(${CPP_MODULE} PUBLIC ${EIGEN3_INCLUDE_DIRS})
