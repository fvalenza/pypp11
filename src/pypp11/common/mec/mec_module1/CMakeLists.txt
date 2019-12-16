cmake_minimum_required(VERSION 3.0)

PROJECT(mec-module1)

SET(CPP_MODULE ${PROJECT_NAME})


# ----------------------------------------------------
# --- C++ Sources ------------------------------------
# ----------------------------------------------------
set(SOURCES_CPP_MODULE
    ${CPP_MODULE}.cpp
    )



# Create library of module
add_library(${CPP_MODULE} ${SOURCES_CPP_MODULE} )
