add_library(hello SHARED src/plugin.cpp)
target_include_directories(hello PRIVATE ${CMAKE_SOURCE_DIR}/sdk/include)
