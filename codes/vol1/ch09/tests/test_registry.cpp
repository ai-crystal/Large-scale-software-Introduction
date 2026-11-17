// 第 9 章：命令表的单元测试
//
// 不引入第三方测试框架，用十几行宏就够了：
//   CHECK(条件)  条件不成立时打印文件、行号和表达式，并记一次失败
// 最后根据失败次数决定进程退出码，CI 靠退出码判断通过与否。

#include "../registry.h"

#include <cstdio>

static int g_failed = 0;

// do { ... } while (0) 是宏的常用写法：
// 把多条语句包成一个整体，展开后可以安全地放在 if 后面。
//
// #condition 是“字符串化”，把宏参数原样变成字符串。
// CHECK(a == b) 失败时，打印出来的就是 a == b。
#define CHECK(condition)                                                  \
    do {                                                                  \
        if (!(condition)) {                                               \
            std::printf("FAIL %s:%d  %s\n", __FILE__, __LINE__, #condition); \
            ++g_failed;                                                   \
        }                                                                 \
    } while (0)

// 测试用的空命令，什么都不做。
static void noop(const char*) {}

int main() {
    CommandTable table;

    // 场景一：添加一条命令，能查到。
    Command a;
    a.name = "hello";
    a.help = "问候";
    a.run = noop;
    a.owner = "plugin_a";
    CHECK(table.add(a));

    // 场景二：同名命令第二次添加应该失败。
    CHECK(!table.add(a));

    // 场景三：查得到和不存在的名字。
    CHECK(table.find("hello") != nullptr);
    CHECK(table.find("missing") == nullptr);

    // 场景四：再加一条属于别的插件的命令。
    Command b;
    b.name = "note";
    b.help = "记录";
    b.run = noop;
    b.owner = "plugin_b";
    CHECK(table.add(b));

    // 场景五：删除 plugin_a 的命令，只影响它自己。
    table.remove_owner("plugin_a");
    CHECK(table.find("hello") == nullptr);
    CHECK(table.find("note") != nullptr);

    std::printf("%s\n", g_failed == 0 ? "全部通过" : "有失败");
    return g_failed == 0 ? 0 : 1;
}
