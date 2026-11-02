# 第 6 章的构建说明
#
# 在第 5 章的基础上多了一个事件总线，插件也多了 notes。
# 产物：
#   host.exe / host                    宿主（命令循环 + 事件）
#   plugins/hello_plugin.dll / .so     hello 命令 + 订阅 file.saved
#   plugins/notes_plugin.dll / .so     note 命令
#
# 用法：
#   cmake -B build
#   cmake --build build
#   cd build && ./host

cmake_minimum_required(VERSION 3.16)
project(ch06 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 宿主：命令表 + 事件总线 + 主程序
add_executable(host host.cpp registry.cpp events.cpp)

# 两个插件，都是动态库
add_library(hello_plugin SHARED hello_plugin.cpp)
add_library(notes_plugin SHARED notes_plugin.cpp)

# 插件产物统一放到 build/plugins
set_target_properties(hello_plugin notes_plugin PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/plugins
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/plugins)
