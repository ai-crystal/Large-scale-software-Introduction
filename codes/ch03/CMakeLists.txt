cmake_minimum_required(VERSION 3.16)
project(ch03 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(hello_plugin SHARED hello_plugin.cpp)
add_executable(host host.cpp)

# 把插件产物放到 plugins 目录，宿主扫描这里
set_target_properties(hello_plugin PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/plugins
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/plugins)
