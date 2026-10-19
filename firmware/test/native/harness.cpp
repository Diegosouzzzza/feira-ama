// PC harness: the real controller logic on a simulated belt, speaking the serial protocol over
// stdin/stdout. Lines starting with '#' are test controls, never protocol:
//   #estop 1|0   press/release the emergency button
//   #remove      take any piece off the belt
//   #reboot      power-cycle the board (new boot_id)
//   #s1_missing  next piece never reaches S1
// Usage: harness [--dump-transitions] [--belt-mm-s N]
#include <atomic>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <iostream>
#include <mutex>
#include <string>
#include <thread>

#include "av_controller.h"

namespace {

// Belt geometry in millimetres from the entrance.
constexpr double kS1From = 300, kS1To = 340;
constexpr double kS2From = 600, kS2To = 640;
constexpr double kDivertAt = 650, kEnd = 820;

class StdoutSink : public av::LineSink {
 public:
  void write_line(const char* data, size_t len) override {
    std::lock_guard<std::mutex> lock(mutex_);
    std::fwrite(data, 1, len, stdout);
    std::fputc('\n', stdout);
    std::fflush(stdout);
  }

 private:
  std::mutex mutex_;
};

class BeltMotor : public av::MotorDriver {
 public:
  void begin() override {}
  void set(bool on, uint8_t) override { this->on = on; }
  bool supports_pwm() const override { return false; }
  bool on = false;
};

class BeltHal : public av::Hal {
 public:
  bool read_s1() override { return has_piece && pos >= kS1From && pos <= kS1To; }
  bool read_s2() override { return has_piece && pos >= kS2From && pos <= kS2To; }
  bool read_estop() override { return estop; }
  av::MotorDriver& motor() override { return motor_; }
  void set_servo(uint8_t degrees) override { servo = degrees; }
  uint32_t random32() override {
    return static_cast<uint32_t>(std::rand()) << 16 ^ static_cast<uint32_t>(std::rand());
  }

  void advance(double dt_s, double belt_mm_s, uint8_t rest_deg) {
    if (!has_piece || !motor_.on) return;
    double next = pos + belt_mm_s * dt_s;
    if (s1_missing && pos < kS1From && next >= kS1From) {
      has_piece = false;  // fell off before the camera
      s1_missing = false;
      return;
    }
    pos = next;
    bool diverting = servo >= 0 && servo != rest_deg;
    if ((diverting && pos >= kDivertAt) || pos >= kEnd) has_piece = false;
  }

  bool has_piece = false;
  double pos = 0;
  bool estop = false;
  bool s1_missing = false;
  int servo = -1;
  BeltMotor motor_;
};

void dump_transitions() {
  for (int s = 0; s < static_cast<int>(av::State::COUNT); ++s) {
    for (int t = 0; t < static_cast<int>(av::Trigger::COUNT); ++t) {
      av::State next;
      if (av::next_state(static_cast<av::State>(s), static_cast<av::Trigger>(t), &next)) {
        std::printf("%s %s %s\n", av::name(static_cast<av::State>(s)),
                    av::name(static_cast<av::Trigger>(t)), av::name(next));
      }
    }
  }
}

}  // namespace

int main(int argc, char** argv) {
  double belt_mm_s = 200;
  for (int i = 1; i < argc; ++i) {
    if (std::strcmp(argv[i], "--dump-transitions") == 0) {
      dump_transitions();
      return 0;
    }
    if (std::strcmp(argv[i], "--belt-mm-s") == 0 && i + 1 < argc) belt_mm_s = std::atof(argv[++i]);
  }
  std::srand(static_cast<unsigned>(
      std::chrono::steady_clock::now().time_since_epoch().count() & 0x7fffffff));

  std::mutex mutex;
  std::deque<std::string> inbox;
  std::atomic<bool> eof{false};
  std::thread reader([&] {
    std::string line;
    while (std::getline(std::cin, line)) {
      if (!line.empty() && line.back() == '\r') line.pop_back();
      std::lock_guard<std::mutex> lock(mutex);
      inbox.push_back(line);
    }
    eof = true;
  });

  StdoutSink sink;
  BeltHal hal;
  av::Controller controller(hal, sink, "nativo-0.2");
  const auto start = std::chrono::steady_clock::now();
  auto now_ms = [&] {
    return static_cast<uint32_t>(std::chrono::duration_cast<std::chrono::milliseconds>(
                                     std::chrono::steady_clock::now() - start)
                                     .count());
  };
  controller.begin(now_ms());
  uint32_t last = now_ms();

  while (!eof) {
    std::deque<std::string> batch;
    {
      std::lock_guard<std::mutex> lock(mutex);
      batch.swap(inbox);
    }
    for (const std::string& line : batch) {
      if (!line.empty() && line[0] == '#') {
        if (line.rfind("#estop ", 0) == 0) hal.estop = line[7] == '1';
        if (line == "#remove") hal.has_piece = false;
        if (line == "#s1_missing") hal.s1_missing = true;
        if (line == "#reboot") controller.begin(now_ms());
        continue;
      }
      if (line.size() + 1 > av::kMaxLineBytes) {
        controller.handle_line_too_long(now_ms());
      } else {
        controller.handle_line(line.data(), line.size(), now_ms());
      }
    }
    // A new cycle means the operator placed a piece at the entrance.
    if (controller.state() == av::State::TO_S1 && !hal.has_piece) {
      hal.has_piece = true;
      hal.pos = 0;
    }
    uint32_t now = now_ms();
    hal.advance((now - last) / 1000.0, belt_mm_s, controller.servo_rest_deg());
    last = now;
    controller.tick(now);
    std::this_thread::sleep_for(std::chrono::milliseconds(2));
  }
  reader.join();
  return 0;
}
