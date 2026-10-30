cmake_minimum_required(VERSION 3.16)
project(ch09 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(mock_host mock_host.cpp)
target_include_directories(mock_host PRIVATE sdk/include)

add_executable(test_registry tests/test_registry.cpp registry.cpp)
target_include_directories(test_registry PRIVATE sdk/include)

enable_testing()
add_test(NAME registry COMMAND test_registry)
