// Test doubles for the controller: scripted inputs and captured output.
#pragma once

#include <string>
#include <vector>

#include "av_hal.h"

namespace avtest {

class FakeMotor : public av::MotorDriver {
 public:
  void begin() override {}
  void set(bool on, uint8_t power_pct) override {
    this->on = on;
    this->power = power_pct;
  }
  bool supports_pwm() const override { return false; }
  bool on = false;
  uint8_t power = 0;
};

class FakeHal : public av::Hal {
 public:
  bool read_s1() override { return s1; }
  bool read_s2() override { return s2; }
  bool read_estop() override { return estop; }
  av::MotorDriver& motor() override { return motor_; }
  void set_servo(uint8_t degrees) override { servo = degrees; }
  uint32_t random32() override { return next_random++; }

  bool s1 = false;
  bool s2 = false;
  bool estop = false;
  int servo = -1;
  uint32_t next_random = 0xb0071d2e;
  FakeMotor motor_;
};

class CaptureSink : public av::LineSink {
 public:
  void write_line(const char* data, size_t len) override { lines.emplace_back(data, len); }
  std::vector<std::string> lines;
};

}  // namespace avtest
