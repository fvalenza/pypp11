cmake_minimum_required(VERSION 3.0)

PROJECT(mec-module2)

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

# As we create a static librayr, and we link it to another static library, need use of Position Independent Code flag
target_compile_options(${CPP_MODULE} PRIVATE -fPIC)


target_link_libraries(${CPP_MODULE} PRIVATE ${DUMMY_LIBRARY})
target_include_directories(${CPP_MODULE} PUBLIC ${LIBS_DIR}/dummylib/include/ )
