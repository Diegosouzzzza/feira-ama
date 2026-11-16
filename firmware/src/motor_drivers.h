// Conveyor motor drivers. Add a class here when a new driver is chosen; the controller only sees
// av::MotorDriver.
#pragma once

#include <Arduino.h>

#include "av_hal.h"
#include "board_config.h"

// Plain on/off output (relay module, or a MOSFET that must not be PWM-driven). Not the default:
// build with -DAV_MOTOR_DRIVER=0 to use it.
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

// Logic-level MOSFET module (D4184) switched low-side, with speed control by PWM (LEDC).
// power_pct 0 = full speed, so TEST_MOTOR works before CONFIGURE and when motor_power_pct is
// left empty.
class PwmMosfetMotor : public av::MotorDriver {
 public:
  explicit PwmMosfetMotor(uint8_t pin) : pin_(pin) {}
  void begin() override {
    // Hold the gate low while the pin changes from GPIO to LEDC: the belt never twitches.
    digitalWrite(pin_, LOW);
    pinMode(pin_, OUTPUT);
    ledcSetup(AV_MOTOR_LEDC_CHANNEL, AV_MOTOR_PWM_HZ, AV_MOTOR_PWM_BITS);
    ledcWrite(AV_MOTOR_LEDC_CHANNEL, 0);
    ledcAttachPin(pin_, AV_MOTOR_LEDC_CHANNEL);
    ledcWrite(AV_MOTOR_LEDC_CHANNEL, 0);
  }
  void set(bool on, uint8_t power_pct) override {
    ledcWrite(AV_MOTOR_LEDC_CHANNEL, on ? av::pwm_duty(power_pct, kMaxDuty) : 0);
  }
  bool supports_pwm() const override { return true; }

 private:
  static constexpr uint32_t kMaxDuty = (1UL << AV_MOTOR_PWM_BITS) - 1;
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
    ledcSetup(AV_MOTOR_LEDC_CHANNEL, AV_MOTOR_PWM_HZ, AV_MOTOR_PWM_BITS);
    ledcAttachPin(AV_PIN_BTS_RPWM, AV_MOTOR_LEDC_CHANNEL);
    ledcWrite(AV_MOTOR_LEDC_CHANNEL, 0);
  }
  void set(bool on, uint8_t power_pct) override {
    if (!on) {
      ledcWrite(AV_MOTOR_LEDC_CHANNEL, 0);
      digitalWrite(AV_PIN_BTS_EN, LOW);
      return;
    }
    digitalWrite(AV_PIN_BTS_EN, HIGH);
    ledcWrite(AV_MOTOR_LEDC_CHANNEL, av::pwm_duty(power_pct, (1UL << AV_MOTOR_PWM_BITS) - 1));
  }
  bool supports_pwm() const override { return true; }
};
