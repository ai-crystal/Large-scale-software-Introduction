cmake_minimum_required(VERSION 3.16)
project(mini_shell LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(host host/main.cpp host/registry.cpp host/events.cpp)
target_include_directories(host PRIVATE sdk/include)

add_subdirectory(plugins/hello)
add_subdirectory(plugins/notes)

set(PLUGIN_OUTPUT_DIR ${CMAKE_BINARY_DIR}/plugins)
set_target_properties(hello notes PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${PLUGIN_OUTPUT_DIR}
    RUNTIME_OUTPUT_DIRECTORY ${PLUGIN_OUTPUT_DIR})
