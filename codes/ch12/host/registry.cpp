#include "registry.h"
#include <cstdio>

bool CommandTable::add(const Command& cmd) {
    if (cmd.name.empty() || !cmd.run) return false;

    auto it = commands_.find(cmd.name);
    if (it != commands_.end()) {
        std::printf("命令冲突：%s 已被 %s 注册，%s 注册失败\n",
                    cmd.name.c_str(), it->second.owner.c_str(), cmd.owner.c_str());
        return false;
    }
    commands_[cmd.name] = cmd;
    return true;
}

const Command* CommandTable::find(const std::string& name) const {
    auto it = commands_.find(name);
    return it == commands_.end() ? nullptr : &it->second;
}

void CommandTable::remove_owner(const std::string& owner) {
    for (auto it = commands_.begin(); it != commands_.end(); ) {
        if (it->second.owner == owner) it = commands_.erase(it);
        else ++it;
    }
}

void CommandTable::list() const {
    for (const auto& pair : commands_) {
        std::printf("  %-12s %s\n", pair.first.c_str(), pair.second.help.c_str());
    }
}

std::vector<std::string> CommandTable::names() const {
    std::vector<std::string> result;
    for (const auto& pair : commands_) result.push_back(pair.first);
    return result;
}
