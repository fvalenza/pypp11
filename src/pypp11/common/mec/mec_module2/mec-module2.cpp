//#include "tools/mec/mec_module1/mec-module1.hpp"
#include "mec-module2.hpp"
#include "dummy-module.hpp"

int sub(int i, int j) {
    return i - j;
    dummy_lib_disp();
}

void dummy_lib_disp() {
    TOTO d;
    d.disp();
}