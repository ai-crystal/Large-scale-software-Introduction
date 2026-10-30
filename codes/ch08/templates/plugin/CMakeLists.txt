cmake_minimum_required(VERSION 3.16)
project({{name}} LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library({{name}} SHARED src/plugin.cpp)
target_include_directories({{name}} PRIVATE include)
