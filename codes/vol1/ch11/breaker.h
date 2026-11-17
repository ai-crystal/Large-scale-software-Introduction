// 第 11 章：熔断器
//
// 连续失败达到阈值后，直接拒绝请求，避免每次都等满超时。
// 冷却一段时间后进入“半开”，允许一次试探：
//   成功 -> 恢复（Closed）
//   失败 -> 继续断开（Open）
//
// 三个状态：
//   Closed    正常，放行
//   Open      断开，直接拒绝
//   HalfOpen  半开，允许一次试探

#pragma once

#include <chrono>

enum class BreakerState { Closed, Open, HalfOpen };

class CircuitBreaker {
public:
    explicit CircuitBreaker(int threshold = 5, int cooldown_ms = 30000)
        : threshold_(threshold), cooldown_ms_(cooldown_ms) {}

    // 每次调用前先问一句：现在允许放行吗？
    bool allow() {
        if (state_ == BreakerState::Open) {
            // 还没冷却完，继续拒绝。
            if (now_ms() - opened_at_ < cooldown_ms_) return false;

            // 冷却结束，进入半开，放一次试试。
            state_ = BreakerState::HalfOpen;
        }
        return true;
    }

    // 调用成功后告诉熔断器。
    void on_success() {
        state_ = BreakerState::Closed;
        failures_ = 0;
    }

    // 调用失败后告诉熔断器。
    void on_failure() {
        ++failures_;

        // 半开状态下失败，立刻重新断开；
        // 正常状态下，累计到阈值才断开。
        if (state_ == BreakerState::HalfOpen || failures_ >= threshold_) {
            state_ = BreakerState::Open;
            opened_at_ = now_ms();
        }
    }

    BreakerState state() const { return state_; }

private:
    // 用单调时钟，不受系统时间调整影响。
    static long long now_ms() {
        using namespace std::chrono;
        return duration_cast<milliseconds>(
            steady_clock::now().time_since_epoch()).count();
    }

    int threshold_;      // 失败多少次后断开
    int cooldown_ms_;    // 断开后冷却多久
    int failures_ = 0;   // 连续失败次数
    BreakerState state_ = BreakerState::Closed;
    long long opened_at_ = 0;   // 进入 Open 的时间
};
