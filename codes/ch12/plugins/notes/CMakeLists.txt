# 第 12 章：notes 插件的构建说明
#
# 和 hello 插件结构完全一样，只是名字不同。
add_library(notes SHARED src/plugin.cpp)
target_include_directories(notes PRIVATE ${CMAKE_SOURCE_DIR}/sdk/include)
