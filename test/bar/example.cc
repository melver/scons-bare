#include "bar/example.hh"

#include <gtest/gtest.h>

TEST(mylib, Foo) { ASSERT_EQ(bar::foo(), 42); }
