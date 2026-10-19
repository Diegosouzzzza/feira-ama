// Bloco 1: valida compilação, gravação e serial. O protocolo real entra no Bloco 6.
#include <Arduino.h>

#ifndef LED_BUILTIN
#define LED_BUILTIN 2
#endif

static constexpr uint32_t kBlinkIntervalMs = 500;
static constexpr size_t kMaxLineLength = 1024;  // docs/protocolo-serial.md

static uint32_t lastBlinkMs = 0;
static bool ledOn = false;
static char lineBuffer[kMaxLineLength];
static size_t lineLength = 0;
static bool lineOverflow = false;

static void sendHello() {
  Serial.printf("{\"type\":\"hello\",\"fw\":\"%s\"}\n", AV_FIRMWARE_VERSION);
}

static void handleLine(const char* line) {
  if (strcmp(line, "ping") == 0) {
    Serial.println("{\"type\":\"pong\"}");
    return;
  }
  Serial.printf("{\"type\":\"echo\",\"len\":%u}\n", static_cast<unsigned>(strlen(line)));
}

static void pollSerial() {
  while (Serial.available() > 0) {
    const char c = static_cast<char>(Serial.read());
    if (c == '\r') continue;
    if (c == '\n') {
      if (lineOverflow) {
        Serial.println("{\"type\":\"error\",\"code\":\"LINE_TOO_LONG\"}");
      } else {
        lineBuffer[lineLength] = '\0';
        handleLine(lineBuffer);
      }
      lineLength = 0;
      lineOverflow = false;
      continue;
    }
    if (lineLength < kMaxLineLength - 1) {
      lineBuffer[lineLength++] = c;
    } else {
      lineOverflow = true;
    }
  }
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(AV_SERIAL_BAUD);
  sendHello();
}

void loop() {
  const uint32_t now = millis();
  if (now - lastBlinkMs >= kBlinkIntervalMs) {
    lastBlinkMs = now;
    ledOn = !ledOn;
    digitalWrite(LED_BUILTIN, ledOn ? HIGH : LOW);
  }
  pollSerial();
}
