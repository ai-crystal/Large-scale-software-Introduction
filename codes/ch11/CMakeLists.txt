cmake_minimum_required(VERSION 3.16)
project(ch11 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(raii_demo raii_demo.cpp)
add_executable(breaker_demo breaker_demo.cpp)
