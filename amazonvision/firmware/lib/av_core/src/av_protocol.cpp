#include "av_protocol.h"

#include <ArduinoJson.h>
#include <stdio.h>
#include <string.h>

namespace av {

namespace {

const char* const kCmdNames[] = {
    "HELLO",          "CONFIGURE",         "ARM",          "STOP",      "START_CYCLE",
    "DECISION",       "HOLD_FOR_REVIEW",   "CLEAR_FAULT",  "ENTER_MAINTENANCE",
    "EXIT_MAINTENANCE", "GET_STATUS",      "TEST_MOTOR",   "TEST_SERVO",
};

void fail(ParseError* error, Nak code, const char* detail) {
  error->code = code;
  snprintf(error->detail, sizeof(error->detail), "%s", detail);
}

bool only_keys(JsonObjectConst obj, const char* const* allowed, size_t count, const char** bad) {
  for (JsonPairConst kv : obj) {
    bool ok = false;
    for (size_t i = 0; i < count; ++i) {
      if (strcmp(kv.key().c_str(), allowed[i]) == 0) {
        ok = true;
        break;
      }
    }
    if (!ok) {
      *bad = kv.key().c_str();
      return false;
    }
  }
  return true;
}

bool hex8(JsonVariantConst v, char* out) {
  if (!v.is<const char*>()) return false;
  const char* s = v.as<const char*>();
  if (strlen(s) != 8) return false;
  for (size_t i = 0; i < 8; ++i) {
    char c = s[i];
    if (!((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f'))) return false;
  }
  memcpy(out, s, 9);
  return true;
}

bool cmd_id(JsonVariantConst v, char* out) {
  if (!v.is<const char*>()) return false;
  const char* s = v.as<const char*>();
  size_t n = strlen(s);
  if (n < 1 || n > 24) return false;
  for (size_t i = 0; i < n; ++i) {
    char c = s[i];
    bool ok = (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') ||
              c == '_' || c == '-';
    if (!ok) return false;
  }
  memcpy(out, s, n + 1);
  return true;
}

bool int_in(JsonVariantConst v, long long lo, long long hi, long long* out) {
  if (!v.is<long long>()) return false;
  long long x = v.as<long long>();
  if (x < lo || x > hi) return false;
  *out = x;
  return true;
}

// Reads a required bounded integer field; on failure fills the error with the field name.
bool field(JsonObjectConst obj, const char* key, long long lo, long long hi, long long* out,
           ParseError* error) {
  if (obj[key].isNull() || !int_in(obj[key], lo, hi, out)) {
    char detail[81];
    snprintf(detail, sizeof(detail), "%s fora da faixa ou ausente", key);
    fail(error, Nak::INVALID_PAYLOAD, detail);
    return false;
  }
  return true;
}

bool empty_payload(JsonObjectConst root, ParseError* error) {
  JsonVariantConst p = root["payload"];
  if (p.isNull()) return true;
  if (!p.is<JsonObjectConst>() || p.as<JsonObjectConst>().size() != 0) {
    fail(error, Nak::INVALID_PAYLOAD, "payload deve ser vazio");
    return false;
  }
  return true;
}

bool parse_config(JsonVariantConst v, BenchConfig* c, ParseError* error) {
  if (!v.is<JsonObjectConst>()) {
    fail(error, Nak::INVALID_PAYLOAD, "payload ausente");
    return false;
  }
  JsonObjectConst p = v.as<JsonObjectConst>();
  static const char* const kKeys[] = {
      "sensor_debounce_ms", "s1_timeout_ms",  "settle_ms",       "decision_timeout_ms",
      "s2_timeout_ms",      "servo_rest_deg", "servo_reject_deg", "reject_hold_ms",
      "reject_motor_ms",    "release_ms",     "release_max_ms",  "link_timeout_ms",
      "motor_power_pct",
  };
  const char* bad = nullptr;
  if (!only_keys(p, kKeys, sizeof(kKeys) / sizeof(kKeys[0]), &bad)) {
    fail(error, Nak::INVALID_PAYLOAD, "campo extra no payload");
    return false;
  }
  long long x = 0;
  if (!field(p, "sensor_debounce_ms", 1, 200, &x, error)) return false;
  c->sensor_debounce_ms = static_cast<uint16_t>(x);
  if (!field(p, "s1_timeout_ms", 500, 30000, &x, error)) return false;
  c->s1_timeout_ms = static_cast<uint16_t>(x);
  if (!field(p, "settle_ms", 0, 5000, &x, error)) return false;
  c->settle_ms = static_cast<uint16_t>(x);
  if (!field(p, "decision_timeout_ms", 500, 30000, &x, error)) return false;
  c->decision_timeout_ms = static_cast<uint16_t>(x);
  if (!field(p, "s2_timeout_ms", 500, 30000, &x, error)) return false;
  c->s2_timeout_ms = static_cast<uint16_t>(x);
  if (!field(p, "servo_rest_deg", 0, 180, &x, error)) return false;
  c->servo_rest_deg = static_cast<uint8_t>(x);
  if (!field(p, "servo_reject_deg", 0, 180, &x, error)) return false;
  c->servo_reject_deg = static_cast<uint8_t>(x);
  if (!field(p, "reject_hold_ms", 100, 5000, &x, error)) return false;
  c->reject_hold_ms = static_cast<uint16_t>(x);
  if (!field(p, "reject_motor_ms", 0, 10000, &x, error)) return false;
  c->reject_motor_ms = static_cast<uint16_t>(x);
  if (!field(p, "release_ms", 0, 10000, &x, error)) return false;
  c->release_ms = static_cast<uint16_t>(x);
  if (!field(p, "release_max_ms", 500, 30000, &x, error)) return false;
  c->release_max_ms = static_cast<uint16_t>(x);
  if (!field(p, "link_timeout_ms", 500, 10000, &x, error)) return false;
  c->link_timeout_ms = static_cast<uint16_t>(x);
  c->motor_power_pct = 0;
  if (!p["motor_power_pct"].isNull()) {
    if (!field(p, "motor_power_pct", 1, 100, &x, error)) return false;
    c->motor_power_pct = static_cast<uint8_t>(x);
  }
  if (c->servo_rest_deg == c->servo_reject_deg) {
    fail(error, Nak::INVALID_PAYLOAD, "servo_reject_deg igual a servo_rest_deg");
    return false;
  }
  if (c->release_max_ms < c->release_ms) {
    fail(error, Nak::INVALID_PAYLOAD, "release_max_ms menor que release_ms");
    return false;
  }
  return true;
}

}  // namespace

const char* name(Cmd c) {
  size_t i = static_cast<size_t>(c);
  return i < sizeof(kCmdNames) / sizeof(kCmdNames[0]) ? kCmdNames[i] : "?";
}

const char* name(Nak n) {
  switch (n) {
    case Nak::BAD_JSON: return "BAD_JSON";
    case Nak::LINE_TOO_LONG: return "LINE_TOO_LONG";
    case Nak::UNSUPPORTED_VERSION: return "UNSUPPORTED_VERSION";
    case Nak::UNKNOWN_COMMAND: return "UNKNOWN_COMMAND";
    case Nak::INVALID_PAYLOAD: return "INVALID_PAYLOAD";
    case Nak::NO_SESSION: return "NO_SESSION";
    case Nak::SESSION_MISMATCH: return "SESSION_MISMATCH";
    case Nak::INVALID_STATE: return "INVALID_STATE";
    case Nak::CYCLE_MISMATCH: return "CYCLE_MISMATCH";
    case Nak::NOT_CONFIGURED: return "NOT_CONFIGURED";
    case Nak::PRECONDITION_FAILED: return "PRECONDITION_FAILED";
  }
  return "?";
}

const char* name(Destination d) { return d == Destination::APPROVED ? "APPROVED" : "REJECTED"; }

bool parse_host_line(const char* line, size_t len, HostMessage* out, ParseError* error) {
  memset(out, 0, sizeof(*out));
  if (len + 1 > kMaxLineBytes) {
    fail(error, Nak::LINE_TOO_LONG, "linha longa demais");
    return false;
  }
  JsonDocument doc;
  if (deserializeJson(doc, line, len) != DeserializationError::Ok) {
    fail(error, Nak::BAD_JSON, "JSON invalido");
    return false;
  }
  if (!doc.is<JsonObjectConst>()) {
    fail(error, Nak::BAD_JSON, "esperado objeto JSON");
    return false;
  }
  JsonObjectConst root = doc.as<JsonObjectConst>();
  JsonVariantConst version = root["protocol_version"];
  if (!version.is<long long>() || version.as<long long>() != kProtocolVersion) {
    fail(error, Nak::UNSUPPORTED_VERSION, "versao de protocolo nao suportada");
    return false;
  }

  const char* type = root["type"].is<const char*>() ? root["type"].as<const char*>() : "";
  if (strcmp(type, "hb") == 0) {
    static const char* const kKeys[] = {"protocol_version", "type", "session_id"};
    const char* bad = nullptr;
    if (!only_keys(root, kKeys, 3, &bad) || !hex8(root["session_id"], out->session_id)) {
      fail(error, Nak::INVALID_PAYLOAD, "heartbeat invalido");
      return false;
    }
    out->heartbeat = true;
    return true;
  }
  if (strcmp(type, "cmd") != 0) {
    fail(error, Nak::INVALID_PAYLOAD, "type invalido");
    return false;
  }

  const char* cmd_name = root["name"].is<const char*>() ? root["name"].as<const char*>() : "";
  bool known = false;
  for (size_t i = 0; i < static_cast<size_t>(Cmd::COUNT); ++i) {
    if (strcmp(cmd_name, kCmdNames[i]) == 0) {
      out->cmd = static_cast<Cmd>(i);
      known = true;
      break;
    }
  }
  if (!known) {
    fail(error, Nak::UNKNOWN_COMMAND, "comando desconhecido");
    return false;
  }

  const bool needs_lot = out->cmd == Cmd::START_CYCLE;
  const bool needs_cycle = out->cmd == Cmd::START_CYCLE || out->cmd == Cmd::DECISION ||
                           out->cmd == Cmd::HOLD_FOR_REVIEW;
  const char* keys[8] = {"protocol_version", "type", "session_id", "cmd_id", "name", "payload"};
  size_t key_count = 6;
  if (needs_lot) keys[key_count++] = "lot_id";
  if (needs_cycle) keys[key_count++] = "cycle_id";
  const char* bad = nullptr;
  if (!only_keys(root, keys, key_count, &bad)) {
    fail(error, Nak::INVALID_PAYLOAD, "campo extra no comando");
    return false;
  }
  if (!hex8(root["session_id"], out->session_id)) {
    fail(error, Nak::INVALID_PAYLOAD, "session_id invalido");
    return false;
  }
  if (!cmd_id(root["cmd_id"], out->cmd_id)) {
    fail(error, Nak::INVALID_PAYLOAD, "cmd_id invalido");
    return false;
  }
  long long x = 0;
  if (needs_lot) {
    if (!field(root, "lot_id", 1, 2147483647LL, &x, error)) return false;
    out->lot_id = static_cast<int32_t>(x);
  }
  if (needs_cycle) {
    if (!field(root, "cycle_id", 1, 2147483647LL, &x, error)) return false;
    out->cycle_id = static_cast<int32_t>(x);
  }

  JsonVariantConst payload = root["payload"];
  switch (out->cmd) {
    case Cmd::CONFIGURE:
      return parse_config(payload, &out->config, error);
    case Cmd::DECISION: {
      static const char* const kKeys[] = {"destination"};
      if (!payload.is<JsonObjectConst>() ||
          !only_keys(payload.as<JsonObjectConst>(), kKeys, 1, &bad) ||
          !payload["destination"].is<const char*>()) {
        fail(error, Nak::INVALID_PAYLOAD, "destination ausente");
        return false;
      }
      const char* d = payload["destination"].as<const char*>();
      if (strcmp(d, "APPROVED") == 0) {
        out->destination = Destination::APPROVED;
      } else if (strcmp(d, "REJECTED") == 0) {
        out->destination = Destination::REJECTED;
      } else {
        fail(error, Nak::INVALID_PAYLOAD, "destination invalido");
        return false;
      }
      return true;
    }
    case Cmd::TEST_MOTOR: {
      static const char* const kKeys[] = {"run_ms"};
      if (!payload.is<JsonObjectConst>() ||
          !only_keys(payload.as<JsonObjectConst>(), kKeys, 1, &bad)) {
        fail(error, Nak::INVALID_PAYLOAD, "payload invalido");
        return false;
      }
      if (!field(payload.as<JsonObjectConst>(), "run_ms", 1, 5000, &x, error)) return false;
      out->run_ms = static_cast<uint16_t>(x);
      return true;
    }
    case Cmd::TEST_SERVO: {
      static const char* const kKeys[] = {"angle_deg", "hold_ms"};
      if (!payload.is<JsonObjectConst>() ||
          !only_keys(payload.as<JsonObjectConst>(), kKeys, 2, &bad)) {
        fail(error, Nak::INVALID_PAYLOAD, "payload invalido");
        return false;
      }
      JsonObjectConst p = payload.as<JsonObjectConst>();
      if (!field(p, "angle_deg", 0, 180, &x, error)) return false;
      out->angle_deg = static_cast<uint8_t>(x);
      if (!field(p, "hold_ms", 0, 5000, &x, error)) return false;
      out->hold_ms = static_cast<uint16_t>(x);
      return true;
    }
    default:
      return empty_payload(root, error);
  }
}

}  // namespace av
