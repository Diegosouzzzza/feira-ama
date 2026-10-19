// Serial protocol v1 (docs/protocolo-serial.md). Validation mirrors the Pydantic models in
// api/src/amazonvision/machine/protocol.py; the contract examples are checked by native tests.
#pragma once

#include <stddef.h>
#include <stdint.h>

namespace av {

constexpr int kProtocolVersion = 1;
constexpr size_t kMaxLineBytes = 1024;  // including the trailing '\n'

enum class Cmd : uint8_t {
  HELLO,
  CONFIGURE,
  ARM,
  STOP,
  START_CYCLE,
  DECISION,
  HOLD_FOR_REVIEW,
  CLEAR_FAULT,
  ENTER_MAINTENANCE,
  EXIT_MAINTENANCE,
  GET_STATUS,
  TEST_MOTOR,
  TEST_SERVO,
  COUNT
};

enum class Nak : uint8_t {
  BAD_JSON,
  LINE_TOO_LONG,
  UNSUPPORTED_VERSION,
  UNKNOWN_COMMAND,
  INVALID_PAYLOAD,
  NO_SESSION,
  SESSION_MISMATCH,
  INVALID_STATE,
  CYCLE_MISMATCH,
  NOT_CONFIGURED,
  PRECONDITION_FAILED
};

enum class Destination : uint8_t { APPROVED, REJECTED };

const char* name(Cmd c);
const char* name(Nak n);
const char* name(Destination d);

struct BenchConfig {
  uint16_t sensor_debounce_ms;
  uint16_t s1_timeout_ms;
  uint16_t settle_ms;
  uint16_t decision_timeout_ms;
  uint16_t s2_timeout_ms;
  uint8_t servo_rest_deg;
  uint8_t servo_reject_deg;
  uint16_t reject_hold_ms;
  uint16_t reject_motor_ms;
  uint16_t release_ms;
  uint16_t release_max_ms;
  uint16_t link_timeout_ms;
  uint8_t motor_power_pct;  // 0 = on/off driver (no PWM)
};

struct HostMessage {
  bool heartbeat;
  char session_id[9];
  char cmd_id[25];
  Cmd cmd;
  int32_t lot_id;
  int32_t cycle_id;
  Destination destination;
  BenchConfig config;
  uint16_t run_ms;
  uint8_t angle_deg;
  uint16_t hold_ms;
};

struct ParseError {
  Nak code;
  char detail[81];
};

// Parses one line (without the '\n'). Returns true and fills `out`, or returns false and fills
// `error` with the same code the host-side validator would produce.
bool parse_host_line(const char* line, size_t len, HostMessage* out, ParseError* error);

}  // namespace av
