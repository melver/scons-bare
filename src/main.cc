#include <gflags/gflags.h>

#include "bar/example.hh"

int main(int argc, char *argv[]) {
  gflags::SetUsageMessage("...");
  gflags::ParseCommandLineFlags(&argc, &argv, true);

  return bar::foo();
}
