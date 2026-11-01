# 第 7 章的构建说明
#
# 两个可执行文件：
#   plugin_host.exe   插件进程（被宿主启动）
#   host.exe          宿主
#
# 它们必须放在同一个目录，因为宿主按相对路径启动 plugin_host.exe。
#
# 用法：
#   cmake -B build
#   cmake --build build
#   cd build && ./host

cmake_minimum_required(VERSION 3.16)
project(ch07 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 插件进程：一个独立的小程序
add_executable(plugin_host plugin_host.cpp)

# 宿主：启动插件进程并通过管道通信
add_executable(host host.cpp)

# 两个都放到 build 根目录，保证相对路径能找到
set_target_properties(plugin_host host PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
