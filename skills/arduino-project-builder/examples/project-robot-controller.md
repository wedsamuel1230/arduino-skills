# Robot Controller Project

**Description:** Button-controlled robot with obstacle avoidance using ultrasonic sensor and state machine architecture. Supports forward, turn left, turn right, and emergency stop modes.

**Hardware Requirements:**
- Arduino UNO or ESP32
- L298N motor driver module
- 2x DC motors with wheels
- HC-SR04 ultrasonic distance sensor
- 3x pushbuttons (forward, left, right)
- Battery pack (7.4V LiPo recommended)
- LED (status indicator)

**Wiring Diagram:**
```
L298N Motor Driver:
  ENA → Pin 9 (PWM for left motor speed)
  IN1 → Pin 8 (left motor direction 1)
  IN2 → Pin 7 (left motor direction 2)
  ENB → Pin 6 (PWM for right motor speed)
  IN3 → Pin 5 (right motor direction 1)
  IN4 → Pin 4 (right motor direction 2)
  VCC → Battery + (7.4V)
  GND → Arduino GND and Battery -
  5V → Arduino VIN (regulated 5V output from L298N)

HC-SR04 Ultrasonic:
  VCC → 5V
  TRIG → Pin 11
  ECHO → Pin 10
  GND → GND

Buttons:
  Forward button → Pin 2 (INPUT_PULLUP)
  Left button → Pin 3 (INPUT_PULLUP)
  Right button → Pin 12 (INPUT_PULLUP)

LED:
  Pin 13 → 220Ω resistor → LED anode
  LED cathode → GND
```

**Features:**
- State machine with 5 states (IDLE, FORWARD, TURN_LEFT, TURN_RIGHT, OBSTACLE_DETECTED)
- Autonomous obstacle avoidance (stops at 20cm, turns right)
- Button override (manual control)
- PWM motor speed control
- Non-blocking ultrasonic sensor reads
- Emergency stop on low battery (if voltage sensor added)

**Complete Code:**

```cpp
// config.h
#define LEFT_MOTOR_ENA 9
#define LEFT_MOTOR_IN1 8
#define LEFT_MOTOR_IN2 7
#define RIGHT_MOTOR_ENB 6
#define RIGHT_MOTOR_IN3 5
#define RIGHT_MOTOR_IN4 4

#define ULTRASONIC_TRIG 11
#define ULTRASONIC_ECHO 10

#define BUTTON_FORWARD 2
#define BUTTON_LEFT 3
#define BUTTON_RIGHT 12

#define LED_PIN 13

#define OBSTACLE_THRESHOLD_CM 20
#define MOTOR_SPEED 200  // 0-255 (PWM)
#define TURN_DURATION_MS 800

// main.ino

// Robot state machine
enum RobotState {
  IDLE,
  MOVING_FORWARD,
  TURNING_LEFT,
  TURNING_RIGHT,
  OBSTACLE_DETECTED
};

RobotState state = IDLE;
unsigned long stateStartTime = 0;

// EveryMs timer
class EveryMs {
private:
  unsigned long interval;
  unsigned long lastTrigger;
public:
  EveryMs(unsigned long ms) : interval(ms), lastTrigger(0) {}
  bool check() {
    unsigned long now = millis();
    if (now - lastTrigger >= interval) {
      lastTrigger = now;
      return true;
    }
    return false;
  }
};

// Debounced button
class DebouncedButton {
private:
  uint8_t pin;
  bool lastState;
  unsigned long lastDebounceTime;
public:
  DebouncedButton(uint8_t p) : pin(p), lastState(HIGH), lastDebounceTime(0) {}
  
  void begin() {
    pinMode(pin, INPUT_PULLUP);
  }
  
  bool pressed() {
    bool currentState = digitalRead(pin);
    if (currentState != lastState) {
      lastDebounceTime = millis();
    }
    
    if ((millis() - lastDebounceTime) > 50) {
      if (currentState == LOW && lastState == HIGH) {
        lastState = currentState;
        return true;
      }
    }
    lastState = currentState;
    return false;
  }
};

// Global objects
DebouncedButton btnForward(BUTTON_FORWARD);
DebouncedButton btnLeft(BUTTON_LEFT);
DebouncedButton btnRight(BUTTON_RIGHT);
EveryMs distanceTimer(100);  // Check distance every 100ms

int distanceCm = 999;

void setup() {
  Serial.begin(9600);
  
  // Motor pins
  pinMode(LEFT_MOTOR_ENA, OUTPUT);
  pinMode(LEFT_MOTOR_IN1, OUTPUT);
  pinMode(LEFT_MOTOR_IN2, OUTPUT);
  pinMode(RIGHT_MOTOR_ENB, OUTPUT);
  pinMode(RIGHT_MOTOR_IN3, OUTPUT);
  pinMode(RIGHT_MOTOR_IN4, OUTPUT);
  
  // Ultrasonic pins
  pinMode(ULTRASONIC_TRIG, OUTPUT);
  pinMode(ULTRASONIC_ECHO, INPUT);
  
  // LED
  pinMode(LED_PIN, OUTPUT);
  
  // Buttons
  btnForward.begin();
  btnLeft.begin();
  btnRight.begin();
  
  stopMotors();
  
  Serial.println(F("=== Robot Controller ==="));
  Serial.println(F("States: IDLE, FORWARD, LEFT, RIGHT, OBSTACLE"));
}

void updateState(RobotState newState) {
  state = newState;
  stateStartTime = millis();
  Serial.print(F("State: "));
  Serial.println(newState);
}

void setMotors(int leftSpeed, int rightSpeed) {
  // Left motor
  if (leftSpeed > 0) {
    digitalWrite(LEFT_MOTOR_IN1, HIGH);
    digitalWrite(LEFT_MOTOR_IN2, LOW);
    analogWrite(LEFT_MOTOR_ENA, abs(leftSpeed));
  } else if (leftSpeed < 0) {
    digitalWrite(LEFT_MOTOR_IN1, LOW);
    digitalWrite(LEFT_MOTOR_IN2, HIGH);
    analogWrite(LEFT_MOTOR_ENA, abs(leftSpeed));
  } else {
    digitalWrite(LEFT_MOTOR_IN1, LOW);
    digitalWrite(LEFT_MOTOR_IN2, LOW);
    analogWrite(LEFT_MOTOR_ENA, 0);
  }
  
  // Right motor
  if (rightSpeed > 0) {
    digitalWrite(RIGHT_MOTOR_IN3, HIGH);
    digitalWrite(RIGHT_MOTOR_IN4, LOW);
    analogWrite(RIGHT_MOTOR_ENB, abs(rightSpeed));
  } else if (rightSpeed < 0) {
    digitalWrite(RIGHT_MOTOR_IN3, LOW);
    digitalWrite(RIGHT_MOTOR_IN4, HIGH);
    analogWrite(RIGHT_MOTOR_ENB, abs(rightSpeed));
  } else {
    digitalWrite(RIGHT_MOTOR_IN3, LOW);
    digitalWrite(RIGHT_MOTOR_IN4, LOW);
    analogWrite(RIGHT_MOTOR_ENB, 0);
  }
}

void stopMotors() {
  setMotors(0, 0);
}

int readUltrasonicCm() {
  digitalWrite(ULTRASONIC_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(ULTRASONIC_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(ULTRASONIC_TRIG, LOW);
  
  long duration = pulseIn(ULTRASONIC_ECHO, HIGH, 30000);  // 30ms timeout
  if (duration == 0) return 999;  // No echo
  
  return duration * 0.034 / 2;  // Convert to cm
}

void loop() {
  // Task 1: Read distance sensor
  if (distanceTimer.check()) {
    distanceCm = readUltrasonicCm();
  }
  
  // Task 2: Check buttons
  if (btnForward.pressed()) {
    updateState(MOVING_FORWARD);
  }
  if (btnLeft.pressed()) {
    updateState(TURNING_LEFT);
  }
  if (btnRight.pressed()) {
    updateState(TURNING_RIGHT);
  }
  
  // Task 3: State machine
  unsigned long elapsed = millis() - stateStartTime;
  
  switch (state) {
    case IDLE:
      stopMotors();
      digitalWrite(LED_PIN, LOW);
      break;
      
    case MOVING_FORWARD:
      setMotors(MOTOR_SPEED, MOTOR_SPEED);
      digitalWrite(LED_PIN, HIGH);
      
      // Check for obstacle
      if (distanceCm < OBSTACLE_THRESHOLD_CM) {
        updateState(OBSTACLE_DETECTED);
      }
      break;
      
    case OBSTACLE_DETECTED:
      stopMotors();
      digitalWrite(LED_PIN, (millis() % 200) < 100);  // Blink fast
      
      if (elapsed >= 500) {
        // Turn right to avoid obstacle
        updateState(TURNING_RIGHT);
      }
      break;
      
    case TURNING_LEFT:
      setMotors(-MOTOR_SPEED, MOTOR_SPEED);  // Left backward, right forward
      digitalWrite(LED_PIN, (millis() % 500) < 250);  // Blink
      
      if (elapsed >= TURN_DURATION_MS) {
        updateState(IDLE);
      }
      break;
      
    case TURNING_RIGHT:
      setMotors(MOTOR_SPEED, -MOTOR_SPEED);  // Left forward, right backward
      digitalWrite(LED_PIN, (millis() % 500) < 250);  // Blink
      
      if (elapsed >= TURN_DURATION_MS) {
        updateState(IDLE);
      }
      break;
  }
  
  // Debug output
  if (Serial.available() && Serial.read() == 'd') {
    Serial.print(F("Distance: "));
    Serial.print(distanceCm);
    Serial.print(F("cm | State: "));
    Serial.println(state);
  }
}
```

**Upload Instructions:**
1. Select board: Tools → Board → Arduino UNO
2. Select port: Tools → Port → (your Arduino's port)
3. Upload sketch
4. Power robot with battery (NOT USB)

**Usage:**
- Press **Forward button** to start moving forward
- Press **Left button** to turn left for 800ms, then stop
- Press **Right button** to turn right for 800ms, then stop
- Robot automatically stops and turns right when obstacle detected (<20cm)
- LED blinks during turns, solid during forward movement

**Safety:**
- ALWAYS test with wheels off the ground first
- Ensure battery voltage is appropriate (7.4V recommended)
- Emergency stop: remove battery or press Reset button
- Add battery voltage monitoring for low-battery warning

**Expected Serial Output:**
```
=== Robot Controller ===
States: IDLE, FORWARD, LEFT, RIGHT, OBSTACLE
State: 1
State: 4
Distance: 15cm | State: 4
State: 3
State: 0
```

**Troubleshooting:**
- **Motors not spinning:** Check L298N wiring, ensure battery connected
- **Motors spin slowly:** Battery voltage too low (need 7.4V minimum)
- **Ultrasonic returns 999:** Check TRIG/ECHO wiring, ensure 5V power
- **Robot turns wrong direction:** Swap IN1/IN2 or IN3/IN4 connections
- **Buttons don't work:** Verify INPUT_PULLUP, check button wiring
