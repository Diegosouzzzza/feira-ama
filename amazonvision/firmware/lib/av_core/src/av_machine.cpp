#include "av_machine.h"

namespace av {

const char* name(State s) {
  switch (s) {
    case State::DISARMED: return "DISARMED";
    case State::READY: return "READY";
    case State::TO_S1: return "TO_S1";
    case State::SETTLING: return "SETTLING";
    case State::INSPECTING: return "INSPECTING";
    case State::REVIEW_HOLD: return "REVIEW_HOLD";
    case State::TO_S2: return "TO_S2";
    case State::SORTING: return "SORTING";
    case State::RELEASING: return "RELEASING";
    case State::FAULT: return "FAULT";
    case State::ESTOP: return "ESTOP";
    case State::MAINTENANCE: return "MAINTENANCE";
    default: return "?";
  }
}

const char* name(Trigger t) {
  switch (t) {
    case Trigger::HELLO: return "HELLO";
    case Trigger::ARM: return "ARM";
    case Trigger::STOP: return "STOP";
    case Trigger::START_CYCLE: return "START_CYCLE";
    case Trigger::DECISION: return "DECISION";
    case Trigger::HOLD_FOR_REVIEW: return "HOLD_FOR_REVIEW";
    case Trigger::CLEAR_FAULT: return "CLEAR_FAULT";
    case Trigger::ENTER_MAINTENANCE: return "ENTER_MAINTENANCE";
    case Trigger::EXIT_MAINTENANCE: return "EXIT_MAINTENANCE";
    case Trigger::S1_PRESENT: return "S1_PRESENT";
    case Trigger::SETTLED: return "SETTLED";
    case Trigger::S2_PRESENT: return "S2_PRESENT";
    case Trigger::SORT_DONE: return "SORT_DONE";
    case Trigger::RELEASED: return "RELEASED";
    case Trigger::TIMEOUT: return "TIMEOUT";
    case Trigger::LINK_LOST: return "LINK_LOST";
    case Trigger::ESTOP_PRESSED: return "ESTOP_PRESSED";
    case Trigger::ESTOP_RELEASED: return "ESTOP_RELEASED";
    default: return "?";
  }
}

const char* name(Fault f) {
  switch (f) {
    case Fault::S1_TIMEOUT: return "S1_TIMEOUT";
    case Fault::DECISION_TIMEOUT: return "DECISION_TIMEOUT";
    case Fault::S2_TIMEOUT: return "S2_TIMEOUT";
    case Fault::EXIT_BLOCKED: return "EXIT_BLOCKED";
    case Fault::LINK_LOST: return "LINK_LOST";
    case Fault::SESSION_REPLACED: return "SESSION_REPLACED";
    case Fault::SENSOR_CONFLICT: return "SENSOR_CONFLICT";
    case Fault::INTERNAL: return "INTERNAL";
    default: return "NONE";
  }
}

bool is_cycle_state(State s) {
  switch (s) {
    case State::TO_S1:
    case State::SETTLING:
    case State::INSPECTING:
    case State::REVIEW_HOLD:
    case State::TO_S2:
    case State::SORTING:
    case State::RELEASING:
      return true;
    default:
      return false;
  }
}

bool is_motion_state(State s) {
  return s == State::TO_S1 || s == State::TO_S2 || s == State::SORTING || s == State::RELEASING;
}

bool is_safe_state(State s) {
  return s == State::DISARMED || s == State::FAULT || s == State::ESTOP || s == State::MAINTENANCE;
}

Fault timeout_fault(State s) {
  switch (s) {
    case State::TO_S1: return Fault::S1_TIMEOUT;
    case State::INSPECTING: return Fault::DECISION_TIMEOUT;
    case State::TO_S2: return Fault::S2_TIMEOUT;
    case State::RELEASING: return Fault::EXIT_BLOCKED;
    default: return Fault::NONE;
  }
}

bool next_state(State s, Trigger t, State* out) {
  // Rules shared by many states (same construction as the Python table).
  if (t == Trigger::ESTOP_PRESSED && s != State::ESTOP) {
    *out = State::ESTOP;
    return true;
  }
  if (is_cycle_state(s)) {
    if (t == Trigger::HELLO || t == Trigger::LINK_LOST) {
      *out = State::FAULT;
      return true;
    }
    if (t == Trigger::STOP) {
      *out = State::DISARMED;
      return true;
    }
  }
  if (t == Trigger::TIMEOUT && timeout_fault(s) != Fault::NONE) {
    *out = State::FAULT;
    return true;
  }

  struct Row {
    State from;
    Trigger trigger;
    State to;
  };
  static const Row kRows[] = {
      {State::DISARMED, Trigger::HELLO, State::DISARMED},
      {State::DISARMED, Trigger::ARM, State::READY},
      {State::DISARMED, Trigger::ENTER_MAINTENANCE, State::MAINTENANCE},
      {State::READY, Trigger::HELLO, State::DISARMED},
      {State::READY, Trigger::STOP, State::DISARMED},
      {State::READY, Trigger::LINK_LOST, State::DISARMED},
      {State::READY, Trigger::START_CYCLE, State::TO_S1},
      {State::TO_S1, Trigger::S1_PRESENT, State::SETTLING},
      {State::SETTLING, Trigger::SETTLED, State::INSPECTING},
      {State::INSPECTING, Trigger::DECISION, State::TO_S2},
      {State::INSPECTING, Trigger::HOLD_FOR_REVIEW, State::REVIEW_HOLD},
      {State::REVIEW_HOLD, Trigger::DECISION, State::TO_S2},
      {State::TO_S2, Trigger::S2_PRESENT, State::SORTING},
      {State::SORTING, Trigger::SORT_DONE, State::RELEASING},
      {State::RELEASING, Trigger::RELEASED, State::READY},
      {State::FAULT, Trigger::HELLO, State::FAULT},
      {State::FAULT, Trigger::CLEAR_FAULT, State::DISARMED},
      {State::ESTOP, Trigger::HELLO, State::ESTOP},
      {State::ESTOP, Trigger::ESTOP_RELEASED, State::DISARMED},
      {State::MAINTENANCE, Trigger::HELLO, State::DISARMED},
      {State::MAINTENANCE, Trigger::STOP, State::DISARMED},
      {State::MAINTENANCE, Trigger::LINK_LOST, State::DISARMED},
      {State::MAINTENANCE, Trigger::EXIT_MAINTENANCE, State::DISARMED},
  };
  for (const Row& row : kRows) {
    if (row.from == s && row.trigger == t) {
      *out = row.to;
      return true;
    }
  }
  return false;
}

}  // namespace av
