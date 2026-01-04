# State Machine Patterns

## Enum-Based FSM (Recommended)

```cpp
enum TrafficLightState {
  RED,
  RED_YELLOW,
  GREEN,
  YELLOW
};

TrafficLightState currentState = RED;
unsigned long stateStartTime = 0;

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  stateStartTime = millis();
}

void loop() {
  unsigned long elapsed = millis() - stateStartTime;
  
  switch (currentState) {
    case RED:
      digitalWrite(RED_PIN, HIGH);
      digitalWrite(YELLOW_PIN, LOW);
      digitalWrite(GREEN_PIN, LOW);
      
      if (elapsed >= 5000) {
        currentState = RED_YELLOW;
        stateStartTime = millis();
      }
      break;
      
    case RED_YELLOW:
      digitalWrite(RED_PIN, HIGH);
      digitalWrite(YELLOW_PIN, HIGH);
      digitalWrite(GREEN_PIN, LOW);
      
      if (elapsed >= 2000) {
        currentState = GREEN;
        stateStartTime = millis();
      }
      break;
      
    case GREEN:
      digitalWrite(RED_PIN, LOW);
      digitalWrite(YELLOW_PIN, LOW);
      digitalWrite(GREEN_PIN, HIGH);
      
      if (elapsed >= 5000) {
        currentState = YELLOW;
        stateStartTime = millis();
      }
      break;
      
    case YELLOW:
      digitalWrite(RED_PIN, LOW);
      digitalWrite(YELLOW_PIN, HIGH);
      digitalWrite(GREEN_PIN, LOW);
      
      if (elapsed >= 2000) {
        currentState = RED;
        stateStartTime = millis();
      }
      break;
  }
}
```

## Robot Controller FSM

```cpp
enum RobotState {
  IDLE,
  MOVING_FORWARD,
  TURNING_LEFT,
  TURNING_RIGHT,
  OBSTACLE_DETECTED,
  EMERGENCY_STOP
};

RobotState state = IDLE;
unsigned long stateStartTime = 0;

struct RobotContext {
  int distanceSensor;
  bool buttonPressed;
  int batteryLevel;
} context;

void updateState(RobotState newState) {
  state = newState;
  stateStartTime = millis();
  Serial.print(F("State changed to: "));
  Serial.println(newState);
}

void loop() {
  // Update sensor context
  context.distanceSensor = analogRead(A0);
  context.buttonPressed = digitalRead(BUTTON_PIN) == LOW;
  context.batteryLevel = analogRead(BATTERY_PIN);
  
  unsigned long elapsed = millis() - stateStartTime;
  
  // Emergency stop has highest priority
  if (context.batteryLevel < 500) {
    if (state != EMERGENCY_STOP) {
      updateState(EMERGENCY_STOP);
    }
  }
  
  switch (state) {
    case IDLE:
      stopMotors();
      
      if (context.buttonPressed) {
        updateState(MOVING_FORWARD);
      }
      break;
      
    case MOVING_FORWARD:
      setMotors(255, 255);
      
      if (context.distanceSensor < 200) {
        updateState(OBSTACLE_DETECTED);
      } else if (context.buttonPressed) {
        updateState(IDLE);
      }
      break;
      
    case OBSTACLE_DETECTED:
      stopMotors();
      
      if (elapsed >= 500) {
        // Decide turn direction based on obstacle position
        updateState(TURNING_RIGHT);
      }
      break;
      
    case TURNING_RIGHT:
      setMotors(255, -255);
      
      if (elapsed >= 1000) {
        updateState(MOVING_FORWARD);
      }
      break;
      
    case EMERGENCY_STOP:
      stopMotors();
      digitalWrite(LED_PIN, (millis() % 500) < 250); // Blink LED
      
      if (context.batteryLevel > 550) {
        updateState(IDLE);
      }
      break;
  }
}

void setMotors(int left, int right) {
  // Motor driver code here
}

void stopMotors() {
  setMotors(0, 0);
}
```

## Button-Triggered FSM

```cpp
enum SystemMode {
  OFF,
  HEATING,
  COOLING,
  AUTO
};

SystemMode mode = OFF;
DebouncedButton modeButton(2);

void setup() {
  Serial.begin(115200);
  pinMode(HEATER_PIN, OUTPUT);
  pinMode(COOLER_PIN, OUTPUT);
}

void loop() {
  modeButton.update();
  
  // Button cycles through modes
  if (modeButton.pressed()) {
    switch (mode) {
      case OFF:      mode = HEATING; break;
      case HEATING:  mode = COOLING; break;
      case COOLING:  mode = AUTO;    break;
      case AUTO:     mode = OFF;     break;
    }
    Serial.print(F("Mode: "));
    Serial.println(mode);
  }
  
  // Execute mode behavior
  float temperature = readTemperature();
  
  switch (mode) {
    case OFF:
      digitalWrite(HEATER_PIN, LOW);
      digitalWrite(COOLER_PIN, LOW);
      break;
      
    case HEATING:
      digitalWrite(HEATER_PIN, HIGH);
      digitalWrite(COOLER_PIN, LOW);
      break;
      
    case COOLING:
      digitalWrite(HEATER_PIN, LOW);
      digitalWrite(COOLER_PIN, HIGH);
      break;
      
    case AUTO:
      if (temperature < 20.0) {
        digitalWrite(HEATER_PIN, HIGH);
        digitalWrite(COOLER_PIN, LOW);
      } else if (temperature > 25.0) {
        digitalWrite(HEATER_PIN, LOW);
        digitalWrite(COOLER_PIN, HIGH);
      } else {
        digitalWrite(HEATER_PIN, LOW);
        digitalWrite(COOLER_PIN, LOW);
      }
      break;
  }
}
```

## Key Points
- Use enum for state definitions (readable, type-safe)
- Track stateStartTime for elapsed time checks
- Each state handles its own transitions
- Emergency states should be checked BEFORE normal state logic
- Use updateState() helper to centralize state changes
- Combine with EveryMs timers for periodic state updates
- States should be mutually exclusive (only one active at a time)
