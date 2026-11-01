# 第 12 章：hello 插件的构建说明
#
# 只做一件事：把 src/plugin.cpp 编译成动态库。
# 插件名 hello 要和 plugin.cpp 里 plugin_name() 返回的名字一致。

add_library(hello SHARED src/plugin.cpp)

# 头文件在项目的 sdk/include 下，用 CMAKE_SOURCE_DIR 找到项目根。
target_include_directories(hello PRIVATE ${CMAKE_SOURCE_DIR}/sdk/include)
