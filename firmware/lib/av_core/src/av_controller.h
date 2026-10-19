// Bench controller: the ESP32 side of the protocol. Behaviour matches the simulated device used by
// the API tests (api/src/amazonvision/machine/simulated_device.py), but driven by real time and
// real sensors. No blocking calls: everything advances in tick().
#pragma once

#include <stddef.h>
#include <stdint.h>

#include "av_hal.h"
#include "av_machine.h"
#include "av_protocol.h"

namespace av {

class Controller {
 public:
  static constexpr uint32_t kHeartbeatMs = 1000;
  static constexpr uint16_t kDefaultDebounceMs = 20;
  static constexpr uint16_t kDefaultLinkTimeoutMs = 2000;
  static constexpr size_t kCmdCache = 16;

  Controller(Hal& hal, LineSink& out, const char* firmware_version);

  // Power-on (or reset): new boot_id, no session, actuators safe. Never moves anything.
  void begin(uint32_t now_ms);
  void handle_line(const char* line, size_t len, uint32_t now_ms);
  void handle_line_too_long(uint32_t now_ms);
  void tick(uint32_t now_ms);

  State state() const { return state_; }
  Fault fault() const { return fault_; }
  const char* boot_id() const { return boot_id_; }
  bool configured() const { return configured_; }
  bool motor_on() const { return motor_on_; }
  uint8_t servo_deg() const { return servo_deg_; }
  uint8_t servo_rest_deg() const { return config_.servo_rest_deg; }

 private:
  struct Debounced {
    bool raw = false;
    bool stable = false;
    uint32_t changed_at = 0;
  };

  struct CachedReply {
    bool used = false;
    bool ack = false;
    char cmd_id[25] = {};
    Cmd cmd = Cmd::HELLO;
    Nak code = Nak::BAD_JSON;
    char detail[81] = {};
    char payload[400] = {};  // serialized AckPayload object
  };

  // ---- protocol output
  void emit_ack(const HostMessage& msg, const char* payload_json);
  void emit_nak(const char* cmd_id, Cmd cmd, Nak code, const char* detail);
  void replay(const CachedReply& reply);
  void remember(const CachedReply& reply);
  const CachedReply* cached(const char* cmd_id) const;
  void emit_state_changed(State from, State to, Trigger trigger);
  void emit_sensor(const char* sensor, bool active);
  void emit_capture_ready();
  void emit_cycle_completed(Destination destination);
  void emit_cycle_aborted(const char* reason);
  void emit_fault();
  void emit_heartbeat();
  void status_json(char* buf, size_t size) const;

  // ---- state machine
  bool transition(Trigger trigger, Fault fault = Fault::NONE, const char* abort_reason = nullptr);
  void enter(State s);
  void actuators_safe();
  void motor(bool on);
  void clear_cycle();

  // ---- commands
  void on_command(const HostMessage& msg);
  void reply_ok(const HostMessage& msg, const char* payload_json = "{}");
  void reply_err(const HostMessage& msg, Nak code, const char* detail = nullptr);

  // ---- periodic
  void read_inputs(uint32_t now);
  void run_phase(uint32_t now);
  uint16_t debounce_ms() const;

  Hal& hal_;
  LineSink& out_;
  const char* firmware_version_;

  char boot_id_[9] = {};
  char session_id_[9] = {};
  bool has_session_ = false;
  uint32_t seq_ = 0;
  uint32_t booted_at_ = 0;
  uint32_t now_ = 0;
  uint32_t last_host_ = 0;
  uint32_t last_heartbeat_ = 0;

  State state_ = State::DISARMED;
  Fault fault_ = Fault::NONE;
  uint32_t phase_started_ = 0;
  uint32_t sort_duration_ = 0;

  bool configured_ = false;
  BenchConfig config_ = {};
  char config_hash_[9] = {};

  int32_t lot_id_ = 0;
  int32_t cycle_id_ = 0;
  bool has_destination_ = false;
  Destination destination_ = Destination::APPROVED;

  bool motor_on_ = false;
  uint8_t servo_deg_ = 0;
  uint32_t test_until_ = 0;
  bool test_active_ = false;

  Debounced s1_, s2_, estop_;
  CachedReply cache_[kCmdCache];
  size_t cache_next_ = 0;
};

}  // namespace av
