# 第 2 章的构建说明
#
# CMake 不直接编译，它根据这份说明生成当前平台能用的构建文件
# （Windows 上生成 Visual Studio 工程，Linux 上生成 Makefile）。
#
# 用法：
#   cmake -B build
#   cmake --build build

cmake_minimum_required(VERSION 3.16)   # 需要 3.16 以上版本

project(ch02 LANGUAGES CXX)            # 项目名 ch02，使用 C++

set(CMAKE_CXX_STANDARD 17)             # 用 C++17 标准
set(CMAKE_CXX_STANDARD_REQUIRED ON)    # 编译器不支持就直接报错，不要偷偷退回旧标准

# 生成一个叫 app 的可执行文件，源文件是这两个。
# 两个 .cpp 会分别编译，再链接到一起。
add_executable(app main.cpp commands.cpp)
