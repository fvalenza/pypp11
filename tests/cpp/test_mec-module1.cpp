#include <catch.hpp>

// #ifdef BUILD_MEC_MODULE1_CPP

#include "mec-module1.hpp"

TEST_CASE("Addition")
{
    REQUIRE(add(1, 1) == 2);
    REQUIRE(1 == 1);
}

// #endif
