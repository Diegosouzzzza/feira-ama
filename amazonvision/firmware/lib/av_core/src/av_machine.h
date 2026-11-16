// Bench state machine. Mirrors api/src/amazonvision/domain/machine.py; a native test compares
// both tables (docs/maquina-de-estados.md is the shared reference).
#pragma once

#include <stdint.h>

namespace av {

enum class State : uint8_t {
  DISARMED,
  READY,
  TO_S1,
  SETTLING,
  INSPECTING,
  REVIEW_HOLD,
  TO_S2,
  SORTING,
  RELEASING,
  FAULT,
  ESTOP,
  MAINTENANCE,
  COUNT
};

enum class Trigger : uint8_t {
  HELLO,
  ARM,
  STOP,
  START_CYCLE,
  DECISION,
  HOLD_FOR_REVIEW,
  CLEAR_FAULT,
  ENTER_MAINTENANCE,
  EXIT_MAINTENANCE,
  S1_PRESENT,
  SETTLED,
  S2_PRESENT,
  SORT_DONE,
  RELEASED,
  TIMEOUT,
  LINK_LOST,
  ESTOP_PRESSED,
  ESTOP_RELEASED,
  COUNT
};

enum class Fault : uint8_t {
  NONE,
  S1_TIMEOUT,
  DECISION_TIMEOUT,
  S2_TIMEOUT,
  EXIT_BLOCKED,
  LINK_LOST,
  SESSION_REPLACED,
  SENSOR_CONFLICT,
  INTERNAL
};

const char* name(State s);
const char* name(Trigger t);
const char* name(Fault f);

bool is_cycle_state(State s);
bool is_motion_state(State s);
bool is_safe_state(State s);  // DISARMED, FAULT, ESTOP, MAINTENANCE

// Writes the next state and returns true, or returns false when the trigger is not allowed.
bool next_state(State s, Trigger t, State* out);

// Fault raised when the state's deadline expires (NONE if the state has no deadline).
Fault timeout_fault(State s);

}  // namespace av
