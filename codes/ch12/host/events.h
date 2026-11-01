// 第 6 章：事件总线
//
// 事件总线的职责：
//   1. 记下“谁对哪个事件感兴趣”       —— on
//   2. 事件发生时，挨个通知他们        —— emit
//   3. 插件卸载时，把它的订阅清掉      —— remove_owner
//
// 它不关心事件的含义，只负责转发。

#pragma once

#include <algorithm>
#include <map>
#include <string>
#include <vector>

// 一个订阅者。
struct Listener {
    std::string owner;   // 哪个插件订阅的，卸载时按它清理
    int priority;        // 数字小的先执行
    void (*fn)(const char* type, const char* payload);   // 回调函数
};

class EventBus {
public:
    // 订阅。同一个事件可以有很多订阅者。
    void on(const std::string& type, const std::string& owner,
            void (*fn)(const char*, const char*), int priority = 100);

    // 发布。把事件送给这个类型下的所有订阅者。
    void emit(const std::string& type, const std::string& payload);

    // 删除某个插件的所有订阅。
    void remove_owner(const std::string& owner);

private:
    // 键是事件名，值是订阅者列表。
    std::map<std::string, std::vector<Listener>> listeners_;
};
