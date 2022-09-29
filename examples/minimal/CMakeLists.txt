cmake_minimum_required(VERSION 3.15)

project(minimal
  VERSION
    0.1.0
  DESCRIPTION
    "My project description"
)

enable_testing()

add_subdirectory(c_files)
add_subdirectory(tests)
