#pragma once

#include "plugin_api.h"
#include <map>
#include <string>
#include <vector>

struct Command {
    std::string name;
    std::string help;
    CommandFn run;
    std::string owner;
};

class CommandTable {
public:
    bool add(const Command& cmd);
    const Command* find(const std::string& name) const;
    void remove_owner(const std::string& owner);
    void list() const;
    std::vector<std::string> names() const;

private:
    std::map<std::string, Command> commands_;
};
