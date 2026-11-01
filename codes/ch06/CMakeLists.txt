# 第 6 章的构建说明
#
# 两个产物：
#   host.exe / host                宿主（需要 events.cpp）
#   plugins/hello_plugin.dll/.so   订阅事件的插件
#
# 用法：
#   cmake -B build
#   cmake --build build
#   cd build && ./host

cmake_minimum_required(VERSION 3.16)
project(ch06 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 宿主：主程序 + 事件总线实现
add_executable(host host.cpp events.cpp)

# 插件：动态库
add_library(hello_plugin SHARED hello_plugin.cpp)

# 插件产物放到 build/plugins
set_target_properties(hello_plugin PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/plugins
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/plugins)
