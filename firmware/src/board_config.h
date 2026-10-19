// Bench wiring. PROVISIONAL until the bench is assembled: confirm every pin against the real
// wiring and record the final values in docs/firmware.md. Override with -D flags if needed.
#pragma once

// Inputs: PC817 opto outputs pull the pin LOW when the 12 V sensor is active.
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

// Emergency button auxiliary contact (the button itself cuts actuator power in hardware).
// Active LOW with pull-up: an unwired pin reads "released"; the hardware cut is what protects.
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

// Conveyor motor driver, chosen when the belt is bought (docs/pendencias.md #2):
//   1 = on/off output (logic-level MOSFET or relay module), active HIGH
//   2 = BTS7960 (IBT-2) H-bridge, forward only, PWM on RPWM
#ifndef AV_MOTOR_DRIVER
#define AV_MOTOR_DRIVER 1
#endif
#define AV_PIN_MOTOR_EN 19   // driver 1
#define AV_PIN_BTS_RPWM 21   // driver 2
#define AV_PIN_BTS_LPWM 22   // driver 2 (held low: no reverse)
#define AV_PIN_BTS_EN 23     // driver 2: R_EN and L_EN tied together
#define AV_MOTOR_LEDC_CHANNEL 1
#define AV_MOTOR_PWM_HZ 20000

// Status LED: on = ready/cycle, slow blink = disarmed, fast blink = fault or emergency.
#ifndef AV_PIN_LED
#define AV_PIN_LED 2
#endif
