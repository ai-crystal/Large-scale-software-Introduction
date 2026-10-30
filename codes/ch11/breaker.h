#pragma once

#include <chrono>

enum class BreakerState { Closed, Open, HalfOpen };

class CircuitBreaker {
public:
    explicit CircuitBreaker(int threshold = 5, int cooldown_ms = 30000)
        : threshold_(threshold), cooldown_ms_(cooldown_ms) {}

    bool allow() {
        if (state_ == BreakerState::Open) {
            if (now_ms() - opened_at_ < cooldown_ms_) return false;
            state_ = BreakerState::HalfOpen;
        }
        return true;
    }

    void on_success() {
        state_ = BreakerState::Closed;
        failures_ = 0;
    }

    void on_failure() {
        ++failures_;
        if (state_ == BreakerState::HalfOpen || failures_ >= threshold_) {
            state_ = BreakerState::Open;
            opened_at_ = now_ms();
        }
    }

    BreakerState state() const { return state_; }

private:
    static long long now_ms() {
        using namespace std::chrono;
        return duration_cast<milliseconds>(
            steady_clock::now().time_since_epoch()).count();
    }

    int threshold_;
    int cooldown_ms_;
    int failures_ = 0;
    BreakerState state_ = BreakerState::Closed;
    long long opened_at_ = 0;
};
