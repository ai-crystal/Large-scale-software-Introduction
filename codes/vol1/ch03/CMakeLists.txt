# 第 3 章的构建说明
#
# 这个工程生成两个东西：
#   hello_plugin.dll / .so   插件（动态库）
#   host.exe / host          宿主（可执行文件）
#
# 用法：
#   cmake -B build
#   cmake --build build
#   cd build && ./host

cmake_minimum_required(VERSION 3.16)
project(ch03 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 生成动态库。SHARED 是关键，不写的话默认生成静态库，
# 静态库不能被运行时加载，也就不能当插件用。
add_library(hello_plugin SHARED hello_plugin.cpp)

# 生成宿主可执行文件。
add_executable(host host.cpp)

# 把插件的产物统一放到 build/plugins 目录，
# 宿主正好扫描这个目录。Windows 看 .dll，Linux 看 .so。
set_target_properties(hello_plugin PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/plugins
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/plugins)
