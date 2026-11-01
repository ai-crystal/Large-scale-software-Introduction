# 第 12 章：完整最小外壳的构建说明
#
# 产物：
#   build/host.exe              宿主
#   build/plugins/hello.dll     hello 插件
#   build/plugins/notes.dll     notes 插件
#
# 用法：
#   cmake -B build
#   cmake --build build
#   cd build && ./host

cmake_minimum_required(VERSION 3.16)
project(mini_shell LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 宿主：主程序、命令表、事件总线三个源文件
add_executable(host host/main.cpp host/registry.cpp host/events.cpp)
target_include_directories(host PRIVATE sdk/include)

# 两个插件，各自的构建说明在同目录的 CMakeLists.txt 里
add_subdirectory(plugins/hello)
add_subdirectory(plugins/notes)

# 插件产物统一放到 build/plugins，宿主扫描这个目录
set(PLUGIN_OUTPUT_DIR ${CMAKE_BINARY_DIR}/plugins)
set_target_properties(hello notes PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${PLUGIN_OUTPUT_DIR}
    RUNTIME_OUTPUT_DIRECTORY ${PLUGIN_OUTPUT_DIR})
