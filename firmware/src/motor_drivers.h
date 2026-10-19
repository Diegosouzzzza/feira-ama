// Conveyor motor drivers. Add a class here when a new driver is chosen; the controller only sees
// av::MotorDriver.
#pragma once

#include <Arduino.h>

#include "av_hal.h"
#include "board_config.h"

class OnOffMotor : public av::MotorDriver {
 public:
  explicit OnOffMotor(uint8_t pin) : pin_(pin) {}
  void begin() override {
    pinMode(pin_, OUTPUT);
    digitalWrite(pin_, LOW);
  }
  void set(bool on, uint8_t) override { digitalWrite(pin_, on ? HIGH : LOW); }
  bool supports_pwm() const override { return false; }

 private:
  uint8_t pin_;
};

// BTS7960 / IBT-2: forward only. power_pct 0 = full speed.
class Bts7960Motor : public av::MotorDriver {
 public:
  void begin() override {
    pinMode(AV_PIN_BTS_EN, OUTPUT);
    pinMode(AV_PIN_BTS_LPWM, OUTPUT);
    digitalWrite(AV_PIN_BTS_LPWM, LOW);
    digitalWrite(AV_PIN_BTS_EN, LOW);
    ledcSetup(AV_MOTOR_LEDC_CHANNEL, AV_MOTOR_PWM_HZ, 8);
    ledcAttachPin(AV_PIN_BTS_RPWM, AV_MOTOR_LEDC_CHANNEL);
    ledcWrite(AV_MOTOR_LEDC_CHANNEL, 0);
  }
  void set(bool on, uint8_t power_pct) override {
    if (!on) {
      ledcWrite(AV_MOTOR_LEDC_CHANNEL, 0);
      digitalWrite(AV_PIN_BTS_EN, LOW);
      return;
    }
    uint8_t pct = power_pct == 0 ? 100 : power_pct;
    digitalWrite(AV_PIN_BTS_EN, HIGH);
    ledcWrite(AV_MOTOR_LEDC_CHANNEL, static_cast<uint32_t>(pct) * 255 / 100);
  }
  bool supports_pwm() const override { return true; }
};
