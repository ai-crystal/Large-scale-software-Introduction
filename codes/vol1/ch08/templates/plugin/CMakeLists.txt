# 第 8 章：插件模板的构建说明
#
# {{name}} 是占位符，生成时会被替换成实际插件名。
# 生成 hello 插件后，这里会变成 project(hello ...) 和 add_library(hello ...)。
#
# 编译：
#   cmake -B build
#   cmake --build build

cmake_minimum_required(VERSION 3.16)
project({{name}} LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 生成动态库。SHARED 表示插件，不是普通可执行文件。
add_library({{name}} SHARED src/plugin.cpp)

# 头文件搜索路径：源码里写 #include "plugin_api.h" 就能找到。
target_include_directories({{name}} PRIVATE include)
