// 第 5 章：命令表的实现
//
// 每个函数都很短，但有几个地方容易写错，
// 比如删除元素时迭代器会失效，下面都有注释。

#include "registry.h"

#include <cstdio>

bool CommandTable::add(const Command& cmd) {
    // 名字为空、执行函数为空，都不是合法命令。
    if (cmd.name.empty() || !cmd.run) return false;

    // 检查重名。这一章选择“拒绝后来者”，并在日志里说清楚是谁和谁冲突。
    auto it = commands_.find(cmd.name);
    if (it != commands_.end()) {
        std::printf("命令冲突：%s 已被 %s 注册，%s 注册失败\n",
                    cmd.name.c_str(), it->second.owner.c_str(), cmd.owner.c_str());
        return false;
    }

    // 存进表。map 的 [] 会插入或覆盖，这里前面已经检查过不存在。
    commands_[cmd.name] = cmd;
    return true;
}

const Command* CommandTable::find(const std::string& name) const {
    auto it = commands_.find(name);
    // 找不到返回空指针，调用方需要判断。
    // 返回指针而不是副本，避免复制整个结构体。
    return it == commands_.end() ? nullptr : &it->second;
}

void CommandTable::remove_owner(const std::string& owner) {
    // 遍历删除时不能简单地 ++it：
    // erase 会让当前迭代器失效，必须接住它的返回值。
    for (auto it = commands_.begin(); it != commands_.end(); ) {
        if (it->second.owner == owner) {
            it = commands_.erase(it);   // erase 返回下一个位置
        } else {
            ++it;
        }
    }
}

void CommandTable::list() const {
    // %-12s 表示左对齐、占 12 个字符宽度，让输出整齐。
    for (const auto& pair : commands_) {
        std::printf("  %-12s %s\n", pair.first.c_str(), pair.second.help.c_str());
    }
}

std::vector<std::string> CommandTable::names() const {
    std::vector<std::string> result;
    for (const auto& pair : commands_) {
        result.push_back(pair.first);
    }
    return result;
}
