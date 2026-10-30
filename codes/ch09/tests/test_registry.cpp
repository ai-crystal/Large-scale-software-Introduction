#include "../registry.h"
#include <cstdio>

static int g_failed = 0;

#define CHECK(condition)                                                  \
    do {                                                                  \
        if (!(condition)) {                                               \
            std::printf("FAIL %s:%d  %s\n", __FILE__, __LINE__, #condition); \
            ++g_failed;                                                   \
        }                                                                 \
    } while (0)

static void noop(const char*) {}

int main() {
    CommandTable table;

    Command a;
    a.name = "hello";
    a.help = "问候";
    a.run = noop;
    a.owner = "plugin_a";
    CHECK(table.add(a));
    CHECK(!table.add(a));                  // 重名，第二次应失败
    CHECK(table.find("hello") != nullptr);
    CHECK(table.find("missing") == nullptr);

    Command b;
    b.name = "note";
    b.help = "记录";
    b.run = noop;
    b.owner = "plugin_b";
    CHECK(table.add(b));

    table.remove_owner("plugin_a");
    CHECK(table.find("hello") == nullptr);
    CHECK(table.find("note") != nullptr);

    std::printf("%s\n", g_failed == 0 ? "全部通过" : "有失败");
    return g_failed == 0 ? 0 : 1;
}
