// Native unit tests of the controller logic with a hand-driven clock and scripted sensors.
#include <cstdio>
#include <functional>
#include <string>
#include <vector>

#include "av_controller.h"
#include "fakes.h"

namespace {

struct Test {
  const char* name;
  std::function<void()> fn;
};
std::vector<Test>& registry() {
  static std::vector<Test> tests;
  return tests;
}
int failures = 0;
const char* current = "";

struct Register {
  Register(const char* name, std::function<void()> fn) { registry().push_back({name, std::move(fn)}); }
};

#define TEST(name)                               \
  void name();                                   \
  const Register register_##name(#name, name);   \
  void name()

#define CHECK(cond)                                                                 \
  do {                                                                              \
    if (!(cond)) {                                                                  \
      std::printf("  FALHOU %s (%s:%d): %s\n", current, __FILE__, __LINE__, #cond); \
      ++failures;                                                                   \
    }                                                                               \
  } while (0)

const char* kConfig =
    R"({"sensor_debounce_ms":20,"s1_timeout_ms":3000,"settle_ms":100,"decision_timeout_ms":1000,)"
    R"("s2_timeout_ms":3000,"servo_rest_deg":10,"servo_reject_deg":75,"reject_hold_ms":200,)"
    R"("reject_motor_ms":0,"release_ms":300,"release_max_ms":2000,"link_timeout_ms":2000})";

struct Rig {
  avtest::FakeHal hal;
  avtest::CaptureSink out;
  av::Controller c{hal, out, "teste"};
  uint32_t now = 1000;
  int n = 0;

  Rig() { c.begin(now); }

  void send(const std::string& line) { c.handle_line(line.data(), line.size(), now); }

  void cmd(const char* name, const std::string& extra = "", const char* cmd_id = nullptr) {
    char id[16];
    std::snprintf(id, sizeof(id), "c%d", ++n);
    send(std::string(R"({"protocol_version":1,"type":"cmd","session_id":"5e1a9c03","cmd_id":")") +
         (cmd_id ? cmd_id : id) + R"(","name":")" + name + "\"" + extra + "}");
  }

  void advance(uint32_t ms) {
    for (uint32_t t = 0; t < ms; t += 5) {
      now += 5;
      c.tick(now);
    }
  }

  void ready() {
    cmd("HELLO");
    cmd("CONFIGURE", std::string(R"(,"payload":)") + kConfig);
    cmd("ARM");
  }

  int count(const std::string& needle) const {
    int k = 0;
    for (const auto& l : out.lines) k += l.find(needle) != std::string::npos;
    return k;
  }
  bool saw(const std::string& needle) const { return count(needle) > 0; }
  const std::string& last() const { return out.lines.back(); }
};

TEST(boots_disarmed_without_motion) {
  Rig r;
  CHECK(r.c.state() == av::State::DISARMED);
  CHECK(!r.hal.motor_.on);
  r.advance(10);
  CHECK(r.saw(R"("type":"hb")"));
  CHECK(!r.saw("session_id"));
}

TEST(estop_pressed_at_boot_starts_in_estop) {
  avtest::FakeHal hal;
  hal.estop = true;
  avtest::CaptureSink out;
  av::Controller c(hal, out, "t");
  c.begin(0);
  CHECK(c.state() == av::State::ESTOP);
}

TEST(commands_require_session) {
  Rig r;
  r.cmd("ARM");
  CHECK(r.saw(R"("code":"NO_SESSION")"));
}

TEST(arm_requires_configuration) {
  Rig r;
  r.cmd("HELLO");
  r.cmd("ARM");
  CHECK(r.saw(R"("code":"NOT_CONFIGURED")"));
}

TEST(full_rejected_cycle) {
  Rig r;
  r.ready();
  CHECK(r.c.state() == av::State::READY);
  r.cmd("START_CYCLE", R"(,"lot_id":3,"cycle_id":41)");
  CHECK(r.c.state() == av::State::TO_S1);
  CHECK(r.hal.motor_.on);

  r.hal.s1 = true;
  r.advance(30);
  CHECK(r.c.state() == av::State::SETTLING);
  CHECK(!r.hal.motor_.on);
  r.advance(120);
  CHECK(r.c.state() == av::State::INSPECTING);
  CHECK(r.saw(R"("name":"CAPTURE_READY","cycle_id":41)"));

  r.cmd("DECISION", R"(,"cycle_id":41,"payload":{"destination":"REJECTED"})");
  CHECK(r.c.state() == av::State::TO_S2);
  CHECK(r.hal.motor_.on);
  r.hal.s1 = false;
  r.hal.s2 = true;
  r.advance(30);
  CHECK(r.c.state() == av::State::SORTING);
  CHECK(r.hal.servo == 75);
  r.advance(210);
  CHECK(r.c.state() == av::State::RELEASING);
  CHECK(r.hal.servo == 10);
  CHECK(r.hal.motor_.on);
  r.hal.s2 = false;
  r.advance(330);
  CHECK(r.c.state() == av::State::READY);
  CHECK(!r.hal.motor_.on);
  CHECK(r.saw(R"("name":"CYCLE_COMPLETED","cycle_id":41,"payload":{"destination":"REJECTED"})"));
}

TEST(approved_piece_skips_the_paddle) {
  Rig r;
  r.ready();
  r.cmd("START_CYCLE", R"(,"lot_id":3,"cycle_id":42)");
  r.hal.s1 = true;
  r.advance(150);
  r.cmd("DECISION", R"(,"cycle_id":42,"payload":{"destination":"APPROVED"})");
  r.hal.s1 = false;
  r.hal.s2 = true;
  r.advance(30);
  CHECK(r.c.state() == av::State::RELEASING);
  CHECK(r.hal.servo == 10);
}

TEST(missing_s1_faults_and_aborts) {
  Rig r;
  r.ready();
  r.cmd("START_CYCLE", R"(,"lot_id":3,"cycle_id":43)");
  for (int i = 0; i < 4; ++i) {
    r.advance(800);
    r.send(R"({"protocol_version":1,"type":"hb","session_id":"5e1a9c03"})");
  }
  CHECK(r.c.state() == av::State::FAULT);
  CHECK(r.c.fault() == av::Fault::S1_TIMEOUT);
  CHECK(r.saw(R"("reason":"S1_TIMEOUT")"));
  CHECK(!r.hal.motor_.on);
}

TEST(short_pulse_is_filtered_by_debounce) {
  Rig r;
  r.ready();
  r.cmd("START_CYCLE", R"(,"lot_id":3,"cycle_id":44)");
  r.hal.s1 = true;
  r.advance(10);
  r.hal.s1 = false;
  r.advance(50);
  CHECK(r.c.state() == av::State::TO_S1);
  CHECK(!r.saw("SENSOR_CHANGED"));
}

TEST(repeated_cmd_id_replays_without_executing) {
  Rig r;
  r.ready();
  r.cmd("START_CYCLE", R"(,"lot_id":3,"cycle_id":45)", "same");
  r.cmd("START_CYCLE", R"(,"lot_id":3,"cycle_id":45)", "same");
  CHECK(r.count(R"("trigger":"START_CYCLE")") == 1);
  CHECK(r.saw(R"("duplicate":true)"));
}

TEST(decision_must_match_cycle) {
  Rig r;
  r.ready();
  r.cmd("START_CYCLE", R"(,"lot_id":3,"cycle_id":46)");
  r.hal.s1 = true;
  r.advance(150);
  r.cmd("DECISION", R"(,"cycle_id":99,"payload":{"destination":"APPROVED"})");
  CHECK(r.saw(R"("code":"CYCLE_MISMATCH")"));
  CHECK(r.c.state() == av::State::INSPECTING);
}

TEST(silent_host_during_cycle_faults_with_link_lost) {
  Rig r;
  r.ready();
  r.cmd("START_CYCLE", R"(,"lot_id":3,"cycle_id":47)");
  r.hal.s1 = true;
  r.advance(150);
  r.cmd("HOLD_FOR_REVIEW", R"(,"cycle_id":47)");
  r.advance(2100);
  CHECK(r.c.state() == av::State::FAULT);
  CHECK(r.c.fault() == av::Fault::LINK_LOST);
  CHECK(r.saw(R"("reason":"LINK_LOST")"));
}

TEST(estop_aborts_then_release_disarms_without_motion) {
  Rig r;
  r.ready();
  r.cmd("START_CYCLE", R"(,"lot_id":3,"cycle_id":48)");
  r.hal.estop = true;
  r.advance(30);
  CHECK(r.c.state() == av::State::ESTOP);
  CHECK(!r.hal.motor_.on);
  CHECK(r.saw(R"("reason":"ESTOP")"));
  r.hal.estop = false;
  r.advance(30);
  CHECK(r.c.state() == av::State::DISARMED);
  CHECK(!r.hal.motor_.on);
}

TEST(clear_fault_refused_while_sensor_occupied) {
  Rig r;
  r.ready();
  r.cmd("START_CYCLE", R"(,"lot_id":3,"cycle_id":49)");
  r.hal.s1 = true;
  r.advance(150);
  r.advance(1100);  // decision deadline
  CHECK(r.c.state() == av::State::FAULT);
  r.cmd("CLEAR_FAULT");
  CHECK(r.saw(R"("code":"PRECONDITION_FAILED")"));
  r.hal.s1 = false;
  r.advance(30);
  r.cmd("CLEAR_FAULT");
  CHECK(r.c.state() == av::State::DISARMED);
}

TEST(hello_in_fault_keeps_original_fault) {
  Rig r;
  r.ready();
  r.cmd("START_CYCLE", R"(,"lot_id":3,"cycle_id":50)");
  r.hal.s1 = true;
  r.advance(1300);
  CHECK(r.c.fault() == av::Fault::DECISION_TIMEOUT);
  r.cmd("HELLO");
  CHECK(r.c.fault() == av::Fault::DECISION_TIMEOUT);
}

TEST(line_too_long_is_reported) {
  Rig r;
  r.c.handle_line_too_long(r.now);
  CHECK(r.saw(R"("code":"LINE_TOO_LONG")"));
}

TEST(transition_table_rejects_unknown_pairs) {
  av::State next;
  CHECK(!av::next_state(av::State::READY, av::Trigger::DECISION, &next));
  CHECK(av::next_state(av::State::REVIEW_HOLD, av::Trigger::DECISION, &next) &&
        next == av::State::TO_S2);
  CHECK(!av::next_state(av::State::REVIEW_HOLD, av::Trigger::TIMEOUT, &next));
  CHECK(!av::next_state(av::State::ESTOP, av::Trigger::ESTOP_PRESSED, &next));
}

}  // namespace

int main() {
  for (const Test& t : registry()) {
    current = t.name;
    int before = failures;
    t.fn();
    std::printf("%s %s\n", failures == before ? "ok  " : "ERRO", t.name);
  }
  std::printf("%zu testes, %d falha(s)\n", registry().size(), failures);
  return failures == 0 ? 0 : 1;
}
