// 第 6 章：事件总线的实现

#include "events.h"

void EventBus::on(const std::string& type, const std::string& owner,
                  void (*fn)(const char*, const char*), int priority) {
    if (!fn) return;

    // 取出这个事件的订阅者列表。
    // 如果还没有人订阅过，map 的 [] 会自动建一个空列表。
    auto& list = listeners_[type];
    list.push_back({ owner, priority, fn });

    // 按优先级排序。stable_sort 是稳定排序，
    // 相同优先级的订阅者保持注册顺序，不会被排乱。
    std::stable_sort(list.begin(), list.end(),
                     [](const Listener& a, const Listener& b) {
                         return a.priority < b.priority;
                     });
}

void EventBus::emit(const std::string& type, const std::string& payload) {
    auto it = listeners_.find(type);
    if (it == listeners_.end()) return;   // 没人订阅，直接返回

    // 复制一份列表再遍历。
    // 因为订阅者在处理过程中可能取消订阅，
    // 直接遍历原列表会跳过元素或者访问失效的内存。
    auto snapshot = it->second;
    for (const auto& listener : snapshot) {
        listener.fn(type.c_str(), payload.c_str());
    }
}

void EventBus::remove_owner(const std::string& owner) {
    for (auto& pair : listeners_) {
        auto& list = pair.second;

        // remove_if 把满足条件的元素移到末尾，返回新的逻辑结尾，
        // erase 再把末尾那段真正删掉。
        list.erase(std::remove_if(list.begin(), list.end(),
                                  [&](const Listener& l) {
                                      return l.owner == owner;
                                  }),
                   list.end());
    }
}
