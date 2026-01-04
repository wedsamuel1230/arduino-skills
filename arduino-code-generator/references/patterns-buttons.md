# Button Debouncing & Input Handling

## Basic Software Debouncing

```cpp
class DebouncedButton {
private:
  uint8_t pin;
  uint8_t lastState;
  unsigned long lastDebounceTime;
  uint16_t debounceDelay;
  
public:
  DebouncedButton(uint8_t buttonPin, uint16_t delay = 50) 
    : pin(buttonPin), lastState(HIGH), lastDebounceTime(0), debounceDelay(delay) {
    pinMode(pin, INPUT_PULLUP);
  }
  
  bool isPressed() {
    uint8_t reading = digitalRead(pin);
    
    if (reading != lastState) {
      lastDebounceTime = millis();
    }
    
    if ((millis() - lastDebounceTime) > debounceDelay) {
      if (reading == LOW) {
        lastState = reading;
        return true;
      }
    }
    
    lastState = reading;
    return false;
  }
};

// Usage
DebouncedButton button(2);

void loop() {
  if (button.isPressed()) {
    Serial.println(F("Button pressed!"));
  }
}
```

## Edge Detection (Press/Release Events)

```cpp
class ButtonWithEvents {
private:
  uint8_t pin;
  uint8_t currentState;
  uint8_t previousState;
  unsigned long lastDebounceTime;
  uint16_t debounceDelay;
  
public:
  enum Event { NONE, PRESSED, RELEASED };
  
  ButtonWithEvents(uint8_t buttonPin, uint16_t delay = 50) 
    : pin(buttonPin), currentState(HIGH), previousState(HIGH), 
      lastDebounceTime(0), debounceDelay(delay) {
    pinMode(pin, INPUT_PULLUP);
  }
  
  Event update() {
    uint8_t reading = digitalRead(pin);
    
    if (reading != previousState) {
      lastDebounceTime = millis();
    }
    
    if ((millis() - lastDebounceTime) > debounceDelay) {
      if (reading != currentState) {
        currentState = reading;
        previousState = reading;
        return (currentState == LOW) ? PRESSED : RELEASED;
      }
    }
    
    previousState = reading;
    return NONE;
  }
};

// Usage
ButtonWithEvents button(2);

void loop() {
  ButtonWithEvents::Event event = button.update();
  
  if (event == ButtonWithEvents::PRESSED) {
    Serial.println(F("↓ Button pressed"));
  } else if (event == ButtonWithEvents::RELEASED) {
    Serial.println(F("↑ Button released"));
  }
}
```

## Long Press Detection

```cpp
class ButtonWithLongPress {
private:
  uint8_t pin;
  uint8_t state;
  unsigned long pressStartTime;
  unsigned long longPressThreshold;
  bool longPressTriggered;
  
public:
  enum Event { NONE, SHORT_PRESS, LONG_PRESS, RELEASED };
  
  ButtonWithLongPress(uint8_t buttonPin, unsigned long threshold = 1000) 
    : pin(buttonPin), state(HIGH), pressStartTime(0), 
      longPressThreshold(threshold), longPressTriggered(false) {
    pinMode(pin, INPUT_PULLUP);
  }
  
  Event update() {
    uint8_t reading = digitalRead(pin);
    
    if (reading == LOW && state == HIGH) {
      // Button just pressed
      pressStartTime = millis();
      longPressTriggered = false;
      state = LOW;
    } 
    else if (reading == LOW && state == LOW) {
      // Button held down
      if (!longPressTriggered && (millis() - pressStartTime) >= longPressThreshold) {
        longPressTriggered = true;
        return LONG_PRESS;
      }
    }
    else if (reading == HIGH && state == LOW) {
      // Button released
      state = HIGH;
      if (!longPressTriggered) {
        return SHORT_PRESS;
      }
      return RELEASED;
    }
    
    return NONE;
  }
};

// Usage
ButtonWithLongPress button(2, 2000);  // 2 second long press

void loop() {
  ButtonWithLongPress::Event event = button.update();
  
  if (event == ButtonWithLongPress::SHORT_PRESS) {
    Serial.println(F("Short press - Toggle LED"));
  } else if (event == ButtonWithLongPress::LONG_PRESS) {
    Serial.println(F("Long press - Reset system"));
  }
}
```

## Multi-Button Manager

```cpp
class MultiButtonManager {
private:
  static const uint8_t MAX_BUTTONS = 8;
  DebouncedButton* buttons[MAX_BUTTONS];
  uint8_t buttonCount;
  
public:
  MultiButtonManager() : buttonCount(0) {}
  
  void addButton(DebouncedButton* btn) {
    if (buttonCount < MAX_BUTTONS) {
      buttons[buttonCount++] = btn;
    }
  }
  
  int checkButtons() {
    for (uint8_t i = 0; i < buttonCount; i++) {
      if (buttons[i]->isPressed()) {
        return i;
      }
    }
    return -1;
  }
};

// Usage
DebouncedButton btn1(2);
DebouncedButton btn2(3);
DebouncedButton btn3(4);
MultiButtonManager manager;

void setup() {
  Serial.begin(115200);
  manager.addButton(&btn1);
  manager.addButton(&btn2);
  manager.addButton(&btn3);
}

void loop() {
  int pressed = manager.checkButtons();
  if (pressed >= 0) {
    Serial.print(F("Button "));
    Serial.print(pressed);
    Serial.println(F(" pressed"));
  }
}
```

## Key Points
- Always debounce buttons (hardware bounce lasts 5-50ms)
- Use INPUT_PULLUP to avoid external resistors
- Never use delay() in button checking (blocks other code)
- Edge detection detects PRESS and RELEASE separately
- Long press: track press duration before release
- Multi-button: check all buttons each loop, return first pressed
