#include "av_controller.h"

#include <ArduinoJson.h>
#include <stdio.h>
#include <string.h>

namespace av {

namespace {

constexpr uint32_t elapsed(uint32_t now, uint32_t since) { return now - since; }

uint32_t fnv1a(const void* data, size_t len) {
  const uint8_t* p = static_cast<const uint8_t*>(data);
  uint32_t h = 2166136261u;
  for (size_t i = 0; i < len; ++i) {
    h ^= p[i];
    h *= 16777619u;
  }
  return h;
}

}  // namespace

Controller::Controller(Hal& hal, LineSink& out, const char* firmware_version)
    : hal_(hal), out_(out), firmware_version_(firmware_version) {}

// ------------------------------------------------------------------ lifecycle

void Controller::begin(uint32_t now_ms) {
  now_ = now_ms;
  snprintf(boot_id_, sizeof(boot_id_), "%08x", static_cast<unsigned>(hal_.random32()));
  has_session_ = false;
  session_id_[0] = '\0';
  seq_ = 0;
  booted_at_ = now_ms;
  last_host_ = now_ms;
  last_heartbeat_ = now_ms - kHeartbeatMs;
  configured_ = false;
  config_ = {};
  config_hash_[0] = '\0';
  fault_ = Fault::NONE;
  test_active_ = false;
  clear_cycle();
  for (CachedReply& r : cache_) r.used = false;
  cache_next_ = 0;

  // Physical inputs are taken as they are at power-on; no events for the initial reading.
  s1_ = {hal_.read_s1(), false, now_ms};
  s1_.stable = s1_.raw;
  s2_ = {hal_.read_s2(), false, now_ms};
  s2_.stable = s2_.raw;
  estop_ = {hal_.read_estop(), false, now_ms};
  estop_.stable = estop_.raw;

  hal_.motor().begin();
  motor_on_ = false;
  hal_.motor().set(false, 0);
  servo_deg_ = 0;
  state_ = estop_.stable ? State::ESTOP : State::DISARMED;
  phase_started_ = now_ms;
}

void Controller::tick(uint32_t now_ms) {
  now_ = now_ms;
  read_inputs(now_ms);

  if (has_session_) {
    uint16_t limit = configured_ ? config_.link_timeout_ms : kDefaultLinkTimeoutMs;
    if (elapsed(now_ms, last_host_) >= limit) {
      if (is_cycle_state(state_)) {
        transition(Trigger::LINK_LOST, Fault::LINK_LOST);
      } else if (state_ == State::READY || state_ == State::MAINTENANCE) {
        transition(Trigger::LINK_LOST);
      }
    }
  }

  run_phase(now_ms);

  if (elapsed(now_ms, last_heartbeat_) >= kHeartbeatMs) {
    last_heartbeat_ = now_ms;
    emit_heartbeat();
  }
}

uint16_t Controller::debounce_ms() const {
  return configured_ ? config_.sensor_debounce_ms : kDefaultDebounceMs;
}

void Controller::read_inputs(uint32_t now) {
  struct Input {
    Debounced* d;
    bool raw;
    const char* name;
  } inputs[] = {
      {&s1_, hal_.read_s1(), "S1"},
      {&s2_, hal_.read_s2(), "S2"},
      {&estop_, hal_.read_estop(), "ESTOP"},
  };
  for (Input& in : inputs) {
    Debounced& d = *in.d;
    if (in.raw != d.raw) {
      d.raw = in.raw;
      d.changed_at = now;
    }
    if (d.raw == d.stable || elapsed(now, d.changed_at) < debounce_ms()) continue;
    d.stable = d.raw;
    emit_sensor(in.name, d.stable);
    if (in.d == &estop_) {
      if (d.stable) {
        transition(Trigger::ESTOP_PRESSED, Fault::NONE, "ESTOP");
      } else {
        transition(Trigger::ESTOP_RELEASED);
      }
    }
  }
}

void Controller::run_phase(uint32_t now) {
  const uint32_t t = elapsed(now, phase_started_);
  switch (state_) {
    case State::TO_S1:
      if (s1_.stable) {
        motor(false);
        transition(Trigger::S1_PRESENT);
      } else if (t >= config_.s1_timeout_ms) {
        transition(Trigger::TIMEOUT, Fault::S1_TIMEOUT);
      }
      break;
    case State::SETTLING:
      if (t >= config_.settle_ms) {
        transition(Trigger::SETTLED);
        emit_capture_ready();
      }
      break;
    case State::INSPECTING:
      if (t >= config_.decision_timeout_ms) transition(Trigger::TIMEOUT, Fault::DECISION_TIMEOUT);
      break;
    case State::TO_S2:
      if (s2_.stable) {
        motor(false);
        transition(Trigger::S2_PRESENT);
      } else if (t >= config_.s2_timeout_ms) {
        transition(Trigger::TIMEOUT, Fault::S2_TIMEOUT);
      }
      break;
    case State::SORTING:
      if (t >= sort_duration_) {
        motor(false);
        servo_deg_ = config_.servo_rest_deg;
        hal_.set_servo(servo_deg_);
        transition(Trigger::SORT_DONE);
      }
      break;
    case State::RELEASING:
      if (t >= config_.release_ms && !s1_.stable && !s2_.stable) {
        motor(false);
        Destination destination = destination_;
        int32_t cycle = cycle_id_;
        transition(Trigger::RELEASED);
        cycle_id_ = cycle;
        emit_cycle_completed(destination);
        clear_cycle();
      } else if (t >= config_.release_max_ms) {
        transition(Trigger::TIMEOUT, Fault::EXIT_BLOCKED);
      }
      break;
    case State::MAINTENANCE:
      if (test_active_ && static_cast<int32_t>(now - test_until_) >= 0) {
        test_active_ = false;
        actuators_safe();
      }
      break;
    default:
      break;
  }
}

// ------------------------------------------------------------------ state machine

void Controller::motor(bool on) {
  motor_on_ = on;
  hal_.motor().set(on, on ? config_.motor_power_pct : 0);
}

void Controller::actuators_safe() {
  motor(false);
  if (configured_) {
    servo_deg_ = config_.servo_rest_deg;
    hal_.set_servo(servo_deg_);
  }
}

void Controller::clear_cycle() {
  lot_id_ = 0;
  cycle_id_ = 0;
  has_destination_ = false;
}

void Controller::enter(State s) {
  phase_started_ = now_;
  switch (s) {
    case State::TO_S1:
    case State::TO_S2:
      motor(true);
      break;
    case State::SETTLING:
      motor(false);
      break;
    case State::SORTING:
      if (destination_ == Destination::REJECTED) {
        servo_deg_ = config_.servo_reject_deg;
        hal_.set_servo(servo_deg_);
        motor(config_.reject_motor_ms > 0);
        sort_duration_ = config_.reject_hold_ms > config_.reject_motor_ms ? config_.reject_hold_ms
                                                                         : config_.reject_motor_ms;
      } else {
        sort_duration_ = 0;
      }
      break;
    case State::RELEASING:
      motor(true);
      break;
    default:
      break;
  }
}

bool Controller::transition(Trigger trigger, Fault fault, const char* abort_reason) {
  State target;
  if (!next_state(state_, trigger, &target)) return false;
  const State previous = state_;
  const bool aborting = is_cycle_state(previous) && is_safe_state(target);
  const bool entering_fault = target == State::FAULT && previous != State::FAULT;
  state_ = target;
  if (is_safe_state(target)) {
    test_active_ = false;
    actuators_safe();
  }
  if (previous == target) return true;
  if (entering_fault) fault_ = fault != Fault::NONE ? fault : Fault::INTERNAL;
  emit_state_changed(previous, target, trigger);
  if (entering_fault) emit_fault();
  if (aborting && cycle_id_ > 0) {
    const char* reason = abort_reason;
    if (reason == nullptr) reason = target == State::FAULT ? name(fault_) : "STOP";
    emit_cycle_aborted(reason);
    clear_cycle();
  }
  enter(target);
  return true;
}

// ------------------------------------------------------------------ host input

void Controller::handle_line_too_long(uint32_t now_ms) {
  now_ = now_ms;
  last_host_ = now_ms;
  emit_nak(nullptr, Cmd::HELLO, Nak::LINE_TOO_LONG, "linha longa demais");
}

void Controller::handle_line(const char* line, size_t len, uint32_t now_ms) {
  now_ = now_ms;
  last_host_ = now_ms;
  HostMessage msg;
  ParseError error;
  if (!parse_host_line(line, len, &msg, &error)) {
    emit_nak(nullptr, Cmd::HELLO, error.code, error.detail);
    return;
  }
  if (msg.heartbeat) return;
  if (const CachedReply* previous = cached(msg.cmd_id)) {
    replay(*previous);
    return;
  }
  if (msg.cmd == Cmd::HELLO) {
    memcpy(session_id_, msg.session_id, sizeof(session_id_));
    has_session_ = true;
    transition(Trigger::HELLO, Fault::SESSION_REPLACED);
    char payload[48];
    snprintf(payload, sizeof(payload), "{\"fw_version\":\"%.16s\"}", firmware_version_);
    reply_ok(msg, payload);
    return;
  }
  if (!has_session_ && msg.cmd != Cmd::GET_STATUS) {
    reply_err(msg, Nak::NO_SESSION);
    return;
  }
  if (has_session_ && strcmp(msg.session_id, session_id_) != 0) {
    emit_nak(msg.cmd_id, msg.cmd, Nak::SESSION_MISMATCH, nullptr);
    return;
  }
  on_command(msg);
}

void Controller::on_command(const HostMessage& msg) {
  char detail[40];
  switch (msg.cmd) {
    case Cmd::CONFIGURE: {
      if (state_ != State::DISARMED && state_ != State::READY) {
        snprintf(detail, sizeof(detail), "estado %s", name(state_));
        return reply_err(msg, Nak::INVALID_STATE, detail);
      }
      config_ = msg.config;
      configured_ = true;
      snprintf(config_hash_, sizeof(config_hash_), "%08x",
               static_cast<unsigned>(fnv1a(&config_, sizeof(config_))));
      servo_deg_ = config_.servo_rest_deg;
      hal_.set_servo(servo_deg_);
      char payload[40];
      snprintf(payload, sizeof(payload), "{\"config_hash\":\"%s\"}", config_hash_);
      return reply_ok(msg, payload);
    }
    case Cmd::ARM:
      if (state_ != State::DISARMED) {
        snprintf(detail, sizeof(detail), "estado %s", name(state_));
        return reply_err(msg, Nak::INVALID_STATE, detail);
      }
      if (!configured_) return reply_err(msg, Nak::NOT_CONFIGURED);
      if (estop_.stable) return reply_err(msg, Nak::PRECONDITION_FAILED, "emergencia acionada");
      if (s1_.stable || s2_.stable) return reply_err(msg, Nak::PRECONDITION_FAILED, "sensor ocupado");
      transition(Trigger::ARM);
      return reply_ok(msg);
    case Cmd::STOP:
      if (!transition(Trigger::STOP, Fault::NONE, "STOP")) {
        snprintf(detail, sizeof(detail), "estado %s", name(state_));
        return reply_err(msg, Nak::INVALID_STATE, detail);
      }
      return reply_ok(msg);
    case Cmd::START_CYCLE:
      if (state_ != State::READY) {
        snprintf(detail, sizeof(detail), "estado %s", name(state_));
        return reply_err(msg, Nak::INVALID_STATE, detail);
      }
      if (s2_.stable) return reply_err(msg, Nak::PRECONDITION_FAILED, "S2 ocupado");
      lot_id_ = msg.lot_id;
      cycle_id_ = msg.cycle_id;
      reply_ok(msg);
      transition(Trigger::START_CYCLE);
      return;
    case Cmd::DECISION:
      if (state_ != State::INSPECTING && state_ != State::REVIEW_HOLD) {
        snprintf(detail, sizeof(detail), "estado %s", name(state_));
        return reply_err(msg, Nak::INVALID_STATE, detail);
      }
      if (msg.cycle_id != cycle_id_) return reply_err(msg, Nak::CYCLE_MISMATCH);
      destination_ = msg.destination;
      has_destination_ = true;
      reply_ok(msg);
      transition(Trigger::DECISION);
      return;
    case Cmd::HOLD_FOR_REVIEW:
      if (state_ != State::INSPECTING) {
        snprintf(detail, sizeof(detail), "estado %s", name(state_));
        return reply_err(msg, Nak::INVALID_STATE, detail);
      }
      if (msg.cycle_id != cycle_id_) return reply_err(msg, Nak::CYCLE_MISMATCH);
      reply_ok(msg);
      transition(Trigger::HOLD_FOR_REVIEW);
      return;
    case Cmd::CLEAR_FAULT:
      if (state_ != State::FAULT) {
        snprintf(detail, sizeof(detail), "estado %s", name(state_));
        return reply_err(msg, Nak::INVALID_STATE, detail);
      }
      if (s1_.stable || s2_.stable) return reply_err(msg, Nak::PRECONDITION_FAILED, "sensor ocupado");
      fault_ = Fault::NONE;
      transition(Trigger::CLEAR_FAULT);
      return reply_ok(msg);
    case Cmd::ENTER_MAINTENANCE:
    case Cmd::EXIT_MAINTENANCE: {
      Trigger t = msg.cmd == Cmd::ENTER_MAINTENANCE ? Trigger::ENTER_MAINTENANCE
                                                     : Trigger::EXIT_MAINTENANCE;
      if (!transition(t)) {
        snprintf(detail, sizeof(detail), "estado %s", name(state_));
        return reply_err(msg, Nak::INVALID_STATE, detail);
      }
      return reply_ok(msg);
    }
    case Cmd::GET_STATUS: {
      char status[360];
      status_json(status, sizeof(status));
      char payload[400];
      snprintf(payload, sizeof(payload), "{\"status\":%s}", status);
      return reply_ok(msg, payload);
    }
    case Cmd::TEST_MOTOR:
      if (state_ != State::MAINTENANCE) return reply_err(msg, Nak::INVALID_STATE, "fora da manutencao");
      reply_ok(msg);
      motor(true);
      test_until_ = now_ + msg.run_ms;
      test_active_ = true;
      return;
    case Cmd::TEST_SERVO:
      if (state_ != State::MAINTENANCE) return reply_err(msg, Nak::INVALID_STATE, "fora da manutencao");
      reply_ok(msg);
      servo_deg_ = msg.angle_deg;
      hal_.set_servo(servo_deg_);
      test_until_ = now_ + msg.hold_ms;
      test_active_ = true;
      return;
    default:
      return reply_err(msg, Nak::UNKNOWN_COMMAND);
  }
}

// ------------------------------------------------------------------ replies and idempotency

void Controller::reply_ok(const HostMessage& msg, const char* payload_json) {
  CachedReply reply;
  reply.used = true;
  reply.ack = true;
  memcpy(reply.cmd_id, msg.cmd_id, sizeof(reply.cmd_id));
  reply.cmd = msg.cmd;
  snprintf(reply.payload, sizeof(reply.payload), "%s", payload_json);
  emit_ack(msg, reply.payload);
  remember(reply);
}

void Controller::reply_err(const HostMessage& msg, Nak code, const char* detail) {
  CachedReply reply;
  reply.used = true;
  reply.ack = false;
  memcpy(reply.cmd_id, msg.cmd_id, sizeof(reply.cmd_id));
  reply.cmd = msg.cmd;
  reply.code = code;
  if (detail) snprintf(reply.detail, sizeof(reply.detail), "%s", detail);
  emit_nak(msg.cmd_id, msg.cmd, code, detail);
  remember(reply);
}

void Controller::remember(const CachedReply& reply) {
  cache_[cache_next_] = reply;
  cache_next_ = (cache_next_ + 1) % kCmdCache;
}

const Controller::CachedReply* Controller::cached(const char* cmd_id) const {
  for (const CachedReply& r : cache_) {
    if (r.used && strcmp(r.cmd_id, cmd_id) == 0) return &r;
  }
  return nullptr;
}

// ------------------------------------------------------------------ serialization

namespace {

class Envelope {
 public:
  Envelope(const char* boot_id, const char* session_id, bool has_session, uint32_t seq,
           State state, const char* type) {
    doc_["protocol_version"] = kProtocolVersion;
    doc_["boot_id"] = boot_id;
    if (has_session) doc_["session_id"] = session_id;
    doc_["seq"] = seq;
    doc_["state"] = name(state);
    doc_["type"] = type;
  }
  JsonDocument& doc() { return doc_; }
  void send(LineSink& out) {
    char buf[kMaxLineBytes];
    size_t n = serializeJson(doc_, buf, sizeof(buf));
    out.write_line(buf, n);
  }

 private:
  JsonDocument doc_;
};

}  // namespace

void Controller::emit_ack(const HostMessage& msg, const char* payload_json) {
  Envelope e(boot_id_, session_id_, has_session_, ++seq_, state_, "ack");
  e.doc()["cmd_id"] = msg.cmd_id;
  e.doc()["name"] = name(msg.cmd);
  e.doc()["duplicate"] = false;
  e.doc()["payload"] = serialized(payload_json);
  e.send(out_);
}

void Controller::emit_nak(const char* cmd_id, Cmd, Nak code, const char* detail) {
  Envelope e(boot_id_, session_id_, has_session_, ++seq_, state_, "nak");
  if (cmd_id) e.doc()["cmd_id"] = cmd_id;
  e.doc()["code"] = name(code);
  if (detail && detail[0]) e.doc()["detail"] = detail;
  e.doc()["duplicate"] = false;
  e.send(out_);
}

void Controller::replay(const CachedReply& reply) {
  Envelope e(boot_id_, session_id_, has_session_, ++seq_, state_, reply.ack ? "ack" : "nak");
  e.doc()["cmd_id"] = reply.cmd_id;
  if (reply.ack) {
    e.doc()["name"] = name(reply.cmd);
    e.doc()["payload"] = serialized(reply.payload);
  } else {
    e.doc()["code"] = name(reply.code);
    if (reply.detail[0]) e.doc()["detail"] = reply.detail;
  }
  e.doc()["duplicate"] = true;
  e.send(out_);
}

void Controller::emit_state_changed(State from, State to, Trigger trigger) {
  Envelope e(boot_id_, session_id_, has_session_, ++seq_, state_, "evt");
  e.doc()["name"] = "STATE_CHANGED";
  if (cycle_id_ > 0) e.doc()["cycle_id"] = cycle_id_;
  JsonObject p = e.doc()["payload"].to<JsonObject>();
  p["from_state"] = name(from);
  p["to_state"] = name(to);
  p["trigger"] = name(trigger);
  if (to == State::FAULT) p["fault"] = name(fault_);
  e.send(out_);
}

void Controller::emit_sensor(const char* sensor, bool active) {
  Envelope e(boot_id_, session_id_, has_session_, ++seq_, state_, "evt");
  e.doc()["name"] = "SENSOR_CHANGED";
  if (cycle_id_ > 0) e.doc()["cycle_id"] = cycle_id_;
  JsonObject p = e.doc()["payload"].to<JsonObject>();
  p["sensor"] = sensor;
  p["active"] = active;
  e.send(out_);
}

void Controller::emit_capture_ready() {
  Envelope e(boot_id_, session_id_, has_session_, ++seq_, state_, "evt");
  e.doc()["name"] = "CAPTURE_READY";
  e.doc()["cycle_id"] = cycle_id_;
  e.doc()["payload"].to<JsonObject>();
  e.send(out_);
}

void Controller::emit_cycle_completed(Destination destination) {
  Envelope e(boot_id_, session_id_, has_session_, ++seq_, state_, "evt");
  e.doc()["name"] = "CYCLE_COMPLETED";
  e.doc()["cycle_id"] = cycle_id_;
  e.doc()["payload"]["destination"] = name(destination);
  e.send(out_);
}

void Controller::emit_cycle_aborted(const char* reason) {
  Envelope e(boot_id_, session_id_, has_session_, ++seq_, state_, "evt");
  e.doc()["name"] = "CYCLE_ABORTED";
  e.doc()["cycle_id"] = cycle_id_;
  e.doc()["payload"]["reason"] = reason;
  e.send(out_);
}

void Controller::emit_fault() {
  Envelope e(boot_id_, session_id_, has_session_, ++seq_, state_, "evt");
  e.doc()["name"] = "FAULT";
  if (cycle_id_ > 0) e.doc()["cycle_id"] = cycle_id_;
  e.doc()["payload"]["code"] = name(fault_);
  e.send(out_);
}

void Controller::status_json(char* buf, size_t size) const {
  JsonDocument doc;
  doc["s1"] = s1_.stable;
  doc["s2"] = s2_.stable;
  doc["estop"] = estop_.stable;
  doc["motor_on"] = motor_on_;
  doc["servo_deg_cmd"] = servo_deg_;
  doc["configured"] = configured_;
  if (cycle_id_ > 0) {
    doc["lot_id"] = lot_id_;
    doc["cycle_id"] = cycle_id_;
  }
  if (has_destination_) doc["destination"] = name(destination_);
  if (fault_ != Fault::NONE) doc["fault"] = name(fault_);
  doc["uptime_ms"] = now_ - booted_at_;
  serializeJson(doc, buf, size);
}

void Controller::emit_heartbeat() {
  char status[360];
  status_json(status, sizeof(status));
  Envelope e(boot_id_, session_id_, has_session_, ++seq_, state_, "hb");
  e.doc()["payload"] = serialized(static_cast<const char*>(status));
  e.send(out_);
}

}  // namespace av
