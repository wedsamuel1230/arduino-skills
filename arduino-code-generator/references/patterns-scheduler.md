# Non-Blocking Scheduler & Timing Patterns

## EveryMs Pattern (Core Building Block)

```cpp
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
  
  void reset() {
    lastTrigger = millis();
  }
};

// Usage: Blink LED every 1000ms, read sensor every 500ms
EveryMs blinkTimer(1000);
EveryMs sensorTimer(500);

void loop() {
  if (blinkTimer.check()) {
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
  }
  
  if (sensorTimer.check()) {
    int value = analogRead(A0);
    Serial.println(value);
  }
}
```

## Priority Task Scheduler

```cpp
class Task {
public:
  typedef void (*TaskFunction)();
  enum Priority { LOW, NORMAL, HIGH, CRITICAL };
  
private:
  TaskFunction callback;
  unsigned long interval;
  unsigned long lastRun;
  Priority priority;
  bool enabled;
  
public:
  Task(TaskFunction func, unsigned long ms, Priority pri = NORMAL)
    : callback(func), interval(ms), lastRun(0), priority(pri), enabled(true) {}
  
  bool shouldRun() const {
    if (!enabled) return false;
    return (millis() - lastRun >= interval);
  }
  
  void execute() {
    if (callback) callback();
    lastRun = millis();
  }
  
  Priority getPriority() const { return priority; }
  void enable() { enabled = true; }
  void disable() { enabled = false; }
};

class Scheduler {
private:
  static const uint8_t MAX_TASKS = 10;
  Task* tasks[MAX_TASKS];
  uint8_t taskCount;
  
public:
  Scheduler() : taskCount(0) {}
  
  bool addTask(Task* task) {
    if (taskCount >= MAX_TASKS) return false;
    tasks[taskCount++] = task;
    return true;
  }
  
  void run() {
    Task* readyTask = nullptr;
    Task::Priority highestPriority = Task::LOW;
    
    // Find highest priority task that's ready
    for (uint8_t i = 0; i < taskCount; i++) {
      if (tasks[i]->shouldRun()) {
        if (tasks[i]->getPriority() > highestPriority || readyTask == nullptr) {
          readyTask = tasks[i];
          highestPriority = tasks[i]->getPriority();
        }
      }
    }
    
    if (readyTask) {
      readyTask->execute();
    }
  }
};

// Task functions
void taskBlinkLED() {
  digitalWrite(LED_PIN, !digitalRead(LED_PIN));
}

void taskReadSensor() {
  int value = analogRead(A0);
  Serial.println(value);
}

// Global scheduler
Scheduler scheduler;
Task ledTask(taskBlinkLED, 1000, Task::NORMAL);
Task sensorTask(taskReadSensor, 500, Task::HIGH);

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  
  scheduler.addTask(&ledTask);
  scheduler.addTask(&sensorTask);
}

void loop() {
  scheduler.run();
}
```

## Multi-Task Environmental Monitor

```cpp
#include <DHT.h>

DHT dht(2, DHT22);
EveryMs readDHTTimer(2000);      // DHT22 needs 2s between reads
EveryMs readLightTimer(1000);
EveryMs displayTimer(5000);
EveryMs csvLogTimer(10000);

struct SensorData {
  float temperature;
  float humidity;
  int lightLevel;
} data;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(A0, INPUT);
  dht.begin();
  
  Serial.println(F("Time_ms,Temp_C,Humidity_%,Light"));
}

void loop() {
  // Task 1: Read DHT22
  if (readDHTTimer.check()) {
    data.temperature = dht.readTemperature();
    data.humidity = dht.readHumidity();
  }
  
  // Task 2: Read light sensor
  if (readLightTimer.check()) {
    data.lightLevel = analogRead(A0);
  }
  
  // Task 3: Display summary
  if (displayTimer.check()) {
    Serial.print(F("Temp: "));
    Serial.print(data.temperature, 1);
    Serial.print(F("°C | Humidity: "));
    Serial.print(data.humidity, 1);
    Serial.println(F("%"));
  }
  
  // Task 4: Log CSV
  if (csvLogTimer.check()) {
    Serial.print(millis());
    Serial.print(F(","));
    Serial.print(data.temperature, 1);
    Serial.print(F(","));
    Serial.print(data.humidity, 1);
    Serial.print(F(","));
    Serial.println(data.lightLevel);
  }
  
  // LED heartbeat
  digitalWrite(LED_PIN, (millis() % 2000) < 100);
}
```

## Key Points
- NEVER use delay() for timing (blocks everything)
- Use unsigned long for millis() (handles overflow correctly)
- EveryMs pattern: simplest non-blocking timer
- Scheduler: run multiple tasks with priorities
- Each task tracks its own last execution time
- Unsigned arithmetic handles millis() overflow (every 49 days)
