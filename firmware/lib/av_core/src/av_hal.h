// Hardware boundary of the controller. The real board implements it in src/; native tests and
// the PC harness implement it with simulated physics.
#pragma once

#include <stddef.h>
#include <stdint.h>

namespace av {

// Conveyor motor. The driver depends on the belt that will be bought (on/off MOSFET or relay,
// BTS7960 H-bridge, ...): the controller only asks for on/off and an optional power percentage.
class MotorDriver {
 public:
  virtual ~MotorDriver() = default;
  virtual void begin() = 0;
  // power_pct: 0 means "full / on-off driver"; 1..100 only when the driver supports PWM.
  virtual void set(bool on, uint8_t power_pct) = 0;
  virtual bool supports_pwm() const = 0;
};

class Hal {
 public:
  virtual ~Hal() = default;
  // Raw (not debounced) inputs, already converted to "active = true".
  virtual bool read_s1() = 0;
  virtual bool read_s2() = 0;
  virtual bool read_estop() = 0;
  virtual MotorDriver& motor() = 0;
  virtual void set_servo(uint8_t degrees) = 0;
  virtual uint32_t random32() = 0;
};

class LineSink {
 public:
  virtual ~LineSink() = default;
  // One complete protocol line, without the trailing '\n'.
  virtual void write_line(const char* data, size_t len) = 0;
};

}  // namespace av
