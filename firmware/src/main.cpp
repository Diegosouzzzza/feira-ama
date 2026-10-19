// AmazonVision 4.0 — ESP32 entry point. Only board glue lives here: the behaviour is in
// lib/av_core (tested natively against the protocol contract).
#include <Arduino.h>
#include <esp_system.h>

#include "av_controller.h"
#include "board_config.h"
#include "motor_drivers.h"

namespace {

class SerialSink : public av::LineSink {
 public:
  void write_line(const char* data, size_t len) override {
    Serial.write(reinterpret_cast<const uint8_t*>(data), len);
    Serial.write('\n');
  }
};

bool active(uint8_t pin) {
  bool high = digitalRead(pin) == HIGH;
  return AV_INPUTS_ACTIVE_LOW ? !high : high;
}

class BoardHal : public av::Hal {
 public:
  void begin() {
    pinMode(AV_PIN_S1, INPUT_PULLUP);
    pinMode(AV_PIN_S2, INPUT_PULLUP);
    pinMode(AV_PIN_ESTOP, INPUT_PULLUP);
    ledcSetup(AV_SERVO_LEDC_CHANNEL, 50, 16);
  }
  bool read_s1() override { return active(AV_PIN_S1); }
  bool read_s2() override { return active(AV_PIN_S2); }
  bool read_estop() override { return digitalRead(AV_PIN_ESTOP) == LOW; }
  av::MotorDriver& motor() override { return motor_; }
  void set_servo(uint8_t degrees) override {
    if (!servo_attached_) {
      // Attach only once a position is known: at power-on the servo is left unpowered.
      ledcAttachPin(AV_PIN_SERVO, AV_SERVO_LEDC_CHANNEL);
      servo_attached_ = true;
    }
    uint32_t us = AV_SERVO_MIN_US + (AV_SERVO_MAX_US - AV_SERVO_MIN_US) * degrees / 180;
    ledcWrite(AV_SERVO_LEDC_CHANNEL, us * 65535UL / 20000UL);  // 20 ms period, 16-bit duty
  }
  uint32_t random32() override { return esp_random(); }

 private:
#if AV_MOTOR_DRIVER == 2
  Bts7960Motor motor_;
#else
  OnOffMotor motor_{AV_PIN_MOTOR_EN};
#endif
  bool servo_attached_ = false;
};

SerialSink sink;
BoardHal hal;
av::Controller controller(hal, sink, AV_FIRMWARE_VERSION);

char line[av::kMaxLineBytes];
size_t line_len = 0;
bool line_overflow = false;

void read_serial(uint32_t now) {
  while (Serial.available() > 0) {
    char c = static_cast<char>(Serial.read());
    if (c == '\r') continue;
    if (c == '\n') {
      if (line_overflow) {
        controller.handle_line_too_long(now);
      } else if (line_len > 0) {
        controller.handle_line(line, line_len, now);
      }
      line_len = 0;
      line_overflow = false;
      continue;
    }
    if (line_len < sizeof(line) - 1) {
      line[line_len++] = c;
    } else {
      line_overflow = true;  // keep discarding until the newline
    }
  }
}

void update_led(uint32_t now) {
  bool on;
  switch (controller.state()) {
    case av::State::FAULT:
    case av::State::ESTOP:
      on = (now / 150) % 2;
      break;
    case av::State::DISARMED:
    case av::State::MAINTENANCE:
      on = (now / 700) % 2;
      break;
    default:
      on = true;
  }
  digitalWrite(AV_PIN_LED, on ? HIGH : LOW);
}

}  // namespace

void setup() {
  pinMode(AV_PIN_LED, OUTPUT);
  Serial.setRxBufferSize(2048);
  Serial.begin(AV_SERIAL_BAUD);
  hal.begin();
  controller.begin(millis());
}

void loop() {
  const uint32_t now = millis();
  read_serial(now);
  controller.tick(now);
  update_led(now);
  delay(1);  // yield; every timing in the controller is millisecond based
}
