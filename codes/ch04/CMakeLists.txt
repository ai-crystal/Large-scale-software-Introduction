# 第 4 章的构建说明
#
# 两个产物：
#   hello_plugin.dll / .so   插件
#   host.exe / host          宿主
#
# 用法：
#   cmake -B build
#   cmake --build build
#   cd build && ./host

cmake_minimum_required(VERSION 3.16)
project(ch04 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 插件：动态库
add_library(hello_plugin SHARED hello_plugin.cpp)

# 宿主：可执行文件
add_executable(host host.cpp)

# 插件产物放到 build/plugins，宿主扫描这个目录
set_target_properties(hello_plugin PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/plugins
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/plugins)
