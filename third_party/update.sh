#!/usr/bin/env bash
git submodule update --init

cd "${0%/*}"

# Google Test
cd googletest
cmake .
make

cd ../gflags
cmake .
make
