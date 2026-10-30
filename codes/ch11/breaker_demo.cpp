#include "breaker.h"
#include <cstdio>

int main() {
    CircuitBreaker breaker(2, 1000);

    for (int i = 0; i < 5; ++i) {
        if (!breaker.allow()) {
            std::printf("第 %d 次：被熔断拒绝\n", i + 1);
            continue;
        }
        std::printf("第 %d 次：放行\n", i + 1);
        breaker.on_failure();
    }
    return 0;
}
