# 第 9 章的构建说明
#
# 两个产物：
#   mock_host.exe        假宿主，用来单独验证插件
#   test_registry.exe    命令表的单元测试
#
# 用法：
#   cmake -B build
#   cmake --build build
#   ctest --test-dir build --output-on-failure

cmake_minimum_required(VERSION 3.16)
project(ch09 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 假宿主：只需要接口头文件
add_executable(mock_host mock_host.cpp)
target_include_directories(mock_host PRIVATE sdk/include)

# 单元测试：要带上命令表的实现
add_executable(test_registry tests/test_registry.cpp registry.cpp)
target_include_directories(test_registry PRIVATE sdk/include)

# 注册到 ctest，之后可以用 ctest 一条命令跑完所有测试
enable_testing()
add_test(NAME registry COMMAND test_registry)
