cmake_minimum_required(VERSION 3.0)

# expose_mec_module1
IF($ENV{BUILD_MEC_MODULE1_CPP} AND $ENV{BUILD_MEC_MODULE1_PYTHON})
    message("mec/cmakelists module1")
    add_subdirectory(mec_module1)
    # add_definitions(-DBUILD_MEC_MODULE1_CPP)
ENDIF($ENV{BUILD_MEC_MODULE1_CPP} AND $ENV{BUILD_MEC_MODULE1_PYTHON})

# expose_mec_module2
IF($ENV{BUILD_MEC_MODULE2_CPP} AND $ENV{BUILD_MEC_MODULE2_PYTHON})
    message("mec/cmakelists module2")
    add_subdirectory(mec_module2)
ENDIF($ENV{BUILD_MEC_MODULE2_CPP} AND $ENV{BUILD_MEC_MODULE2_PYTHON})

# expose_mec_module3
IF($ENV{BUILD_MEC_MODULE3_CPP} AND $ENV{BUILD_MEC_MODULE3_PYTHON})
    message("mec/cmakelists module3")
    add_subdirectory(mec_module3)
    # add_definitions(-DBUILD_MEC_MODULE1_CPP)
ENDIF($ENV{BUILD_MEC_MODULE3_CPP} AND $ENV{BUILD_MEC_MODULE3_PYTHON})
