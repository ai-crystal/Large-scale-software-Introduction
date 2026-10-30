cmake_minimum_required(VERSION 3.16)
project(ch05 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(host host.cpp registry.cpp)
add_library(hello_plugin SHARED hello_plugin.cpp)
add_library(notes_plugin SHARED notes_plugin.cpp)

set_target_properties(hello_plugin notes_plugin PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/plugins
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/plugins)
