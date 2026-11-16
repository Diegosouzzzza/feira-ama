// Bench wiring. PROVISIONAL until the bench is assembled: confirm every pin against the real
// wiring and record the final values in docs/firmware.md. Override with -D flags if needed.
#pragma once

// Inputs: Optical IR NPN sensors (E18-D80NK 5V) with 1k + BAT54S 3.3V Schottky clamp.
// Pull the pin LOW when an apple is detected.
// Avoid strapping pins (0, 2, 12, 15) and input-only pins 34-39 (no internal pull-up).
#ifndef AV_PIN_S1
#define AV_PIN_S1 25
#endif
#ifndef AV_PIN_S2
#define AV_PIN_S2 26
#endif
#ifndef AV_INPUTS_ACTIVE_LOW
#define AV_INPUTS_ACTIVE_LOW 1
#endif

// Emergency button auxiliary NC contact (E12 NF 11-12 tied to GND; E12-B 21-22 cuts K1 coil in hardware).
// Normal (NC closed to GND) = LOW (0V); Emergency pressed or wire broken (NC open) = HIGH (3.3V via pull-up).
#ifndef AV_PIN_ESTOP
#define AV_PIN_ESTOP 27
#endif

// Diverter servo (MG996R): 50 Hz, pulse 500-2500 us mapped to 0-180 degrees.
#ifndef AV_PIN_SERVO
#define AV_PIN_SERVO 18
#endif
#define AV_SERVO_LEDC_CHANNEL 0
#define AV_SERVO_MIN_US 500
#define AV_SERVO_MAX_US 2500

// Conveyor motor driver (D4184 MOSFET module on GPIO19, active HIGH with 10k internal pull-down):
//   0 = plain on/off output (relay module), active HIGH, no speed control
//   1 = PWM output (logic-level MOSFET D4184), active HIGH, 20 kHz, speed by motor_power_pct
//   2 = BTS7960 (IBT-2) H-bridge, forward only, PWM on RPWM
#ifndef AV_MOTOR_DRIVER
#define AV_MOTOR_DRIVER 1
#endif
#define AV_PIN_MOTOR_EN 19   // driver 1 (D4184 MOSFET SIG/GATE on GPIO19)
#define AV_PIN_BTS_RPWM 21   // driver 2
#define AV_PIN_BTS_LPWM 22   // driver 2 (held low: no reverse)
#define AV_PIN_BTS_EN 23     // driver 2: R_EN and L_EN tied together
// LEDC channels share a timer in pairs (0-1, 2-3, ...). The servo owns channel 0 at 50 Hz, so
// the motor must NOT use channel 1: setting 20 kHz there would retune the servo's timer.
#ifndef AV_MOTOR_LEDC_CHANNEL
#define AV_MOTOR_LEDC_CHANNEL 2
#endif
// 20 kHz is above hearing. If the D4184 module has an optocoupler input (PC817) and the speed
// stops following motor_power_pct, lower this (e.g. -DAV_MOTOR_PWM_HZ=2000).
#ifndef AV_MOTOR_PWM_HZ
#define AV_MOTOR_PWM_HZ 20000
#endif
#define AV_MOTOR_PWM_BITS 8
#if (AV_MOTOR_LEDC_CHANNEL / 2) == (AV_SERVO_LEDC_CHANNEL / 2)
#error "AV_MOTOR_LEDC_CHANNEL shares its LEDC timer with the servo: pick channel 2 or above"
#endif

// Safety Relay K1 (E08 via Q2 BC337-40 low-side driver + 10k pull-down) and Buzzer (E25 via Q1 BC337-40):
#ifndef AV_PIN_RELAY_K1
#define AV_PIN_RELAY_K1 4
#endif
#ifndef AV_PIN_BUZZER
#define AV_PIN_BUZZER 13
#endif

// Panel 22mm LED indicators (H05-R, H05-G, H05-Y via 330 ohm resistors) and onboard status LED:
#ifndef AV_PIN_LED_R
#define AV_PIN_LED_R 17
#endif
#ifndef AV_PIN_LED_G
#define AV_PIN_LED_G 16
#endif
#ifndef AV_PIN_LED_Y
#define AV_PIN_LED_Y 5
#endif
#ifndef AV_PIN_LED
#define AV_PIN_LED 2
#endif
