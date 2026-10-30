#pragma once

#include <algorithm>
#include <map>
#include <string>
#include <vector>

struct Listener {
    std::string owner;
    int priority;
    void (*fn)(const char* type, const char* payload);
};

class EventBus {
public:
    void on(const std::string& type, const std::string& owner,
            void (*fn)(const char*, const char*), int priority = 100);

    void emit(const std::string& type, const std::string& payload);
    void remove_owner(const std::string& owner);

private:
    std::map<std::string, std::vector<Listener>> listeners_;
};
