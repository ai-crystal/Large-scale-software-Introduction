#include "events.h"

void EventBus::on(const std::string& type, const std::string& owner,
                  void (*fn)(const char*, const char*), int priority) {
    if (!fn) return;
    auto& list = listeners_[type];
    list.push_back({ owner, priority, fn });
    std::stable_sort(list.begin(), list.end(),
                     [](const Listener& a, const Listener& b) {
                         return a.priority < b.priority;
                     });
}

void EventBus::emit(const std::string& type, const std::string& payload) {
    auto it = listeners_.find(type);
    if (it == listeners_.end()) return;
    auto snapshot = it->second;
    for (const auto& listener : snapshot) {
        listener.fn(type.c_str(), payload.c_str());
    }
}

void EventBus::remove_owner(const std::string& owner) {
    for (auto& pair : listeners_) {
        auto& list = pair.second;
        list.erase(std::remove_if(list.begin(), list.end(),
                                  [&](const Listener& l) { return l.owner == owner; }),
                   list.end());
    }
}
