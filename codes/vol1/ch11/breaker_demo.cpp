// 第 11 章：熔断器演示
//
// 阈值设成 2、冷却 1 秒，方便观察状态变化：
// 前两次放行并失败，之后被拒绝；等一秒，再放行一次试探。

#include "breaker.h"

#include <cstdio>

#ifdef _WIN32
#include <windows.h>
#endif

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif

    // 失败 2 次就断开，冷却 1000 毫秒。
    CircuitBreaker breaker(2, 1000);

    for (int i = 0; i < 5; ++i) {
        // 每次调用前先问熔断器。
        if (!breaker.allow()) {
            std::printf("第 %d 次：被熔断拒绝\n", i + 1);
            continue;
        }

        std::printf("第 %d 次：放行\n", i + 1);

        // 这里假设调用失败了。
        breaker.on_failure();
    }

    return 0;
}
