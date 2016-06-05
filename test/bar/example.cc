#define BOOST_TEST_DYN_LINK
#include <boost/test/unit_test.hpp>

#include "bar/example.hh"

BOOST_AUTO_TEST_SUITE(mylib)

BOOST_AUTO_TEST_CASE(Foo) { BOOST_CHECK_EQUAL(bar::foo(), 42); }

BOOST_AUTO_TEST_SUITE_END()
