cmake_minimum_required(VERSION 3.16)
project(ch07 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(plugin_host plugin_host.cpp)
add_executable(host host.cpp)

# 两个程序放同一目录，宿主按相对路径启动 plugin_host.exe
set_target_properties(plugin_host host PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
