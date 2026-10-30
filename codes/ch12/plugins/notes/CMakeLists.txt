add_library(notes SHARED src/plugin.cpp)
target_include_directories(notes PRIVATE ${CMAKE_SOURCE_DIR}/sdk/include)
