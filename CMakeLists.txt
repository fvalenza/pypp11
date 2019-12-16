cmake_minimum_required(VERSION 2.8.12)
project(pypp11)

SET(CMAKE_CXX_STANDARD 11)

# ----------------------------------------------------
# --- ENV VARS -----------------------------------
# ----------------------------------------------------
SET(LIBS_DIR $ENV{PYPP11_EXTERNAL_LIBS_DIR})

# ----------------------------------------------------
# --- MACROS -----------------------------------------
# ----------------------------------------------------
MACRO(ADD_PYBIND_MODULE NAME SRC_DIR PKGS LINK_DIRS)
    SET(CPP_MODULE ${NAME})
    STRING(REGEX REPLACE "_" "-" CPP_MODULE ${CPP_MODULE})
    pybind11_add_module(expose_${NAME} ${SRC_DIR}/expose-${CPP_MODULE}.cpp)
    TARGET_LINK_LIBRARIES(expose_${NAME} PRIVATE ${CPP_MODULE})
    FOREACH(PKG ${PKGS})
        TARGET_LINK_LIBRARIES(expose_${NAME} PRIVATE ${PKG})
    ENDFOREACH(PKG)
    FOREACH(LDIR ${LINK_DIRS})
        TARGET_LINK_LIBRARIES(expose_${NAME} PRIVATE -L${LDIR})
    ENDFOREACH(LDIR)
ENDMACRO(ADD_PYBIND_MODULE)



include_directories("include/")


add_subdirectory(external_libraries/pybind11)

# --- MAIN LIBRARY -------------------------------------------------------------
add_subdirectory(src)


# --- C++ MODULES EXPOSED ------------------------------------------------------

# expose_mec_module1
IF($ENV{BUILD_MEC_MODULE1_CPP} AND $ENV{BUILD_MEC_MODULE1_PYTHON})
    message("cmakelists module1")
    ADD_PYBIND_MODULE(mec_module1 src/pypp11/common/mec/mec_module1 "" "")
ENDIF($ENV{BUILD_MEC_MODULE1_CPP} AND $ENV{BUILD_MEC_MODULE1_PYTHON})

# expose_mec_module2
IF($ENV{BUILD_MEC_MODULE2_CPP} AND $ENV{BUILD_MEC_MODULE2_PYTHON})
    ADD_PYBIND_MODULE(mec_module2 src/pypp11/common/mec/mec_module2 "dummylib" "${LIBS_DIR}/dummylib/lib")
ENDIF($ENV{BUILD_MEC_MODULE2_CPP} AND $ENV{BUILD_MEC_MODULE2_PYTHON})

# expose_mec_module3
IF($ENV{BUILD_MEC_MODULE3_CPP} AND $ENV{BUILD_MEC_MODULE3_PYTHON})
    ADD_PYBIND_MODULE(mec_module3 src/pypp11/common/mec/mec_module3 "" "")
ENDIF($ENV{BUILD_MEC_MODULE3_CPP} AND $ENV{BUILD_MEC_MODULE3_PYTHON})


# --- UNIT TESTS ---------------------------------------------------------------
add_subdirectory(tests)
