# 第 5 章的构建说明
#
# 三个产物：
#   host.exe / host                    宿主
#   plugins/hello_plugin.dll / .so     hello 插件
#   plugins/notes_plugin.dll / .so     notes 插件
#
# 用法：
#   cmake -B build
#   cmake --build build
#   cd build && ./host

cmake_minimum_required(VERSION 3.16)
project(ch05 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 宿主需要两个源文件：
#   host.cpp     加载插件、命令循环
#   registry.cpp 命令表的增删查
add_executable(host host.cpp registry.cpp)

# 两个插件，都是动态库
add_library(hello_plugin SHARED hello_plugin.cpp)
add_library(notes_plugin SHARED notes_plugin.cpp)

# 插件产物统一放到 build/plugins，宿主扫描这个目录
set_target_properties(hello_plugin notes_plugin PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/plugins
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/plugins)
