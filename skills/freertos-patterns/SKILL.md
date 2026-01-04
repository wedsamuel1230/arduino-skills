---
id: freertos-patterns
title: FreeRTOS Patterns for ESP32 & RP2040 Multicore
category: arduino
platforms:
  - esp32
  - rp2040
whenToUse: |
  When users need multitasking, task synchronization, or real-time scheduling on ESP32 (FreeRTOS) or RP2040 (dual-core).
  Triggers: "FreeRTOS", "ESP32 tasks", "multitasking", "task priority", "semaphore", "queue", "mutex", "task synchronization", "RTOS patterns", "preemptive scheduling", "RP2040 dual core", "loop1", "setup1", "multicore"
---

# FreeRTOS Patterns for ESP32 & RP2040 Multicore

Comprehensive patterns for multitasking on ESP32 (FreeRTOS) and RP2040 (dual-core with mutex synchronization).

## Resources

- **references/patterns-task-creation.md** - Task lifecycle, priorities, stack sizing
- **references/patterns-queues.md** - Inter-task communication via queues
- **references/patterns-synchronization.md** - Semaphores, mutexes, critical sections
- **references/patterns-memory.md** - Heap management, stack monitoring
- **references/patterns-advanced.md** - Watchdogs, notifications, event groups
- **assets/workflow.mmd** - FreeRTOS architecture diagram

## Quick Start

```cpp
#include <Arduino.h>

// Task function prototype
void taskBlink(void* parameter);

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  
  // Create task with priority 1, 2KB stack
  xTaskCreate(
    taskBlink,          // Task function
    "Blink",            // Task name
    2048,               // Stack size (bytes)
    NULL,               // Parameters
    1,                  // Priority (0 = lowest)
    NULL                // Task handle
  );
}

void taskBlink(void* parameter) {
  while(true) {
    digitalWrite(LED_BUILTIN, HIGH);
    vTaskDelay(pdMS_TO_TICKS(500));
    digitalWrite(LED_BUILTIN, LOW);
    vTaskDelay(pdMS_TO_TICKS(500));
  }
}

void loop() {
  // Empty - FreeRTOS scheduler manages tasks
}
```

## When to Use

### ESP32 FreeRTOS
Use FreeRTOS patterns when:
- **Multiple concurrent operations** - WiFi + sensor reading + display updates
- **Priority-based scheduling** - Critical tasks (safety) must preempt low-priority tasks
- **Real-time constraints** - Guaranteed response time needed
- **Complex synchronization** - Shared resources between tasks (UART, SPI, I2C)
- **Event-driven architecture** - Tasks wake on events (button press, network packet)

### RP2040 Dual-Core
Use RP2040 multicore patterns when:
- **Parallel execution** - WiFi/Bluetooth on Core1, sensors on Core0
- **Dedicated cores** - Audio processing on Core1, UI on Core0
- **Simple threading** - Only 2 tasks needed (setup1/loop1 simpler than FreeRTOS)
- **Mutex protection** - Shared data between cores (similar to FreeRTOS mutex)

**Platform Comparison:**
```
ESP32:  Core0 (Protocol) + Core1 (App) = 240MHz dual-core, 520KB SRAM
RP2040: Core0 (loop0)    + Core1 (loop1) = 133MHz dual-core, 264KB SRAM
```

**Don't use threading when:**
- ❌ Arduino UNO/Nano (single core, use millis() patterns instead)
- ❌ Simple sequential logic (overhead not justified)
- ❌ Battery-powered projects (cooperative scheduling more efficient)

## Core Principles

1. **Task as Infinite Loop** - Each task is a function with `while(true)` loop
2. **Blocking is OK** - vTaskDelay() yields CPU to other tasks (unlike delay())
3. **Stack Per Task** - Each task has isolated stack (2-4KB typical)
4. **Priority Preemption** - Higher priority tasks interrupt lower priority tasks
5. **Synchronization Primitives** - Use queues/semaphores for inter-task communication

## Implementation

### Pattern 1: Basic Multi-Tasking

```cpp
#include <Arduino.h>

// Task handles for monitoring
TaskHandle_t taskBlinkHandle;
TaskHandle_t taskSensorHandle;

// Shared data (protected by mutex)
SemaphoreHandle_t dataMutex;
float sensorValue = 0.0;

void taskBlink(void* parameter) {
  pinMode(LED_BUILTIN, OUTPUT);
  
  while(true) {
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void taskReadSensor(void* parameter) {
  pinMode(A0, INPUT);
  
  while(true) {
    int raw = analogRead(A0);
    float voltage = raw * (3.3 / 4095.0);
    
    // Protect shared data with mutex
    if (xSemaphoreTake(dataMutex, pdMS_TO_TICKS(100))) {
      sensorValue = voltage;
      xSemaphoreGive(dataMutex);
    }
    
    vTaskDelay(pdMS_TO_TICKS(500));
  }
}

void taskPrintStats(void* parameter) {
  while(true) {
    // Read shared data safely
    float localValue;
    if (xSemaphoreTake(dataMutex, pdMS_TO_TICKS(100))) {
      localValue = sensorValue;
      xSemaphoreGive(dataMutex);
    }
    
    Serial.print("Sensor: ");
    Serial.print(localValue, 2);
    Serial.println(" V");
    
    vTaskDelay(pdMS_TO_TICKS(2000));
  }
}

void setup() {
  Serial.begin(115200);
  
  // Create mutex before tasks
  dataMutex = xSemaphoreCreateMutex();
  
  // Create tasks with different priorities
  xTaskCreate(taskBlink, "Blink", 2048, NULL, 1, &taskBlinkHandle);
  xTaskCreate(taskReadSensor, "Sensor", 4096, NULL, 2, &taskSensorHandle);
  xTaskCreate(taskPrintStats, "Print", 4096, NULL, 1, NULL);
}

void loop() {
  // Monitor tasks every 5 seconds
  vTaskDelay(pdMS_TO_TICKS(5000));
  
  Serial.println("\n=== Task Statistics ===");
  Serial.printf("Free heap: %d bytes\n", ESP.getFreeHeap());
  
  // Get stack high water marks
  UBaseType_t blinkStack = uxTaskGetStackHighWaterMark(taskBlinkHandle);
  UBaseType_t sensorStack = uxTaskGetStackHighWaterMark(taskSensorHandle);
  
  Serial.printf("Blink task free stack: %d bytes\n", blinkStack * 4);
  Serial.printf("Sensor task free stack: %d bytes\n", sensorStack * 4);
}
```

### Pattern 2: Queue-Based Communication

```cpp
#include <Arduino.h>

// Queue for sensor data
QueueHandle_t sensorQueue;

struct SensorData {
  uint32_t timestamp;
  float temperature;
  float humidity;
  int lightLevel;
};

void taskReadSensors(void* parameter) {
  SensorData data;
  
  while(true) {
    data.timestamp = millis();
    data.temperature = random(200, 300) / 10.0; // Mock: 20-30°C
    data.humidity = random(400, 700) / 10.0;     // Mock: 40-70%
    data.lightLevel = analogRead(A0);
    
    // Send to queue (wait max 10ms)
    if (xQueueSend(sensorQueue, &data, pdMS_TO_TICKS(10)) != pdPASS) {
      Serial.println("Queue full, dropping data!");
    }
    
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void taskLogData(void* parameter) {
  SensorData data;
  
  while(true) {
    // Wait indefinitely for data
    if (xQueueReceive(sensorQueue, &data, portMAX_DELAY) == pdPASS) {
      Serial.printf("[%lu] T=%.1f°C H=%.1f%% L=%d\n",
                    data.timestamp,
                    data.temperature,
                    data.humidity,
                    data.lightLevel);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(A0, INPUT);
  
  // Create queue: 10 items, size of SensorData struct
  sensorQueue = xQueueCreate(10, sizeof(SensorData));
  
  if (sensorQueue == NULL) {
    Serial.println("Queue creation failed!");
    while(1);
  }
  
  xTaskCreate(taskReadSensors, "Producer", 4096, NULL, 2, NULL);
  xTaskCreate(taskLogData, "Consumer", 4096, NULL, 1, NULL);
}

void loop() {
  vTaskDelay(portMAX_DELAY);
}
```

### Pattern 3: Priority Inversion Protection

```cpp
#include <Arduino.h>

// Mutex with priority inheritance
SemaphoreHandle_t resourceMutex;

void taskHighPriority(void* parameter) {
  while(true) {
    Serial.println("HIGH: Requesting resource...");
    
    if (xSemaphoreTake(resourceMutex, pdMS_TO_TICKS(1000))) {
      Serial.println("HIGH: Got resource");
      vTaskDelay(pdMS_TO_TICKS(100));
      xSemaphoreGive(resourceMutex);
    } else {
      Serial.println("HIGH: Timeout!");
    }
    
    vTaskDelay(pdMS_TO_TICKS(2000));
  }
}

void taskLowPriority(void* parameter) {
  while(true) {
    Serial.println("LOW: Requesting resource...");
    
    if (xSemaphoreTake(resourceMutex, pdMS_TO_TICKS(1000))) {
      Serial.println("LOW: Got resource, holding 500ms...");
      vTaskDelay(pdMS_TO_TICKS(500)); // Simulate long operation
      xSemaphoreGive(resourceMutex);
    }
    
    vTaskDelay(pdMS_TO_TICKS(3000));
  }
}

void setup() {
  Serial.begin(115200);
  
  // Create mutex with priority inheritance
  resourceMutex = xSemaphoreCreateMutex();
  
  // Low priority task gets resource first
  xTaskCreate(taskLowPriority, "Low", 2048, NULL, 1, NULL);
  vTaskDelay(pdMS_TO_TICKS(100));
  
  // High priority task will boost low priority when waiting
  xTaskCreate(taskHighPriority, "High", 2048, NULL, 3, NULL);
}

void loop() {
  vTaskDelay(portMAX_DELAY);
}
```

### Pattern 4: Binary Semaphore for ISR Synchronization

```cpp
#include <Arduino.h>

#define BUTTON_PIN 0  // Boot button on ESP32

SemaphoreHandle_t buttonSemaphore;
volatile uint32_t isrCount = 0;

// ISR handler
void IRAM_ATTR buttonISR() {
  isrCount++;
  BaseType_t xHigherPriorityTaskWoken = pdFALSE;
  
  // Signal semaphore from ISR
  xSemaphoreGiveFromISR(buttonSemaphore, &xHigherPriorityTaskWoken);
  
  if (xHigherPriorityTaskWoken) {
    portYIELD_FROM_ISR();
  }
}

void taskButtonHandler(void* parameter) {
  uint32_t eventCount = 0;
  
  while(true) {
    // Wait indefinitely for semaphore
    if (xSemaphoreTake(buttonSemaphore, portMAX_DELAY) == pdPASS) {
      eventCount++;
      Serial.printf("Button event #%lu (ISR count: %lu)\n", 
                    eventCount, isrCount);
      
      // Debounce delay
      vTaskDelay(pdMS_TO_TICKS(200));
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  // Create binary semaphore (initially empty)
  buttonSemaphore = xSemaphoreCreateBinary();
  
  xTaskCreate(taskButtonHandler, "Button", 2048, NULL, 3, NULL);
  
  // Attach interrupt
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonISR, FALLING);
  
  Serial.println("Press button (GPIO 0) to trigger event");
}

void loop() {
  vTaskDelay(portMAX_DELAY);
}
```

### Pattern 5: Task Notifications (Lightweight Alternative)

```cpp
#include <Arduino.h>

TaskHandle_t workerTaskHandle;

void taskWorker(void* parameter) {
  uint32_t notificationValue;
  
  while(true) {
    // Wait for notification (blocks indefinitely)
    notificationValue = ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
    
    Serial.printf("Received notification: %lu\n", notificationValue);
    
    // Process work based on notification count
    for (uint32_t i = 0; i < notificationValue; i++) {
      Serial.printf("Processing task %lu...\n", i + 1);
      vTaskDelay(pdMS_TO_TICKS(100));
    }
  }
}

void taskController(void* parameter) {
  uint32_t workCount = 1;
  
  while(true) {
    vTaskDelay(pdMS_TO_TICKS(2000));
    
    Serial.printf("Sending %lu work items\n", workCount);
    
    // Notify worker task (increment notification count)
    xTaskNotifyGive(workerTaskHandle);
    
    workCount = (workCount % 5) + 1;
  }
}

void setup() {
  Serial.begin(115200);
  
  xTaskCreate(taskWorker, "Worker", 2048, NULL, 2, &workerTaskHandle);
  xTaskCreate(taskController, "Controller", 2048, NULL, 1, NULL);
}

void loop() {
  vTaskDelay(portMAX_DELAY);
}
```

### Pattern 6: RP2040 Dual-Core with Mutex (Pico SDK)

**Note:** RP2040 uses `setup1()`/`loop1()` for Core1, not FreeRTOS tasks.

```cpp
#include <Arduino.h>
#include <pico/mutex.h>

// Shared data protected by mutex
mutex_t dataMutex;
float sharedSensorValue = 0.0;
volatile uint32_t core0Count = 0;
volatile uint32_t core1Count = 0;

// Core 0: Default Arduino setup() and loop()
void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(A0, INPUT);
  
  // Initialize mutex before Core1 starts
  mutex_init(&dataMutex);
  
  Serial.println("Core0 setup complete");
}

void loop() {
  // Core 0: Read sensor with mutex protection
  int raw = analogRead(A0);
  float voltage = raw * (3.3 / 4095.0);
  
  mutex_enter_blocking(&dataMutex);
  sharedSensorValue = voltage;
  core0Count++;
  mutex_exit(&dataMutex);
  
  digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  delay(500);
}

// Core 1: Runs in parallel on second core
void setup1() {
  Serial.println("Core1 setup complete");
}

void loop1() {
  // Core 1: Print sensor data with mutex protection
  float localValue;
  uint32_t localCore0Count, localCore1Count;
  
  mutex_enter_blocking(&dataMutex);
  localValue = sharedSensorValue;
  localCore0Count = core0Count;
  localCore1Count = core1Count;
  core1Count++;
  mutex_exit(&dataMutex);
  
  Serial.printf("Sensor: %.2fV | Core0: %lu | Core1: %lu\n",
                localValue, localCore0Count, localCore1Count);
  
  delay(1000);
}
```

**Key Differences from ESP32:**
- ✅ No `xTaskCreate()` - use `setup1()`/`loop1()` for Core1
- ✅ Mutex API: `mutex_enter_blocking()` instead of `xSemaphoreTake()`
- ✅ Simpler model: Only 2 cores (no priority levels or task handles)
- ✅ Both cores run infinite loops (like Arduino loop())
- ⚠️ Must initialize mutex in `setup()` before Core1 starts
- ⚠️ RP2040 has 264KB SRAM vs ESP32's 520KB (smaller stack available)

## Verification Steps

### Test 1: Task Creation & Scheduling

```cpp
// Expected output:
[HIGH] Priority 3 task running
[MED] Priority 2 task running
[LOW] Priority 1 task running
Free heap: ~280000 bytes
```

**Pass criteria:**
- ✅ High priority task preempts lower priority tasks
- ✅ All tasks execute in priority order
- ✅ No stack overflow errors
- ✅ Heap remains stable over 1 minute

### Test 2: Queue Communication

```cpp
// Expected output:
[1234] T=25.3°C H=55.2% L=2048
[2234] T=26.1°C H=53.8% L=2051
Queue spaces available: 7
```

**Pass criteria:**
- ✅ Producer never blocks (queue not full)
- ✅ Consumer receives data in FIFO order
- ✅ No data corruption or garbled values
- ✅ Queue usage stays below 80%

### Test 3: Mutex Protection

```cpp
// Expected output:
Task A: value = 0
Task B: value = 1
Task A: value = 2
// No race conditions or torn reads
```

**Pass criteria:**
- ✅ No simultaneous access to shared data
- ✅ Value increments correctly (no lost updates)
- ✅ No deadlocks after 5 minutes
- ✅ Mutex always released after take

### Test 4: Stack Monitoring

```cpp
// Expected output:
Task 'Blink' free stack: 1456 bytes (72% free)
Task 'Sensor' free stack: 3012 bytes (73% free)
WARNING: Task 'Logger' only 200 bytes free!
```

**Pass criteria:**
- ✅ All tasks maintain >20% free stack
- ✅ No stack overflow exceptions
- ✅ High water mark doesn't decrease over time
- ✅ configCHECK_FOR_STACK_OVERFLOW enabled

## Common Pitfalls

### ❌ Pitfall 1: Insufficient Stack Size

```cpp
// WRONG: Task stack too small
xTaskCreate(taskBigArray, "Task", 1024, NULL, 1, NULL);

void taskBigArray(void* parameter) {
  char buffer[2048];  // Stack overflow!
  // ...
}
```

**Fix:**
```cpp
✅ // Calculate stack: function locals + call stack + margin
xTaskCreate(taskBigArray, "Task", 4096, NULL, 1, NULL);

// Monitor at runtime
UBaseType_t freeStack = uxTaskGetStackHighWaterMark(NULL);
if (freeStack < 512) {
  Serial.println("WARNING: Low stack!");
}
```

### ❌ Pitfall 2: Using delay() Instead of vTaskDelay()

```cpp
// WRONG: Blocks entire CPU
void taskBlink(void* parameter) {
  while(true) {
    digitalWrite(LED, HIGH);
    delay(1000);  // Other tasks can't run!
    digitalWrite(LED, LOW);
    delay(1000);
  }
}
```

**Fix:**
```cpp
✅ void taskBlink(void* parameter) {
  while(true) {
    digitalWrite(LED, HIGH);
    vTaskDelay(pdMS_TO_TICKS(1000));  // Yields to other tasks
    digitalWrite(LED, LOW);
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}
```

### ❌ Pitfall 3: Unprotected Shared Data

```cpp
// WRONG: Race condition
int sharedCounter = 0;

void taskA(void* p) {
  while(true) {
    sharedCounter++;  // Not atomic!
    vTaskDelay(10);
  }
}

void taskB(void* p) {
  while(true) {
    Serial.println(sharedCounter);  // May read torn value
    vTaskDelay(10);
  }
}
```

**Fix:**
```cpp
✅ SemaphoreHandle_t counterMutex;
int sharedCounter = 0;

void taskA(void* p) {
  while(true) {
    xSemaphoreTake(counterMutex, portMAX_DELAY);
    sharedCounter++;
    xSemaphoreGive(counterMutex);
    vTaskDelay(10);
  }
}

void taskB(void* p) {
  while(true) {
    xSemaphoreTake(counterMutex, portMAX_DELAY);
    int local = sharedCounter;
    xSemaphoreGive(counterMutex);
    Serial.println(local);
    vTaskDelay(10);
  }
}
```

### ❌ Pitfall 4: Forgetting IRAM_ATTR for ISR

```cpp
// WRONG: ISR may crash if code not in IRAM
void buttonISR() {
  xSemaphoreGiveFromISR(sem, NULL);
}
```

**Fix:**
```cpp
✅ void IRAM_ATTR buttonISR() {
  BaseType_t xHigherPriorityTaskWoken = pdFALSE;
  xSemaphoreGiveFromISR(sem, &xHigherPriorityTaskWoken);
  
  if (xHigherPriorityTaskWoken) {
    portYIELD_FROM_ISR();
  }
}
```

### ❌ Pitfall 5: Deadlock from Improper Lock Order

```cpp
// WRONG: Task A locks mutex1 then mutex2
//        Task B locks mutex2 then mutex1
//        = DEADLOCK!

void taskA(void* p) {
  xSemaphoreTake(mutex1, portMAX_DELAY);
  xSemaphoreTake(mutex2, portMAX_DELAY);
  // Critical section
  xSemaphoreGive(mutex2);
  xSemaphoreGive(mutex1);
}

void taskB(void* p) {
  xSemaphoreTake(mutex2, portMAX_DELAY);  // Wrong order!
  xSemaphoreTake(mutex1, portMAX_DELAY);
  // Critical section
  xSemaphoreGive(mutex1);
  xSemaphoreGive(mutex2);
}
```

**Fix:**
```cpp
✅ // ALWAYS acquire locks in same order
void taskA(void* p) {
  xSemaphoreTake(mutex1, portMAX_DELAY);
  xSemaphoreTake(mutex2, portMAX_DELAY);
  // Critical section
  xSemaphoreGive(mutex2);
  xSemaphoreGive(mutex1);
}

void taskB(void* p) {
  xSemaphoreTake(mutex1, portMAX_DELAY);  // Same order!
  xSemaphoreTake(mutex2, portMAX_DELAY);
  // Critical section
  xSemaphoreGive(mutex2);
  xSemaphoreGive(mutex1);
}
```

### ❌ Pitfall 6: RP2040 Mutex Not Initialized Before Core1

```cpp
// WRONG: Core1 may start before mutex is ready
void setup() {
  Serial.begin(115200);
  // Core1's setup1() may run here!
}

void setup1() {
  mutex_init(&myMutex);  // Too late! Core0 may access mutex
}
```

**Fix:**
```cpp
✅ // Initialize mutex in setup() before Core1 starts
mutex_t myMutex;

void setup() {
  Serial.begin(115200);
  mutex_init(&myMutex);  // Core1 guaranteed to see initialized mutex
}

void setup1() {
  // Mutex already ready
}
```

## Engineering Rationale

### Why FreeRTOS on ESP32?

1. **Native Integration** - ESP-IDF builds on FreeRTOS, zero setup overhead
2. **Dual-Core Support** - Tasks can run on Core 0 (protocol) and Core 1 (app)
3. **Priority Preemption** - Critical tasks interrupt lower priority tasks automatically
4. **Rich Primitives** - Queues, semaphores, mutexes, timers, event groups built-in
5. **Stack Isolation** - Each task has its own stack (prevents corruption)
6. **Blocking is Efficient** - vTaskDelay() yields CPU (unlike delay() which wastes cycles)

### Why RP2040 Multicore (Without FreeRTOS)?

1. **Simpler Model** - Only 2 cores, no task scheduler overhead
2. **Lower Latency** - Direct core assignment vs scheduler dispatch
3. **Arduino-like** - setup1()/loop1() familiar to Arduino programmers
4. **Memory Efficient** - No RTOS kernel overhead (~8KB savings)
5. **Deterministic** - No context switching or priority inversion
6. **Good for Dedicated Tasks** - Core0 = WiFi, Core1 = Audio processing

### ESP32 vs RP2040 Threading Models

**ESP32 FreeRTOS:**
- ✅ Unlimited tasks (limited by RAM)
- ✅ Priority-based preemption (0-24 levels)
- ✅ Rich synchronization (queues, semaphores, mutexes, event groups)
- ✅ Software timers and watchdogs
- ⚠️ ~8KB kernel overhead
- ⚠️ Context switching overhead (~10µs)

**RP2040 Multicore:**
- ✅ Zero RTOS overhead
- ✅ Direct core assignment (deterministic)
- ✅ Lower latency (no scheduler)
- ✅ Simple mutex API
- ⚠️ Only 2 parallel tasks (Core0 + Core1)
- ⚠️ No priority levels or preemption
- ⚠️ Manual synchronization required

**When to Choose Which:**
- **ESP32:** Need >2 concurrent tasks, priority scheduling, or event-driven architecture
- **RP2040:** Need exactly 2 parallel tasks, deterministic timing, or minimal overhead

### Memory Comparison

```
Platform     SRAM     Flash    Cores   Clock    Cost
ESP32        520KB    4MB      2       240MHz   $8
RP2040       264KB    2MB      2       133MHz   $4
Arduino UNO  2KB      32KB     1       16MHz    $25
```

### Task vs Core Model

**ESP32 Task Model:**
```cpp
xTaskCreatePinnedToCore(task1, "T1", 4096, NULL, 2, NULL, 0);  // Core 0
xTaskCreatePinnedToCore(task2, "T2", 4096, NULL, 1, NULL, 1);  // Core 1
xTaskCreatePinnedToCore(task3, "T3", 4096, NULL, 3, NULL, 0);  // Core 0 (high priority)
// Scheduler manages 3+ tasks across 2 cores
```

**RP2040 Core Model:**
```cpp
void setup()  { /* Core 0 init */ }
void loop()   { /* Core 0 work */ }
void setup1() { /* Core 1 init */ }
void loop1()  { /* Core 1 work */ }
// Exactly 2 parallel infinite loops
```

### Mutex Performance

**ESP32 FreeRTOS Mutex:**
- Take/Give: ~2µs
- Priority inheritance: Automatic
- Timeout support: Yes
- ISR-safe variant: `xSemaphoreTakeFromISR()`

**RP2040 Pico SDK Mutex:**
- Enter/Exit: ~0.5µs (4× faster)
- Priority inheritance: N/A (no priorities)
- Timeout support: Limited (`mutex_enter_timeout_us()`)
- ISR-safe: Use spinlocks instead
3. **WiFi Stack Integration** - WiFi library uses FreeRTOS tasks internally
4. **Priority Scheduling** - Critical tasks (motor control) preempt background tasks (logging)
5. **Memory Overhead** - ~8KB kernel + 2-4KB per task (affordable with 520KB SRAM)

### Task Priority Guidelines

| Priority | Use Case | Example |
|----------|----------|---------|
| 0 | Idle task (auto-created) | Cleanup, power management |
| 1-2 | Background logging, LED blink | Data logging, status updates |
| 3-5 | Sensor reading, network | WiFi, I2C/SPI communication |
| 6-10 | Real-time control, safety | Motor control, emergency stop |
| 11-24 | Reserved for system | WiFi stack, Bluetooth |

**Rule:** Keep user tasks in 1-10 range, leave 11+ for ESP-IDF internals.

### Stack Sizing Formula

```
Stack Size = Function Locals + Call Chain + Margin

Example:
- Function has 1KB local array
- Calls 3 functions (256 bytes each)
- Margin: 1KB
Total: 1024 + 768 + 1024 = 2816 → Round to 3072 (3KB)
```

**Monitoring:**
```cpp
UBaseType_t freeWords = uxTaskGetStackHighWaterMark(NULL);
uint32_t freeBytes = freeWords * sizeof(StackType_t);
```

### Mutex vs Semaphore vs Queue

| Primitive | Use Case | Max Count | Priority Inheritance |
|-----------|----------|-----------|---------------------|
| **Mutex** | Exclusive resource access | 1 | ✅ Yes |
| **Binary Semaphore** | Event signaling | 1 | ❌ No |
| **Counting Semaphore** | Resource pool (e.g., 5 buffers) | N | ❌ No |
| **Queue** | Data passing | N items | ❌ No |

**When to use each:**
- Mutex: Shared UART, SPI bus, global variable
- Binary Semaphore: ISR → Task notification, one-shot events
- Counting Semaphore: Connection pool, buffer pool
- Queue: Sensor data pipeline, command queue

### Memory Allocation: Heap vs Stack

**FreeRTOS Heap (configTOTAL_HEAP_SIZE):**
- Task control blocks
- Queue storage
- Semaphore/mutex objects
- Dynamic allocation (malloc, new)

**Task Stack (per-task):**
- Local variables
- Function call frames
- ISR context save

**ESP32 Default:**
- Heap: ~280KB free at boot
- Each task: 2-4KB stack typical
- Formula: `totalHeap - (numTasks * avgStackSize) - systemOverhead`

## Advanced Patterns

### Pattern 1: Watchdog Protection

```cpp
#include <esp_task_wdt.h>

void taskCritical(void* parameter) {
  // Register with watchdog (3 second timeout)
  esp_task_wdt_add(NULL);
  
  while(true) {
    // Do critical work
    readSafetySensors();
    updateMotorControl();
    
    // Reset watchdog timer
    esp_task_wdt_reset();
    
    vTaskDelay(pdMS_TO_TICKS(100));
  }
}

void setup() {
  // Enable watchdog
  esp_task_wdt_init(3, true);  // 3 second timeout, panic on trigger
  
  xTaskCreate(taskCritical, "Safety", 4096, NULL, 10, NULL);
}
```

### Pattern 2: Event Groups for Complex Sync

```cpp
#include <Arduino.h>

EventGroupHandle_t systemEvents;

// Event bits
#define BIT_WIFI_CONNECTED    (1 << 0)
#define BIT_SENSOR_READY      (1 << 1)
#define BIT_SD_MOUNTED        (1 << 2)
#define BIT_ALL_READY         (BIT_WIFI_CONNECTED | BIT_SENSOR_READY | BIT_SD_MOUNTED)

void taskStartup(void* parameter) {
  // Wait for all subsystems
  EventBits_t bits = xEventGroupWaitBits(
    systemEvents,
    BIT_ALL_READY,
    pdFALSE,  // Don't clear bits
    pdTRUE,   // Wait for ALL bits
    portMAX_DELAY
  );
  
  if ((bits & BIT_ALL_READY) == BIT_ALL_READY) {
    Serial.println("All subsystems ready, starting main task");
    startMainApplication();
  }
  
  vTaskDelete(NULL);
}

void taskInitWiFi(void* parameter) {
  // Initialize WiFi...
  Serial.println("WiFi connected");
  xEventGroupSetBits(systemEvents, BIT_WIFI_CONNECTED);
  vTaskDelete(NULL);
}

void taskInitSensor(void* parameter) {
  // Initialize sensor...
  Serial.println("Sensor ready");
  xEventGroupSetBits(systemEvents, BIT_SENSOR_READY);
  vTaskDelete(NULL);
}

void taskInitSD(void* parameter) {
  // Initialize SD card...
  Serial.println("SD mounted");
  xEventGroupSetBits(systemEvents, BIT_SD_MOUNTED);
  vTaskDelete(NULL);
}

void setup() {
  Serial.begin(115200);
  
  systemEvents = xEventGroupCreate();
  
  xTaskCreate(taskInitWiFi, "InitWiFi", 4096, NULL, 1, NULL);
  xTaskCreate(taskInitSensor, "InitSensor", 2048, NULL, 1, NULL);
  xTaskCreate(taskInitSD, "InitSD", 2048, NULL, 1, NULL);
  xTaskCreate(taskStartup, "Startup", 2048, NULL, 2, NULL);
}
```

### Pattern 3: Software Timers

```cpp
#include <Arduino.h>

TimerHandle_t periodicTimer;
uint32_t timerCount = 0;

void timerCallback(TimerHandle_t xTimer) {
  timerCount++;
  Serial.printf("Timer fired: %lu\n", timerCount);
  
  // Don't call blocking functions here!
  // Max execution time: ~10ms
}

void setup() {
  Serial.begin(115200);
  
  // Create timer: 1 second period, auto-reload
  periodicTimer = xTimerCreate(
    "Periodic",                 // Name
    pdMS_TO_TICKS(1000),       // Period (1 second)
    pdTRUE,                    // Auto-reload
    NULL,                      // Timer ID
    timerCallback              // Callback
  );
  
  if (periodicTimer != NULL) {
    xTimerStart(periodicTimer, 0);
  }
}

void loop() {
  vTaskDelay(portMAX_DELAY);
}
```

### Pattern 4: Core Affinity (Dual-Core Optimization)

```cpp
// Pin tasks to specific cores
void taskWiFi(void* parameter) {
  while(true) {
    // WiFi operations (run on Core 0 with protocol stack)
    handleWiFiPackets();
    vTaskDelay(pdMS_TO_TICKS(10));
  }
}

void taskApplication(void* parameter) {
  while(true) {
    // Application logic (run on Core 1)
    processUserInput();
    updateDisplay();
    vTaskDelay(pdMS_TO_TICKS(50));
  }
}

void setup() {
  // Core 0: Protocol stack (WiFi, BLE)
  xTaskCreatePinnedToCore(taskWiFi, "WiFi", 4096, NULL, 2, NULL, 0);
  
  // Core 1: Application logic
  xTaskCreatePinnedToCore(taskApplication, "App", 4096, NULL, 1, NULL, 1);
}
```

### Pattern 5: Graceful Task Deletion

```cpp
TaskHandle_t workerHandle;
volatile bool shouldExit = false;

void taskWorker(void* parameter) {
  while(!shouldExit) {
    // Do work
    processData();
    vTaskDelay(pdMS_TO_TICKS(100));
  }
  
  // Cleanup before exit
  Serial.println("Worker task exiting");
  freeResources();
  
  vTaskDelete(NULL);
}

void stopWorker() {
  shouldExit = true;
  
  // Wait for task to exit gracefully
  while(eTaskGetState(workerHandle) != eDeleted) {
    vTaskDelay(pdMS_TO_TICKS(10));
  }
  
  Serial.println("Worker stopped");
}
```

## Integration Notes

### With arduino-non-blocking-scheduler
- **Progression:** millis() scheduler (UNO) → multicore (RP2040) → FreeRTOS (ESP32)
- **When to upgrade:** >2 concurrent operations (use FreeRTOS), or exactly 2 tasks (use RP2040 multicore)
- **Pattern:** Replace EveryMs timers with vTaskDelay() (ESP32) or separate loop1() (RP2040)

### With arduino-state-machine
- **Combine:** State machine logic inside FreeRTOS task or loop1() function
- **Example:** WiFi connection state machine runs in dedicated task (ESP32) or Core1 (RP2040)
- **Benefit:** States don't block other tasks/core during transitions

### With arduino-data-logging
- **Queue-based logging:** Sensor tasks write to queue, logger task reads (ESP32 only)
- **SD card mutex:** Protect SD.write() calls with mutex (both ESP32 and RP2040)
- **Buffering:** Use stream buffer (ESP32) or shared array with mutex (RP2040)

### Platform-Specific Integration
- **ESP32:** Use FreeRTOS tasks with queues and mutexes
- **RP2040:** Use setup1()/loop1() with Pico SDK mutexes
- **UNO/Nano:** Use millis()-based scheduler (no threading)
- **Auto-detect:** Check `#ifdef ESP32` and `#ifdef ARDUINO_ARCH_RP2040` to select pattern

### With arduino-i2c-scanner
- **I2C mutex:** Share I2C bus between multiple sensor tasks
- **Priority:** High-priority task for critical sensors (BME280)
- **Error handling:** Task suspends itself if I2C fails, watchdog triggers

### With arduino-hardware-compatibility
- **Dynamic task creation:** Create tasks based on detected hardware
- **ESP32-specific:** FreeRTOS only available on ESP32 (not UNO/RP2040)
- **Fallback:** Use millis() patterns on non-FreeRTOS platforms

## Acceptance Criteria

**Pre-flight checks:**
- [ ] All tasks created successfully (check return values)
- [ ] Stack sizes validated with uxTaskGetStackHighWaterMark()
- [ ] Mutexes/semaphores created before first use
- [ ] Queues sized appropriately (not full after 1 minute)
- [ ] Priority values in valid range (0-24)
- [ ] Core affinity set correctly (0 or 1)

**Runtime validation:**
- [ ] No stack overflow errors in Serial Monitor
- [ ] Heap usage stable (ESP.getFreeHeap() not decreasing)
- [ ] Task statistics available via vTaskList()
- [ ] Mutex deadlocks detected (timeout, not hang)
- [ ] ISR handlers use IRAM_ATTR and FromISR variants

**Performance criteria:**
- [ ] High priority tasks respond within 10ms
- [ ] Queue processing keeps up with producer rate
- [ ] Watchdog doesn't trigger during normal operation
- [ ] CPU utilization <80% (use vTaskGetRunTimeStats())

**Code quality:**
- [ ] No delay() calls (use vTaskDelay instead)
- [ ] Critical sections minimized (<10ms)
- [ ] Shared data protected by mutex/semaphore
- [ ] Task handle pointers checked for NULL
- [ ] vTaskDelete() called when task exits

## Teaching Notes

**Progression for students:**

1. **Week 1:** Basic task creation, vTaskDelay vs delay()
   - Create 2 tasks: LED blink + serial print
   - Observe preemption with different priorities

2. **Week 2:** Queues for data passing
   - Producer-consumer pattern with sensor data
   - Monitor queue fill level

3. **Week 3:** Mutexes for shared resources
   - Protect shared counter variable
   - Demonstrate race condition without mutex

4. **Week 4:** ISR → Task synchronization
   - Binary semaphore triggered by button interrupt
   - Show task unblocking latency

5. **Week 5:** Complete project
   - Environmental monitor with 4 tasks
   - Queue-based logging, mutex-protected SD card
   - Watchdog protection, stack monitoring

**Common misconceptions:**
- "FreeRTOS tasks are like threads" → Correct: Cooperative + Preemptive scheduling
- "Queues are like variables" → Correct: Copy data, not pointers
- "Higher priority = runs more often" → Correct: Runs first when ready, not more frequently

**Debugging tips:**
- Enable `configCHECK_FOR_STACK_OVERFLOW 2` in sdkconfig (ESP32)
- Use `vTaskList()` to print all task states (ESP32)
- Monitor heap with `ESP.getFreeHeap()` every 5 seconds (ESP32)
- Check task high water mark if crashes occur (ESP32)
- For RP2040: Use `Serial.printf()` to log core execution order

## References

### ESP32 FreeRTOS
- [FreeRTOS Documentation](https://www.freertos.org/Documentation/RTOS_book.html) - Official book (free PDF)
- [ESP-IDF FreeRTOS Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/freertos.html) - ESP32-specific API
- [FreeRTOS API Reference](https://www.freertos.org/a00106.html) - Complete function list
- [Mastering FreeRTOS](https://www.freertos.org/fr-content-src/uploads/2018/07/161204_Mastering_the_FreeRTOS_Real_Time_Kernel-A_Hands-On_Tutorial_Guide.pdf) - Hands-on guide
- [ESP32 Technical Reference](https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf) - Hardware details (dual-core, interrupts)

### RP2040 Multicore
- [Pico SDK Multicore](https://raspberrypi.github.io/pico-sdk-doxygen/group__pico__multicore.html) - Official multicore API
- [RP2040 Datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf) - Dual Cortex-M0+ architecture
- [Arduino-Pico Core](https://arduino-pico.readthedocs.io/en/latest/) - Earle Philhower's Arduino core with multicore support
- [Mutex Examples](https://github.com/raspberrypi/pico-examples/tree/master/multicore) - Official Pico multicore examples

### General RTOS
- [RTOS Design Patterns](https://www.state-machine.com/doc/Sutter08.pdf) - Academic paper on RTOS patterns
