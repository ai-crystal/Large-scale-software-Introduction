// 第 5 章：命令表
//
// 这张表回答三个问题：
//   1. 某个名字对应哪条命令？        —— find
//   2. 这条命令是谁注册的？          —— owner 字段
//   3. 某个插件卸载时，删掉它注册的？ —— remove_owner
//
// 表本身不关心命令具体做什么，只负责保存和查找。

#pragma once

#include "plugin_api.h"

#include <map>
#include <string>
#include <vector>

// 表里存的一条记录。
// owner 是插件名，卸载时按它批量删除。
struct Command {
    std::string name;
    std::string help;
    CommandFn run;
    std::string owner;
};

class CommandTable {
public:
    // 添加一条命令。
    // 返回 true 表示成功，false 表示名字重复或者参数不合法。
    bool add(const Command& cmd);

    // 按名字查找。找不到返回空指针。
    const Command* find(const std::string& name) const;

    // 删除某个插件注册的所有命令。
    void remove_owner(const std::string& owner);

    // 打印全部命令，help 命令会调用它。
    void list() const;

    // 返回所有命令名，调试或补全时可能用到。
    std::vector<std::string> names() const;

private:
    // 键是命令名，值是命令本身。
    std::map<std::string, Command> commands_;
};
