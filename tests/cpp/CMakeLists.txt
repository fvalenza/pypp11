cmake_minimum_required(VERSION 3.0)


include_directories(${LIBS_DIR}/catch/single_include/catch2/)
link_directories(${LIBS_DIR}/dummylib/lib)


MACRO(ADD_UNIT_TEST NAME PKGS)
    add_executable(${NAME}_test ../test_main.cpp test_${NAME}.cpp)
    FOREACH(PKG ${PKGS})
        TARGET_LINK_LIBRARIES(${NAME}_test PUBLIC ${PKG})
    ENDFOREACH(PKG)
ENDMACRO(ADD_UNIT_TEST)

# mec-module1.cpp
IF($ENV{BUILD_MEC_MODULE1_CPP} AND $ENV{BUILD_MEC_MODULE1_PYTHON})
    message("tests/cpp/cmakelist module1")
    ADD_UNIT_TEST(mec-module1 mec-module1 )
ENDIF($ENV{BUILD_MEC_MODULE1_CPP} AND $ENV{BUILD_MEC_MODULE1_PYTHON})

# mec-module2.cpp
IF($ENV{BUILD_MEC_MODULE2_CPP} AND $ENV{BUILD_MEC_MODULE2_PYTHON})
    ADD_UNIT_TEST(mec-module2 "mec-module2;dummylib" )
ENDIF($ENV{BUILD_MEC_MODULE2_CPP} AND $ENV{BUILD_MEC_MODULE2_PYTHON})
