# 第 11 章的构建说明
#
# 两个可执行文件：
#   raii_demo.exe     演示文件句柄和 unique_ptr 的自动释放
#   breaker_demo.exe  演示熔断器的状态变化
#
# 用法：
#   cmake -B build
#   cmake --build build

cmake_minimum_required(VERSION 3.16)
project(ch11 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# RAII 示例
add_executable(raii_demo raii_demo.cpp)

# 熔断器示例
add_executable(breaker_demo breaker_demo.cpp)
