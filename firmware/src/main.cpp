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
  // Fail-safe NC contact (E12 NF 11-12 to GND): closed (normal) = LOW; open (pressed or broken wire) = HIGH.
  bool read_estop() override { return digitalRead(AV_PIN_ESTOP) == HIGH; }
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
#elif AV_MOTOR_DRIVER == 1
  PwmMosfetMotor motor_{AV_PIN_MOTOR_EN};
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
  bool led_r = false;
  bool led_g = false;
  bool led_y = false;
  bool relay_k1 = false;
  bool buzzer = false;

  switch (controller.state()) {
    case av::State::FAULT:
    case av::State::ESTOP:
      on = (now / 150) % 2;
      led_r = true;
      relay_k1 = false;  // Cut +12V_AT immediately on E-STOP or FAULT
      buzzer = (now / 250) % 2;
      break;
    case av::State::DISARMED:
    case av::State::MAINTENANCE:
      on = (now / 700) % 2;
      led_y = true;
      relay_k1 = (controller.state() == av::State::MAINTENANCE) && !hal.read_estop();
      break;
    default:
      on = true;
      led_g = true;
      relay_k1 = !hal.read_estop();
      break;
  }
  digitalWrite(AV_PIN_LED, on ? HIGH : LOW);
  digitalWrite(AV_PIN_LED_R, led_r ? HIGH : LOW);
  digitalWrite(AV_PIN_LED_G, led_g ? HIGH : LOW);
  digitalWrite(AV_PIN_LED_Y, led_y ? HIGH : LOW);
  digitalWrite(AV_PIN_RELAY_K1, relay_k1 ? HIGH : LOW);
  digitalWrite(AV_PIN_BUZZER, buzzer ? HIGH : LOW);
}

}  // namespace

void setup() {
  // Safe boot initialization: drive all actuator/alarm outputs LOW before enabling OUTPUT drivers.
  digitalWrite(AV_PIN_RELAY_K1, LOW);
  digitalWrite(AV_PIN_BUZZER, LOW);
  digitalWrite(AV_PIN_LED_R, LOW);
  digitalWrite(AV_PIN_LED_G, LOW);
  digitalWrite(AV_PIN_LED_Y, LOW);
  digitalWrite(AV_PIN_LED, LOW);

  pinMode(AV_PIN_RELAY_K1, OUTPUT);
  pinMode(AV_PIN_BUZZER, OUTPUT);
  pinMode(AV_PIN_LED_R, OUTPUT);
  pinMode(AV_PIN_LED_G, OUTPUT);
  pinMode(AV_PIN_LED_Y, OUTPUT);
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
