#include "example.hh"

#include <gflags/gflags.h>

#include "foo.h"

DEFINE_bool(some_flag, false, "Some flag.");

namespace bar {

int foo() {
  if (FLAGS_some_flag) {
    return 0;
  }

  return c_foo();
}

}  // namespace bar
